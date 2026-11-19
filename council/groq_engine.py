"""Groq API Engine for fast, low-cost local test generation with hard budget caps."""
import json
import os
from pathlib import Path
import time
import urllib.request

BASE_DIR = Path(__file__).resolve().parents[1]

def load_dotenv():
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())

load_dotenv()

class GroqCouncilEngine:
    """Fast Groq API backend replacing heavy local/Kaggle GPU inference.
    
    Equipped with a STRICT budget circuit breaker: stops execution if cumulative
    tokens exceed max_total_tokens (default 1,000,000) or estimated cost exceeds $5.00.
    """
    def __init__(
        self,
        model: str = "openai/gpt-oss-20b",
        api_key: str = None,
        max_new_tokens: int = 2500,
        temperature: float = 0.2,
        max_total_tokens: int = 1_000_000,
        max_budget_usd: float = 5.0,
        work: Path = None,
        enable_critic: bool = True
    ):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment or .env file.")
        
        self.model = model
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.max_total_tokens = max_total_tokens
        self.max_budget_usd = max_budget_usd
        self.enable_critic = enable_critic
        self.mock = False
        self.work = Path(work) if work else None

        # Pricing estimates per million tokens (conservative overestimates)
        self.cost_per_m_in = 0.15   # $0.15 per 1M prompt tokens
        self.cost_per_m_out = 0.60  # $0.60 per 1M completion tokens

        self.telemetry = {
            "coder_calls": 0, "critic_calls": 0,
            "coder_input_tokens": 0, "critic_input_tokens": 0,
            "coder_tokens": 0, "critic_tokens": 0,
            "total_tokens": 0, "estimated_cost_usd": 0.0,
            "seconds": 0.0
        }

    def _check_budget(self):
        tot = self.telemetry["total_tokens"]
        cost = self.telemetry["estimated_cost_usd"]
        if tot >= self.max_total_tokens:
            raise RuntimeError(
                f"[SAFETY CIRCUIT BREAKER] Cumulative token limit reached: {tot} >= {self.max_total_tokens}. "
                f"Aborting to avoid overspending!"
            )
        if cost >= self.max_budget_usd:
            raise RuntimeError(
                f"[SAFETY CIRCUIT BREAKER] Budget limit reached: ${cost:.4f} >= ${self.max_budget_usd:.2f}. "
                f"Aborting to protect wallet!"
            )

    def _call_groq(self, role: str, system: str, user: str) -> str:
        self._check_budget()
        start = time.perf_counter()

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            "max_tokens": self.max_new_tokens,
            "temperature": self.temperature
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        
        # Retry logic for network resilience
        last_exc = None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    break
            except Exception as e:
                last_exc = e
                time.sleep(1.0 * (attempt + 1))
        else:
            raise RuntimeError(f"Failed to call Groq API after 3 attempts: {last_exc}")

        elapsed = time.perf_counter() - start
        choice = data["choices"][0]
        content = choice["message"].get("content") or ""
        
        # If model spent all tokens in reasoning and was cut off before emitting content, retry with higher limit
        if choice.get("finish_reason") == "length" and not content.strip():
            payload["max_tokens"] = min(self.max_new_tokens + 1500, 4096)
            req2 = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
            try:
                with urllib.request.urlopen(req2, timeout=40) as resp2:
                    data2 = json.loads(resp2.read().decode('utf-8'))
                    choice = data2["choices"][0]
                    content = choice["message"].get("content") or ""
                    data = data2
            except Exception:
                pass
        
        usage = data.get("usage", {})
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        call_tokens = prompt_tokens + completion_tokens

        # Accounting & update
        self.telemetry[f"{role}_calls"] += 1
        self.telemetry[f"{role}_input_tokens"] += prompt_tokens
        self.telemetry[f"{role}_tokens"] += completion_tokens
        self.telemetry["total_tokens"] += call_tokens
        self.telemetry["seconds"] += elapsed

        call_cost = (prompt_tokens / 1_000_000 * self.cost_per_m_in) + (completion_tokens / 1_000_000 * self.cost_per_m_out)
        self.telemetry["estimated_cost_usd"] += call_cost

        return content

    def generate(self, role: str, system_prompt: str, user_prompt: str, seed: int = 42) -> str:
        return self._call_groq(role, system_prompt, user_prompt)

    def call_coder(self, system_prompt: str, user_prompt: str) -> str:
        return self._call_groq("coder", system_prompt, user_prompt)

    def call_critic(self, system_prompt: str, user_prompt: str) -> str:
        if not self.enable_critic:
            raise RuntimeError("Critic disabled")
        return self._call_groq("critic", system_prompt, user_prompt)

    def get_summary_report(self) -> str:
        t = self.telemetry
        return (
            f"=== GROQ BUDGET & USAGE ACCOUNTING ===\n"
            f"Model: {self.model}\n"
            f"Total API Calls: {t['coder_calls'] + t['critic_calls']} (Coder: {t['coder_calls']}, Critic: {t['critic_calls']})\n"
            f"Total Tokens: {t['total_tokens']:,} / {self.max_total_tokens:,} ({t['total_tokens']/self.max_total_tokens*100:.1f}% of limit)\n"
            f"  - Input Tokens: {t['coder_input_tokens'] + t['critic_input_tokens']:,}\n"
            f"  - Output Tokens: {t['coder_tokens'] + t['critic_tokens']:,}\n"
            f"Estimated Spend: ${t['estimated_cost_usd']:.4f} / ${self.max_budget_usd:.2f}\n"
            f"Total Inference Time: {t['seconds']:.2f}s\n"
            f"====================================="
        )
