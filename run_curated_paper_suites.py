#!/usr/bin/env python3
"""Run benchmark across 5 curated real suites from Test4Py paper with Groq Engine."""
import json
import shutil
import time
from pathlib import Path

from council.groq_engine import GroqCouncilEngine
from council_multitarget import run_single_evaluation

BASE_DIR = Path(__file__).resolve().parent
REPOS_DIR = BASE_DIR / "local_benchmark_repos"
OUT_BASE = BASE_DIR / "paper_curated_eval"

PAPER_SUITES = [
    {
        "id": "genty_repeat",
        "suite_name": "genty (Box Test Suite)",
        "category": "Decorator / Param",
        "project": "genty",
        "module": "genty.genty_repeat",
        "file": "genty/genty_repeat.py",
        "symbol": "genty_repeat",
        "setup_hint": "from genty.genty_repeat import genty_repeat\ncount = 3\ndec = genty_repeat(count)"
    },
    {
        "id": "codetiming_timer",
        "suite_name": "codetiming (Real Python)",
        "category": "Context Manager",
        "project": "codetiming",
        "module": "codetiming._timer",
        "file": "codetiming/_timer.py",
        "symbol": "Timer",
        "setup_hint": "from codetiming import Timer\nt = Timer(name='perf', text='Elapsed: {:0.4f}s')\nt.start()"
    },
    {
        "id": "docstring_parser_parse",
        "suite_name": "docstring_parser",
        "category": "Type-rich AST",
        "project": "docstring_parser",
        "module": "docstring_parser.parser",
        "file": "docstring_parser/parser.py",
        "symbol": "parse",
        "setup_hint": "sample_doc = \"\"\"Summary line.\n\n:param name: param desc\n:type name: str\n:returns: return desc\n\"\"\""
    },
    {
        "id": "woa_whale_opt",
        "suite_name": "woa (Optimization Algo)",
        "category": "Numerical / Numpy",
        "project": "woa",
        "module": "src.whale_optimization",
        "file": "src/whale_optimization.py",
        "symbol": "WhaleOptimization",
        "setup_hint": "from src.whale_optimization import WhaleOptimization\nwoa = WhaleOptimization(opt_func=lambda x: sum(i**2 for i in x), constraints=[(-5, 5), (-5, 5)], nsols=5, b=1, a=2, a_step=0.1)"
    },
    {
        "id": "superstring",
        "suite_name": "superstring.py",
        "category": "Data Structure",
        "project": "superstring.py",
        "module": "superstring.superstring",
        "file": "superstring/superstring.py",
        "symbol": "SuperString",
        "setup_hint": "from superstring.superstring import SuperString\ns = SuperString('Test String For Python Testing')"
    }
]

def main():
    if OUT_BASE.exists():
        shutil.rmtree(OUT_BASE)
    OUT_BASE.mkdir(exist_ok=True)
    
    engine = GroqCouncilEngine(
        model="openai/gpt-oss-20b",
        max_new_tokens=2500,
        max_total_tokens=1_000_000,
        max_budget_usd=5.0
    )
    
    print("=" * 80)
    print("CHẠY ĐỐI CHUẨN TRÊN 5 BỘ SUITE THẬT TỪ BÀI BÁO TEST4PY")
    print("=" * 80)
    
    results = []
    for s in PAPER_SUITES:
        target_out = OUT_BASE / s["id"]
        target_out.mkdir(exist_ok=True)
        repo_root = REPOS_DIR / s["project"]
        
        t0 = time.perf_counter()
        res = run_single_evaluation(
            target=s,
            arm="ranked",
            sample_idx=0,
            engine=engine,
            repo_root=repo_root,
            out_dir=target_out,
            seed=42,
            repair_with="critic"
        )
        elapsed = time.perf_counter() - t0
        
        line_pct = res.get("line_pct")
        branch_pct = res.get("branch_pct")
        line_str = f"{line_pct:.2f}%" if line_pct is not None else "0.00%"
        branch_str = f"{branch_pct:.2f}%" if branch_pct is not None else "0.00%"
        
        rec = {
            "suite": s["suite_name"],
            "category": s["category"],
            "symbol": s["symbol"],
            "first_pass": res.get("first_pass", False),
            "suite_pass": res.get("suite_pass", False),
            "line_pct": line_pct if line_pct is not None else 0.0,
            "branch_pct": branch_pct if branch_pct is not None else 0.0,
            "latency": round(elapsed, 2)
        }
        results.append(rec)
        print(f"{s['suite_name']:28} | Pass: {str(rec['suite_pass']):5} | Line: {line_str:7} | Branch: {branch_str:7} | Time: {elapsed:.2f}s")
        
    summary_path = OUT_BASE / "curated_summary.json"
    summary_path.write_text(json.dumps(results, indent=2))
    
    print("\n" + "=" * 80)
    print(engine.get_summary_report())
    print("=" * 80)

if __name__ == "__main__":
    main()
