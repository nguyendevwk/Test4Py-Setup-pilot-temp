#!/usr/bin/env python3
"""Standalone, Zero-Bias Dual-GPU Test Synthesis & Evaluation Harness.

Completely independent of any specific project, dataset, or legacy codebase.
Works on ANY Python repository, class, or function.

Hardware target: Kaggle Dual-GPU (2x Tesla T4 15GB).
- GPU 0 (cuda:0): Coder Model (e.g. Qwen2.5-Coder-14B-Instruct in 4-bit NF4)
- GPU 1 (cuda:1): Critic/Verifier Model (e.g. Qwen3-4B-Instruct in 4-bit NF4)
"""

import argparse
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

# ==============================================================================
# 1. PURE AST STATE MINER (HOÀN TOÀN ĐỘC LẬP VỚI MỌI REPO)
# ==============================================================================

SETTER_PREFIXES = ('set_', 'add_', 'register_', 'create_', 'build_', 'init_', 'append_', 'put_', 'insert_', 'configure_', 'setup_')

def extract_target_ast(file_path: Path, symbol_name: str):
    """Trích xuất mã nguồn và context của hàm hoặc class bất kỳ từ file Python."""
    source = file_path.read_text(encoding='utf-8')
    tree = ast.parse(source)
    target_node = None
    parent_class = None

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if node.name == symbol_name:
                target_node = node
                break
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)) and sub.name == symbol_name:
                    target_node = sub
                    parent_class = node
                    break
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == symbol_name:
            target_node = node
            break

    if not target_node:
        raise ValueError(f"Symbol '{symbol_name}' không tìm thấy trong {file_path}")

    return {
        'source': ast.get_source_segment(source, target_node) or '',
        'is_method': parent_class is not None,
        'parent_class': parent_class.name if parent_class else None,
        'docstring': ast.get_docstring(target_node) or ''
    }

def mine_candidate_setups(repo_root: Path, target_file: Path, class_name: str = None):
    """Tự động khai phá các chuỗi setup và setter từ class và toàn bộ codebase."""
    candidates = []
    if not class_name:
        return candidates

    tree = ast.parse(target_file.read_text(encoding='utf-8'))
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            init_args = []
            setters = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    if item.name == '__init__':
                        init_args = [a.arg for a in item.args.args if a.arg != 'self']
                    elif item.name.startswith(SETTER_PREFIXES):
                        setters.append(item.name)
            candidates.append({
                'class': class_name,
                'init_args': init_args,
                'setters': setters
            })
    return candidates

def probe_setup_candidate(setup_code: str, timeout: int = 5) -> bool:
    """Kiểm chứng động (Runtime Probe) chuỗi setup trong sandbox cô lập."""
    script = f"""
import sys
try:
{chr(10).join('    ' + line for line in setup_code.splitlines())}
except Exception as e:
    sys.exit(1)
sys.exit(0)
"""
    try:
        proc = subprocess.run([sys.executable, '-c', script], timeout=timeout, capture_output=True)
        return proc.returncode == 0
    except subprocess.TimeoutExpired:
        return False

# ==============================================================================
# 2. STANDALONE DUAL-GPU INFERENCE ENGINE (ZERO EXTERNAL DEPENDENCIES)
# ==============================================================================

class StandaloneDualGPUEngine:
    """Nạp Coder trên GPU 0 và Critic trên GPU 1 bằng 4-bit NF4 Quantization."""
    def __init__(self, coder_model: str, critic_model: str, load_in_4bit: bool = True, temperature: float = 0.7):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        self.temperature = float(temperature)
        self.device_coder = "cuda:0" if torch.cuda.device_count() > 0 else "cpu"
        self.device_critic = "cuda:1" if torch.cuda.device_count() > 1 else self.device_coder

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        ) if load_in_4bit and "cuda" in self.device_coder else None

        print(f"🤖 [Engine] Đang nạp Coder ({coder_model}) trên {self.device_coder}...")
        self.tokenizer_coder = AutoTokenizer.from_pretrained(coder_model, use_fast=True)
        coder_kwargs = {"quantization_config": bnb_config, "device_map": {"": self.device_coder}} if bnb_config else {"device_map": {"": self.device_coder}, "torch_dtype": torch.float16}
        self.model_coder = AutoModelForCausalLM.from_pretrained(coder_model, **coder_kwargs).eval()

        print(f"⚖️ [Engine] Đang nạp Critic ({critic_model}) trên {self.device_critic}...")
        self.tokenizer_critic = AutoTokenizer.from_pretrained(critic_model, use_fast=True)
        critic_kwargs = {"quantization_config": bnb_config, "device_map": {"": self.device_critic}} if bnb_config else {"device_map": {"": self.device_critic}, "torch_dtype": torch.float16}
        self.model_critic = AutoModelForCausalLM.from_pretrained(critic_model, **critic_kwargs).eval()

        self.token_stats = {"in_coder": 0, "out_coder": 0, "in_critic": 0, "out_critic": 0}

    def generate(self, role: str, system_prompt: str, user_prompt: str, max_new_tokens: int = 1536, seed: int = 42) -> str:
        import torch
        torch.manual_seed(seed)
        model = self.model_coder if role == "coder" else self.model_critic
        tokenizer = self.tokenizer_coder if role == "coder" else self.tokenizer_critic
        device = self.device_coder if role == "coder" else self.device_critic

        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
        inputs = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt", return_dict=True).to(device)
        in_len = inputs.input_ids.shape[1]
        self.token_stats[f"in_{role}"] += in_len

        with torch.inference_mode():
            gen_opts = {"max_new_tokens": max_new_tokens, "pad_token_id": tokenizer.eos_token_id}
            if self.temperature > 0.0:
                gen_opts.update({"do_sample": True, "temperature": self.temperature, "top_p": 0.95})
            else:
                gen_opts.update({"do_sample": False})
            outputs = model.generate(**inputs, **gen_opts)

        gen_tokens = outputs[0, in_len:]
        self.token_stats[f"out_{role}"] += len(gen_tokens)
        return tokenizer.decode(gen_tokens, skip_special_tokens=True)

# ==============================================================================
# 3. TEST EXTRACTION & QUALITY EVALUATION (PYTEST + COVERAGE)
# ==============================================================================

def clean_code_block(raw_text: str) -> str:
    """Tách mã Python sạch từ markdown codeblock."""
    if "```python" in raw_text:
        return raw_text.split("```python")[1].split("```")[0].strip()
    elif "```" in raw_text:
        return raw_text.split("```")[1].split("```")[0].strip()
    return raw_text.strip()

def run_test_and_coverage(test_code: str, repo_root: Path, target_module: str, work_dir: Path):
    """Thực thi test bằng pytest và đo branch coverage thật."""
    work_dir.mkdir(parents=True, exist_ok=True)
    test_file = work_dir / "test_synthesized.py"
    test_file.write_text(test_code, encoding="utf-8")

    env = dict(os.environ, PYTHONPATH=str(repo_root))
    pytest_json = work_dir / "pytest_report.json"
    cov_file = work_dir / ".coverage"

    # Chạy pytest có ghi nhận coverage branch
    cmd = [
        sys.executable, "-m", "coverage", "run",
        "--branch", f"--source={target_module}",
        "-m", "pytest",
        "-p", "pytest_jsonreport.plugin",
        f"--json-report-file={pytest_json}",
        str(test_file)
    ]
    env["COVERAGE_FILE"] = str(cov_file)
    proc = subprocess.run(cmd, cwd=repo_root, env=env, capture_output=True, text=True, timeout=60)

    # Đọc kết quả pytest
    pass_count = 0
    total_count = 0
    if pytest_json.exists():
        try:
            report_data = json.loads(pytest_json.read_text())
            pass_count = len([t for t in report_data.get("tests", []) if t.get("outcome") == "passed"])
            total_count = len(report_data.get("tests", []))
        except Exception:
            pass

    # Đọc branch coverage
    branch_pct = 0.0
    if cov_file.exists():
        cov_json = work_dir / "coverage.json"
        subprocess.run([sys.executable, "-m", "coverage", "json", "-o", str(cov_json)], cwd=repo_root, env=env, capture_output=True)
        if cov_json.exists():
            try:
                cdata = json.loads(cov_json.read_text())
                totals = cdata.get("totals", {})
                branch_pct = totals.get("percent_covered", 0.0)
            except Exception:
                pass

    return {
        "exit_code": proc.returncode,
        "pass_count": pass_count,
        "total_count": total_count,
        "branch_pct": branch_pct,
        "stdout": proc.stdout[-2000:],
        "stderr": proc.stderr[-2000:]
    }

# ==============================================================================
# 4. MASTER RUNNER FUNCTION
# ==============================================================================

def run_evaluation(args):
    repo_root = Path(args.repo).resolve()
    target_file = (repo_root / args.file).resolve()
    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"🚀 [Harness] Target: {args.symbol} trong {target_file}")
    info = extract_target_ast(target_file, args.symbol)

    # 1. State Mining
    setup_context = ""
    probe_time = 0.0
    if args.mode in ("ranked", "verified"):
        t0 = time.perf_counter()
        setups = mine_candidate_setups(repo_root, target_file, info.get("parent_class"))
        if setups and args.mode == "verified":
            valid = []
            for s in setups:
                dummy_code = f"from {args.module} import {s['class']}\nobj = {s['class']}()"
                if probe_setup_candidate(dummy_code):
                    valid.append(dummy_code)
            if valid:
                setup_context = valid[0]
        elif setups:
            setup_context = f"# Suggested setup:\nfrom {args.module} import {setups[0]['class']}\nobj = {setups[0]['class']}()"
        probe_time = time.perf_counter() - t0

    # 2. Nạp Engine
    engine = StandaloneDualGPUEngine(
        coder_model=args.coder_model,
        critic_model=args.critic_model,
        load_in_4bit=args.load_in_4bit,
        temperature=args.temperature
    )

    results = []
    for i in range(args.samples):
        sample_seed = args.seed + i
        sample_dir = output_dir / f"sample_{i+1:02d}"
        print(f"\n▶️ [Sample {i+1:02d}/{args.samples}] Seed={sample_seed} Mode={args.mode}...")

        # Prompt Coder
        sys_p = "You are an expert Python test engineer. Write rigorous, self-contained, non-vacuous pytest unit tests for the target code. Avoid empty assertions like `assert True`. Derive assertions strictly from specifications."
        user_p = f"Target Function/Class:\n```python\n{info['source']}\n```\n\nModule: {args.module}\nSymbol: {args.symbol}\n"
        if setup_context:
            user_p += f"\nVerified State Setup Context:\n```python\n{setup_context}\n```\n"

        gen_code = engine.generate("coder", sys_p, user_p, seed=sample_seed)
        clean_code = clean_code_block(gen_code)

        # Chạy kiểm thử lần 1
        eval_res = run_test_and_coverage(clean_code, repo_root, args.module, sample_dir)

        # Critic Repair nếu có lỗi và không phải chế độ no-repair
        repaired = False
        if eval_res["pass_count"] == 0 and not args.no_repair:
            print("  ⚠️ Test trượt ban đầu, gọi Critic sửa lỗi...")
            c_sys = "You are an expert test debugger. Repair the pytest file using the provided failure diagnostics. Preserve testing intent, fix imports or setup state, and do NOT delete assertions."
            c_user = f"Failing Test Code:\n```python\n{clean_code}\n```\n\nDiagnostics:\n{eval_res['stderr'] or eval_res['stdout']}\n\nTarget Source:\n```python\n{info['source']}\n```"
            rep_code = clean_code_block(engine.generate("critic", c_sys, c_user, seed=sample_seed))
            eval_res_rep = run_test_and_coverage(rep_code, repo_root, args.module, sample_dir / "repaired")
            if eval_res_rep["pass_count"] > 0:
                eval_res = eval_res_rep
                clean_code = rep_code
                repaired = True

        (sample_dir / "final_test.py").write_text(clean_code, encoding="utf-8")
        results.append({
            "sample_id": f"sample_{i+1:02d}",
            "pass_count": eval_res["pass_count"],
            "total_count": eval_res["total_count"],
            "branch_pct": eval_res["branch_pct"],
            "repaired_by_critic": repaired
        })
        print(f"  Outcome: {eval_res['pass_count']}/{eval_res['total_count']} passed | Branch Cov: {eval_res['branch_pct']:.2f}% | Critic Repaired: {repaired}")

    summary = {
        "target": f"{args.module}:{args.symbol}",
        "mode": args.mode,
        "samples": args.samples,
        "temperature": args.temperature,
        "probe_time_seconds": probe_time,
        "telemetry": engine.token_stats,
        "results": results
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n✅ Đã lưu tóm tắt tại: {output_dir / 'summary.json'}")

# ==============================================================================
# CLI INTERFACE
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Standalone Universal Dual-GPU Test Harness")
    parser.add_argument("--repo", required=True, help="Root path of target repository")
    parser.add_argument("--file", required=True, help="Relative path to target file (e.g. src/core/manager.py)")
    parser.add_argument("--module", required=True, help="Python import module (e.g. core.manager)")
    parser.add_argument("--symbol", required=True, help="Target function or class name")
    parser.add_argument("--mode", choices=("baseline", "ranked", "verified"), default="verified")
    parser.add_argument("--samples", type=int, default=15)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--coder-model", default="Qwen/Qwen2.5-Coder-14B-Instruct")
    parser.add_argument("--critic-model", default="Qwen/Qwen3-4B-Instruct-2507")
    parser.add_argument("--load-in-4bit", action="store_true", default=True)
    parser.add_argument("--no-repair", action="store_true")
    parser.add_argument("--output", default="/kaggle/working/UNIVERSAL_TEST_RUN")
    args = parser.parse_args()

    run_evaluation(args)

if __name__ == '__main__':
    main()
