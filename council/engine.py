"""Multi-GPU Council Engine managing Coder (GPU 0) and Critic (GPU 1)."""
import os
import time
from typing import Dict, Any, Optional

class CouncilEngine:
    """Orchestrates 2-GPU Council collaboration for test generation and repair."""

    def __init__(
        self,
        coder_model: str = "Qwen/Qwen2.5-Coder-7B-Instruct",
        critic_model: str = "Qwen/Qwen3-4B-Instruct-2507",
        coder_device: Optional[str] = None,
        critic_device: Optional[str] = None,
        max_new_tokens: int = 1536,
        mock: bool = False,
    ):
        self.mock = mock
        self.coder_model_name = coder_model
        self.critic_model_name = critic_model
        self.max_new_tokens = max_new_tokens
        self.telemetry = {
            "coder_calls": 0,
            "critic_calls": 0,
            "coder_tokens": 0,
            "critic_tokens": 0,
            "coder_seconds": 0.0,
            "critic_seconds": 0.0,
        }

        if mock:
            self.coder_device = "cpu"
            self.critic_device = "cpu"
            self.coder_model = None
            self.coder_tokenizer = None
            self.critic_model = None
            self.critic_tokenizer = None
            return

        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        num_gpus = torch.cuda.device_count()
        if coder_device is None:
            self.coder_device = "cuda:0" if num_gpus >= 1 else "cpu"
        else:
            self.coder_device = coder_device

        if critic_device is None:
            self.critic_device = "cuda:1" if num_gpus >= 2 else (self.coder_device)
        else:
            self.critic_device = critic_device

        print(f"[Council] Initializing Dual-Engine:")
        print(f"  - Coder Model  : {self.coder_model_name} on {self.coder_device}")
        print(f"  - Critic Model : {self.critic_model_name} on {self.critic_device}")

        # 1. Load Coder (GPU 0)
        t0 = time.perf_counter()
        self.coder_tokenizer = AutoTokenizer.from_pretrained(self.coder_model_name, use_fast=True)
        dtype_coder = torch.float16 if "cuda" in self.coder_device else torch.float32
        self.coder_model = AutoModelForCausalLM.from_pretrained(
            self.coder_model_name,
            torch_dtype=dtype_coder,
            device_map={"": self.coder_device}
        ).eval()
        print(f"  ✓ Coder loaded in {time.perf_counter() - t0:.2f}s")

        # 2. Load Critic (GPU 1 or fallback)
        t1 = time.perf_counter()
        self.critic_tokenizer = AutoTokenizer.from_pretrained(self.critic_model_name, use_fast=True)
        dtype_critic = torch.float16 if "cuda" in self.critic_device else torch.float32
        self.critic_model = AutoModelForCausalLM.from_pretrained(
            self.critic_model_name,
            torch_dtype=dtype_critic,
            device_map={"": self.critic_device}
        ).eval()
        print(f"  ✓ Critic loaded in {time.perf_counter() - t1:.2f}s")

    def call_coder(self, system_prompt: str, user_prompt: str) -> str:
        """Execute inference on Coder model (GPU 0)."""
        if self.mock:
            self.telemetry["coder_calls"] += 1
            return "```python\ndef test_mock():\n    assert True\n```"

        import torch
        t0 = time.perf_counter()
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
        inputs = self.coder_tokenizer.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
        ).to(self.coder_device)

        with torch.no_grad():
            outputs = self.coder_model.generate(
                inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,
                pad_token_id=self.coder_tokenizer.eos_token_id,
            )
        generated_ids = outputs[0][inputs.shape[1]:]
        text = self.coder_tokenizer.decode(generated_ids, skip_special_tokens=True)
        dt = time.perf_counter() - t0

        self.telemetry["coder_calls"] += 1
        self.telemetry["coder_tokens"] += len(generated_ids)
        self.telemetry["coder_seconds"] += dt
        return text

    def call_critic(self, system_prompt: str, user_prompt: str) -> str:
        """Execute inference on Critic model (GPU 1)."""
        if self.mock:
            self.telemetry["critic_calls"] += 1
            return "```python\ndef test_mock_repaired():\n    assert True\n```"

        import torch
        t0 = time.perf_counter()
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
        inputs = self.critic_tokenizer.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
        ).to(self.critic_device)

        with torch.no_grad():
            outputs = self.critic_model.generate(
                inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,
                pad_token_id=self.critic_tokenizer.eos_token_id,
            )
        generated_ids = outputs[0][inputs.shape[1]:]
        text = self.critic_tokenizer.decode(generated_ids, skip_special_tokens=True)
        dt = time.perf_counter() - t0

        self.telemetry["critic_calls"] += 1
        self.telemetry["critic_tokens"] += len(generated_ids)
        self.telemetry["critic_seconds"] += dt
        return text
