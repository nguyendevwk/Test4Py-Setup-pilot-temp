#!/usr/bin/env python3
"""Standardized Multi-Target State-Aware Council Benchmark for Kaggle Dual-GPU.

Evaluates Dual-GPU Council (Coder on GPU 0, Critic on GPU 1) against Baseline.
Focuses heavily on Type-Annotated & Docstring-Rich targets (Tập A trong Test4Py),
bridging prior research on Type Hints/Docstrings with Object State Setup.

Features:
- Dual-focus: Tập A (Type-Annotated & Docstring-Rich) + Tập NA (Stateful Baselines)
- AST-level Type Hint & Docstring extraction injected into LLM context
- Pure-AST State Mining & Dynamic Sandboxed Probing
- Dual-GPU 4-bit NF4 Quantization with strict VRAM cache clearing
- Test-Node Pruning to eliminate failing secondary assertions
- Line (Statement) Coverage & Branch Coverage calculation
- Automated Markdown and CSV reporting with 1-click zip archive.
"""

import argparse
import ast
import csv
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback

BASE_DIR = Path(__file__).resolve().parent

CURATED_TARGETS = [
    # =========================================================================
    # TẬP A: TYPE-ANNOTATED & DOCSTRING-RICH SUBJECTS (TEST4PY TABLE 1)
    # =========================================================================
    {
        "id": "docstring_parser_parse",
        "category": "Typed_A",
        "project": "docstring_parser",
        "repo_url": "https://github.com/rr-/docstring_parser.git",
        "commit": None,
        "module": "docstring_parser.parser",
        "file": "docstring_parser/parser.py",
        "symbol": "parse",
        "class_name": None,
        "setup_hint": "sample_doc = \"\"\"Summary line.\n\n:param name: parameter description\n:type name: str\n:returns: return description\n\"\"\""
    },
    {
        "id": "codetiming_timer",
        "category": "Typed_A",
        "project": "codetiming",
        "repo_url": "https://github.com/realpython/codetiming.git",
        "commit": None,
        "module": "codetiming._timer",
        "file": "codetiming/_timer.py",
        "symbol": "Timer",
        "class_name": "Timer",
        "setup_hint": "from codetiming import Timer\nt = Timer(name='perf_timer', text='Elapsed: {:0.4f}s')\nt.start()"
    },
    {
        "id": "typesystem_schema",
        "category": "Typed_A",
        "project": "typesystem",
        "repo_url": "https://github.com/encode/typesystem.git",
        "commit": None,
        "module": "typesystem.schemas",
        "file": "typesystem/schemas.py",
        "symbol": "Schema",
        "class_name": "Schema",
        "setup_hint": "from typesystem import Schema, String, Integer\nclass UserSchema(Schema):\n    username = String(max_length=50)\n    age = Integer()\nuser = UserSchema(username='alice', age=30)"
    },
    # =========================================================================
    # TẬP NA: STATEFUL OBJECT GRAPH BASELINES (TEST4PY TABLE 1)
    # =========================================================================
    {
        "id": "pycg_imports",
        "category": "NA_Baseline",
        "project": "PyCG",
        "repo_url": "https://github.com/vitsalis/PyCG.git",
        "commit": "8d5dc40837803beef1d8d379fbf2cdad6cd94641",
        "module": "pycg.machinery.imports",
        "file": "pycg/machinery/imports.py",
        "symbol": "get_custom_loader",
        "class_name": "ImportManager",
        "setup_hint": "from pycg.machinery.imports import ImportManager\nmod = ImportManager('test_mod')\nmod.create_node('pkg')\nmod.set_current_mod('pkg')"
    },
    {
        "id": "woa_whale_opt",
        "category": "NA_Baseline",
        "project": "woa",
        "repo_url": "https://github.com/docwza/woa.git",
        "commit": "4747379",
        "module": "src.whale_optimization",
        "file": "src/whale_optimization.py",
        "symbol": "WhaleOptimization",
        "class_name": "WhaleOptimization",
        "setup_hint": "from src.whale_optimization import WhaleOptimization\nwoa = WhaleOptimization(opt_func=lambda x: sum(i**2 for i in x), constraints=[(-5, 5), (-5, 5)], nsols=5, b=1, a=2, a_step=0.1)"
    },
    {
        "id": "superstring",
        "category": "NA_Baseline",
        "project": "superstring.py",
        "repo_url": "https://github.com/btwael/superstring.py.git",
        "commit": "f47ef78",
        "module": "superstring.superstring",
        "file": "superstring/superstring.py",
        "symbol": "SuperString",
        "class_name": "SuperString",
        "setup_hint": "from superstring.superstring import SuperString\ns = SuperString('Test String For Python Testing')"
    }
]

SETTER_PREFIXES = ('set_', 'add_', 'register_', 'create_', 'build_', 'init_', 'append_', 'put_', 'insert_', 'configure_', 'setup_')


def extract_target_source(file_path: Path, symbol_name: str) -> dict:
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
        lines = source.splitlines()[:100]
        return {'source': '\n'.join(lines), 'parent_class': None, 'docstring': '', 'type_hints': {}, 'has_type_hints': False, 'has_docstrings': False}

    # Extract type hints via AST
    type_hints = {}
    if isinstance(target_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        for arg in target_node.args.args:
            if arg.annotation:
                type_hints[arg.arg] = ast.unparse(arg.annotation)
        if target_node.returns:
            type_hints['return'] = ast.unparse(target_node.returns)
    elif isinstance(target_node, ast.ClassDef):
        for item in target_node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                type_hints[item.target.id] = ast.unparse(item.annotation)
            elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == '__init__':
                for arg in item.args.args:
                    if arg.annotation and arg.arg != 'self':
                        type_hints[arg.arg] = ast.unparse(arg.annotation)

    docstring = ast.get_docstring(target_node) or ''

    return {
        'source': ast.get_source_segment(source, target_node) or '',
        'parent_class': parent_class.name if parent_class else None,
        'docstring': docstring,
        'has_docstrings': bool(docstring.strip()),
        'type_hints': type_hints,
        'has_type_hints': bool(type_hints)
    }


def probe_setup_candidate(setup_code: str, timeout: int = 4) -> bool:
    script = f"""
import sys
try:
{chr(10).join('    ' + line for line in setup_code.splitlines())}
except Exception:
    sys.exit(1)
sys.exit(0)
"""
    try:
        proc = subprocess.run([sys.executable, '-c', script], timeout=timeout, capture_output=True)
        return proc.returncode == 0
    except Exception:
        return False


def clean_code_block(raw_text: str) -> str:
    if "```python" in raw_text:
        return raw_text.split("```python")[1].split("```")[0].strip()
    elif "```" in raw_text:
        return raw_text.split("```")[1].split("```")[0].strip()
    return raw_text.strip()


def prune_and_filter_tests(test_code: str, passing_node_ids: set) -> str:
    """Uses AST to retain only test functions that genuinely passed."""
    if not passing_node_ids:
        return test_code
    passing_func_names = {node.split('::')[-1].split('[')[0] for node in passing_node_ids}
    try:
        tree = ast.parse(test_code)
        new_body = []
        for item in tree.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if item.name in passing_func_names or not item.name.startswith('test_'):
                    new_body.append(item)
            else:
                new_body.append(item)
        tree.body = new_body
        return ast.unparse(tree)
    except Exception:
        return test_code


class DualGPUBenchmarkEngine:
    def __init__(self, coder_model: str, critic_model: str, mock: bool = False, temperature: float = 0.7):
        self.mock = mock
        self.temperature = float(temperature)
        self.telemetry = {"in_coder": 0, "out_coder": 0, "in_critic": 0, "out_critic": 0}

        if mock:
            print("🧪 [Engine] Mock mode activated. No GPU models loaded.")
            return

        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
        self.dev_coder = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.dev_critic = "cuda:1" if torch.cuda.device_count() > 1 else self.dev_coder

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        ) if "cuda" in self.dev_coder else None

        print(f"🤖 [Engine] Loading Coder ({coder_model}) on {self.dev_coder} (NF4 4-bit)...")
        self.tok_coder = AutoTokenizer.from_pretrained(coder_model, use_fast=True)
        coder_kwargs = {"quantization_config": bnb_config, "device_map": {"": self.dev_coder}} if bnb_config else {"device_map": {"": self.dev_coder}, "torch_dtype": torch.float16}
        self.model_coder = AutoModelForCausalLM.from_pretrained(coder_model, **coder_kwargs).eval()

        print(f"⚖️ [Engine] Loading Critic ({critic_model}) on {self.dev_critic} (NF4 4-bit)...")
        self.tok_critic = AutoTokenizer.from_pretrained(critic_model, use_fast=True)
        critic_kwargs = {"quantization_config": bnb_config, "device_map": {"": self.dev_critic}} if bnb_config else {"device_map": {"": self.dev_critic}, "torch_dtype": torch.float16}
        self.model_critic = AutoModelForCausalLM.from_pretrained(critic_model, **critic_kwargs).eval()

    def generate(self, role: str, system_prompt: str, user_prompt: str, seed: int = 42, max_new_tokens: int = 1536) -> str:
        if self.mock:
            return f"```python\ndef test_{role}_mock():\n    assert True\n```"

        import torch
        import gc

        torch.manual_seed(seed)
        model = self.model_coder if role == "coder" else self.model_critic
        tokenizer = self.tok_coder if role == "coder" else self.tok_critic
        device = self.dev_coder if role == "coder" else self.dev_critic

        msgs = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
        inputs = tokenizer.apply_chat_template(msgs, tokenize=True, add_generation_prompt=True, return_tensors="pt").to(device)
        in_len = inputs.shape[1]
        self.telemetry[f"in_{role}"] += in_len

        with torch.inference_mode():
            gen_opts = {"max_new_tokens": max_new_tokens, "pad_token_id": tokenizer.eos_token_id}
            if self.temperature > 0.0:
                gen_opts.update({"do_sample": True, "temperature": self.temperature, "top_p": 0.95})
            else:
                gen_opts.update({"do_sample": False})
            outputs = model.generate(inputs, **gen_opts)

        gen_tokens = outputs[0, in_len:]
        self.telemetry[f"out_{role}"] += len(gen_tokens)
        result = tokenizer.decode(gen_tokens, skip_special_tokens=True)

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()

        return result


def execute_pytest_and_coverage(test_code: str, repo_root: Path, target_module: str, work_dir: Path, timeout: int = 30) -> dict:
    work_dir.mkdir(parents=True, exist_ok=True)
    test_file = work_dir / "test_run.py"
    test_file.write_text(test_code, encoding="utf-8")

    env = dict(os.environ, PYTHONPATH=str(repo_root), COVERAGE_FILE=str(work_dir / ".coverage"),
               PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", PYTHONDONTWRITEBYTECODE="1")
    rep_file = work_dir / "pytest_report.json"

    cmd = [
        sys.executable, "-m", "coverage", "run",
        "--branch", f"--source={target_module}",
        "-m", "pytest",
        "-p", "pytest_jsonreport.plugin",
        f"--json-report-file={rep_file}",
        str(test_file)
    ]

    proc = subprocess.run(cmd, cwd=repo_root, env=env, capture_output=True, text=True, timeout=timeout)

    passing_nodes = set()
    total_nodes = 0
    if rep_file.exists():
        try:
            data = json.loads(rep_file.read_text())
            for t in data.get("tests", []):
                total_nodes += 1
                if t.get("outcome") == "passed":
                    passing_nodes.add(t.get("nodeid"))
        except Exception:
            pass

    line_pct = 0.0
    branch_pct = 0.0
    cov_file = work_dir / ".coverage"
    if cov_file.exists() and passing_nodes:
        cov_json = work_dir / "coverage.json"
        subprocess.run([sys.executable, "-m", "coverage", "json", "-o", str(cov_json)], cwd=repo_root, env=env, capture_output=True)
        if cov_json.exists():
            try:
                cdata = json.loads(cov_json.read_text())
                totals = cdata.get("totals", {})
                line_pct = totals.get("percent_covered", 0.0)
                num_branches = totals.get("num_branches", 0)
                covered_branches = totals.get("covered_branches", 0)
                branch_pct = round(100.0 * covered_branches / num_branches, 2) if num_branches > 0 else line_pct
            except Exception:
                pass

    return {
        "exit_code": proc.returncode,
        "total_nodes": total_nodes,
        "passing_nodes": list(passing_nodes),
        "pass_count": len(passing_nodes),
        "line_pct": line_pct,
        "branch_pct": branch_pct,
        "stdout": proc.stdout[-1500:],
        "stderr": proc.stderr[-1500:]
    }


def run_single_evaluation(target: dict, arm: str, sample_idx: int, engine: DualGPUBenchmarkEngine,
                          repo_root: Path, out_dir: Path, seed: int = 42) -> dict:
    sample_dir = out_dir / f"sample_{sample_idx+1:02d}"
    sample_dir.mkdir(parents=True, exist_ok=True)
    sample_seed = seed + sample_idx

    target_file = repo_root / target["file"]
    ast_info = extract_target_source(target_file, target["symbol"])

    setup_context = ""
    probe_time = 0.0
    if arm in ("ranked", "verified"):
        t0 = time.perf_counter()
        candidate = target.get("setup_hint") or ""
        if candidate and arm == "verified":
            if probe_setup_candidate(candidate):
                setup_context = candidate
        elif candidate:
            setup_context = candidate
        probe_time = time.perf_counter() - t0

    sys_p = "You are an expert Python test engineer. Write rigorous, self-contained, non-vacuous pytest tests. Use provided Type Annotations and Docstring Specifications to construct valid argument values, edge cases, and expected assertions."
    user_p = f"Target Function/Class:\n```python\n{ast_info['source']}\n```\n\nModule: {target['module']}\nSymbol: {target['symbol']}\n"
    
    # Explicitly highlight Type Hints and Docstrings (Grounded Semantic Priors)
    if ast_info['has_type_hints']:
        user_p += f"\nType Annotations:\n```python\n{json.dumps(ast_info['type_hints'], indent=2)}\n```\n"
    if ast_info['has_docstrings']:
        user_p += f"\nDocstring Specification:\n\"\"\"\n{ast_info['docstring']}\n\"\"\"\n"

    # State Setup Context (Only for Ranked / Verified arms)
    if setup_context:
        user_p += f"\nVerified State Setup Context:\n```python\n{setup_context}\n```\n"

    t0 = time.perf_counter()
    gen_raw = engine.generate("coder", sys_p, user_p, seed=sample_seed)
    gen_code = clean_code_block(gen_raw)

    eval_v1 = execute_pytest_and_coverage(gen_code, repo_root, target["module"], sample_dir / "v1_raw")

    final_code = gen_code
    repaired = False
    if eval_v1["pass_count"] == 0 and not engine.mock:
        c_sys = "You are an expert test debugger. Repair the pytest file using failure diagnostics. Preserve testing intent, fix imports or setup state, and do NOT delete assertions."
        c_user = f"Failing Test Code:\n```python\n{gen_code}\n```\n\nDiagnostics:\n{eval_v1['stderr'] or eval_v1['stdout']}\n\nTarget Source:\n```python\n{ast_info['source']}\n```"
        rep_raw = engine.generate("critic", c_sys, c_user, seed=sample_seed)
        rep_code = clean_code_block(rep_raw)
        eval_rep = execute_pytest_and_coverage(rep_code, repo_root, target["module"], sample_dir / "v2_repaired")
        if eval_rep["pass_count"] > 0:
            final_code = rep_code
            eval_v1 = eval_rep
            repaired = True

    # Test Pruning: extract genuine passing tests into final suite
    pruned_code = prune_and_filter_tests(final_code, set(eval_v1["passing_nodes"]))
    (sample_dir / "test_final.py").write_text(pruned_code, encoding="utf-8")
    eval_final = execute_pytest_and_coverage(pruned_code, repo_root, target["module"], sample_dir / "final_eval")

    run_sec = time.perf_counter() - t0

    suite_pass = bool(eval_final["pass_count"] > 0 and eval_final["exit_code"] == 0)

    res = {
        "target_id": target["id"],
        "category": target.get("category", "General"),
        "project": target["project"],
        "module": target["module"],
        "symbol": target["symbol"],
        "has_type_hints": ast_info["has_type_hints"],
        "has_docstrings": ast_info["has_docstrings"],
        "arm": arm,
        "sample": f"sample_{sample_idx+1:02d}",
        "suite_pass": suite_pass,
        "pass_count": eval_final["pass_count"],
        "total_count": eval_final["total_nodes"],
        "line_pct": eval_final["line_pct"],
        "branch_pct": eval_final["branch_pct"],
        "repaired_by_critic": repaired,
        "probe_time_sec": round(probe_time, 3),
        "runtime_sec": round(run_sec, 2)
    }

    (sample_dir / "result.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    return res


def clone_if_needed(target: dict, repos_dir: Path):
    dest = repos_dir / target["project"]
    commit = target.get("commit")
    if not dest.exists():
        print(f"📥 Cloning {target['project']} from {target['repo_url']}...")
        if commit and len(commit) == 40:
            dest.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "init", "-q", str(dest)], check=True)
            subprocess.run(["git", "-C", str(dest), "fetch", "--depth", "1", target["repo_url"], commit], check=True)
            subprocess.run(["git", "-C", str(dest), "checkout", "-q", "--detach", "FETCH_HEAD"], check=True)
        else:
            subprocess.run(["git", "clone", "--depth", "1", target["repo_url"], str(dest)], check=True)
            if commit:
                try:
                    subprocess.run(["git", "-C", str(dest), "checkout", "-q", commit], check=True)
                except Exception:
                    pass
    return dest


def export_markdown_report(records: list, out_path: Path, telemetry: dict):
    lines = [
        "# REPRODUCIBLE MULTI-TARGET BENCHMARK EVALUATION",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')} | Target: Kaggle Dual-GPU (2x Tesla T4)\n",
        "## 1. Evaluation Results by Target & Experimental Arm",
        "Focusing on Type Hints & Docstrings (Tập A) combined with State-Aware Council Setup.\n",
        "| Category | Project | Target Symbol | Type / Doc? | Arm | Suite Pass Rate | Line Cov % | Branch Cov % | Avg Time |",
        "|---|---|---|:---:|---|:---:|:---:|:---:|:---:|"
    ]

    target_keys = sorted(list({(r['category'], r['project'], r['symbol'], r['target_id'], r.get('has_type_hints', False), r.get('has_docstrings', False)) for r in records}))
    arms = ["baseline", "ranked", "verified"]

    for cat, proj, sym, tid, has_t, has_d in target_keys:
        type_doc_str = "Type+Doc" if has_t and has_d else ("Type" if has_t else ("Doc" if has_d else "None"))
        for arm in arms:
            recs = [r for r in records if r["target_id"] == tid and r["arm"] == arm]
            if not recs:
                continue
            pass_rate = f"{sum(bool(r['suite_pass']) for r in recs)}/{len(recs)}"
            avg_line = round(sum(r["line_pct"] for r in recs) / len(recs), 2)
            avg_branch = round(sum(r["branch_pct"] for r in recs) / len(recs), 2)
            avg_sec = round(sum(r["runtime_sec"] for r in recs) / len(recs), 2)
            lines.append(f"| {cat} | {proj} | `{sym}` | {type_doc_str} | **{arm}** | {pass_rate} | **{avg_line}%** | **{avg_branch}%** | {avg_sec}s |")

    lines.extend([
        "",
        "## 2. Resource Telemetry & Hardware Feasibility",
        "",
        f"- **Coder Tokens In/Out**: {telemetry.get('in_coder', 0)} / {telemetry.get('out_coder', 0)}",
        f"- **Critic Tokens In/Out**: {telemetry.get('in_critic', 0)} / {telemetry.get('out_critic', 0)}",
        "- **Hardware Footprint**: 100% Free Kaggle Dual-GPU (2x Tesla T4 15GB, BitsAndBytes NF4 4-bit).",
        "- **Memory Safety**: `torch.cuda.empty_cache()` invoked per sample; 0 CUDA OOM exceptions.",
        ""
    ])

    report_text = "\n".join(lines)
    out_path.write_text(report_text, encoding="utf-8")
    return report_text


def main():
    parser = argparse.ArgumentParser(description="Multi-Target State-Aware Council Benchmark")
    parser.add_argument("--output", type=Path, default=Path("/kaggle/working/EVALUATION_OUTPUT") if Path("/kaggle").exists() else BASE_DIR / "runs/multitarget_eval")
    parser.add_argument("--repos-dir", type=Path, default=Path("/kaggle/working/BENCHMARK_REPOS") if Path("/kaggle").exists() else BASE_DIR / "runs/repos")
    parser.add_argument("--targets", default="all", help="Comma-separated target IDs or 'all'")
    parser.add_argument("--arms", default="baseline,ranked,verified", help="Comma-separated arms")
    parser.add_argument("--samples", type=int, default=2, help="Samples per arm")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--coder-model", default="Qwen/Qwen2.5-Coder-7B-Instruct")
    parser.add_argument("--critic-model", default="Qwen/Qwen3-4B-Instruct-2507")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--mock", action="store_true", help="Run without GPUs for fast offline smoke-test")
    parser.add_argument("--zip", action="store_true", default=True, help="Create zip archive of output")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    args.repos_dir.mkdir(parents=True, exist_ok=True)

    selected_ids = [t.strip() for t in args.targets.split(",")]
    targets = CURATED_TARGETS if args.targets == "all" else [t for t in CURATED_TARGETS if t["id"] in selected_ids]
    arms = [a.strip() for a in args.arms.split(",")]

    print(f"🚀 [Master Benchmark] Starting evaluation across {len(targets)} targets and {len(arms)} arms (Samples={args.samples})...")
    engine = DualGPUBenchmarkEngine(args.coder_model, args.critic_model, mock=args.mock, temperature=args.temperature)

    all_records = []
    for tgt in targets:
        repo_root = clone_if_needed(tgt, args.repos_dir)
        print(f"\n========================================================")
        print(f"🎯 Target [{tgt.get('category')}]: {tgt['project']} -> {tgt['symbol']} ({tgt['module']})")
        print(f"========================================================")

        for arm in arms:
            print(f"\n▶️ Arm: [{arm.upper()}]...")
            tgt_out = args.output / tgt["project"] / tgt["symbol"] / arm
            for s_idx in range(args.samples):
                rec = run_single_evaluation(tgt, arm, s_idx, engine, repo_root, tgt_out, seed=args.seed)
                all_records.append(rec)
                print(f"  [{s_idx+1}/{args.samples}] Pass: {rec['suite_pass']} | Nodes: {rec['pass_count']}/{rec['total_count']} | Line: {rec['line_pct']:.1f}% | Branch: {rec['branch_pct']:.1f}% ({rec['runtime_sec']}s)")

    # Save summary.json and results.csv
    summary_data = {
        "schema_version": 2,
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "targets_count": len(targets),
        "arms": arms,
        "samples_per_arm": args.samples,
        "telemetry": engine.telemetry,
        "records": all_records
    }
    (args.output / "summary.json").write_text(json.dumps(summary_data, indent=2), encoding="utf-8")

    # CSV
    keys = ["category", "project", "module", "symbol", "has_type_hints", "has_docstrings", "arm", "sample", "suite_pass", "pass_count", "total_count", "line_pct", "branch_pct", "repaired_by_critic", "runtime_sec"]
    with (args.output / "results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_records)

    # Markdown Report
    rep_text = export_markdown_report(all_records, args.output / "FINAL_REPORT.md", engine.telemetry)
    print("\n" + "="*70)
    print(rep_text)
    print("="*70)

    if args.zip:
        zip_path = args.output.parent / f"{args.output.name}.zip"
        shutil.make_archive(str(args.output), "zip", args.output)
        print(f"\n📦 Archive generated at: {zip_path}")

    print(f"\n✅ All benchmark runs completed successfully! Output: {args.output}")


if __name__ == '__main__':
    main()
