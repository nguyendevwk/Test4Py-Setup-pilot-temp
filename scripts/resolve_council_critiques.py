#!/usr/bin/env python3
"""Resolves all 3 critiques raised by the Expert Review Committee:

1. Refines docstring_parser_numpydoc grounding (fixes doc.summary -> doc.short_description) and re-evaluates across 5 seeds.
2. Refines genty_dataset parameter unpacking and re-evaluates across 5 seeds.
3. Performs a 5-round repeated execution stress test across ALL 21 Golden Curated Test Suites to measure Flake Rate.
"""

import ast
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from council.groq_engine import GroqCouncilEngine
from pilot.multitarget import execute_pytest_and_coverage
from run_sota_curated_benchmark import (
    TARGETS, SYMBOL_GROUNDING_MAP, generate_sota_coder_test,
    repair_sota_with_critic, SEEDS, OUT_DIR, REPOS_DIR
)

BASE_DIR = Path(__file__).resolve().parents[1]
GOLDEN_DIR = BASE_DIR / "monograph_final_deliverables" / "golden_suites"

# 1. Update Grounding for docstring_parser & genty
SYMBOL_GROUNDING_MAP["docstring_parser"] += (
    "\n- CRITICAL: Docstring objects do NOT have a '.summary' attribute!\n"
    "  Use `doc.short_description` for the summary line, and `doc.long_description` for the extended body."
)

SYMBOL_GROUNDING_MAP["genty"] += (
    "\n- CRITICAL: For `@genty_dataset`, define the test method with explicit parameters matching the dataset tuples:\n"
    "  `@genty_dataset(('val1', 'val2'), ('val3', 'val4'))\n"
    "  def test_method(self, arg1, arg2): ...`"
)

def re_evaluate_refined_targets():
    print("=" * 70)
    print("ACTION 1 & 2: RE-EVALUATING NUMPYDOC & GENTY_DATASET WITH REFINED GROUNDING")
    print("=" * 70)

    engine = GroqCouncilEngine(model="openai/gpt-oss-20b", max_budget_usd=1.0)
    
    refined_targets = [t for t in TARGETS if t["id"] in ("docstring_parser_numpydoc", "genty_dataset")]
    results = {}

    for target in refined_targets:
        tid = target["id"]
        print(f"\n[*] Evaluating Refined Target: {tid}")
        passes = 0
        covs = []

        for seed in SEEDS:
            work_dir = OUT_DIR / "runs_refined" / tid / f"seed_{seed}"
            if work_dir.exists():
                shutil.rmtree(work_dir)
            work_dir.mkdir(parents=True, exist_ok=True)

            code_v1 = generate_sota_coder_test(engine, target, seed)
            (work_dir / "test_v1.py").write_text(code_v1)

            rep1 = execute_pytest_and_coverage(code_v1, str(target["repo_dir"]), target["module"], str(work_dir / "eval_v1"))
            first_pass = bool(rep1.get("suite_pass", False))
            final_pass = first_pass
            final_code = code_v1
            curr_rep = rep1

            if not first_pass:
                prev_code = code_v1
                prev_rep = rep1
                for r in [1, 2]:
                    tb_log = (prev_rep.get("stdout") or "") + "\n" + (prev_rep.get("stderr") or "")
                    code_rep = repair_sota_with_critic(engine, target, prev_code, tb_log[-4000:], r)
                    (work_dir / f"test_r{r}.py").write_text(code_rep)
                    rep_res = execute_pytest_and_coverage(code_rep, str(target["repo_dir"]), target["module"], str(work_dir / f"eval_r{r}"))
                    if rep_res.get("suite_pass", False):
                        final_pass = True
                        final_code = code_rep
                        curr_rep = rep_res
                        print(f"  [+] Seed {seed}: REPAIRED & PASSED on Round {r}!")
                        break
                    else:
                        prev_code = code_rep
                        prev_rep = rep_res
                        curr_rep = rep_res

            status = "PASS" if final_pass else "FAIL"
            line_cov = curr_rep.get("line_pct", 0.0) or 0.0
            covs.append(line_cov)
            if final_pass:
                passes += 1
            print(f"  [-] Seed {seed}: {status:4s} | LineCov: {line_cov:5.1f}%")

        pass_rate = passes / len(SEEDS) * 100.0
        mean_cov = sum(covs) / len(covs)
        results[tid] = {"pass_rate": pass_rate, "mean_cov": mean_cov}
        print(f"[=>] {tid}: Pass Rate = {pass_rate:.1f}% (Mean Cov = {mean_cov:.1f}%)")

    print(engine.get_summary_report())
    return results

def run_flakiness_verification(rounds=5):
    print("\n" + "=" * 70)
    print(f"ACTION 3: FLAKINESS & STABILITY VERIFICATION ACROSS 21 GOLDEN SUITES ({rounds} ROUNDS)")
    print("=" * 70)

    repo_map = {
        'codetiming': REPOS_DIR / 'codetiming',
        'docstring_parser': REPOS_DIR / 'docstring_parser',
        'genty': REPOS_DIR / 'genty',
        'pycg': REPOS_DIR / 'PyCG',
        'string_utils': REPOS_DIR / 'python-string-utils',
        'superstring': REPOS_DIR / 'superstring.py',
        'typesystem': REPOS_DIR / 'typesystem',
        'woa': REPOS_DIR / 'woa'
    }

    golden_files = sorted(GOLDEN_DIR.glob("*.py"))
    total_runs = len(golden_files) * rounds
    passed_runs = 0
    flaky_targets = []

    for f in golden_files:
        name = f.stem
        repo = None
        for k, p in repo_map.items():
            if k in name:
                repo = p
                break
        env = dict(os.environ, PYTHONPATH=f"{repo}:{os.environ.get('PYTHONPATH', '')}")
        cmd = ["uv", "run", "--with", "pytest", "--with", "six", "--with", "numpy", "python3", "-m", "pytest", "-q", str(f)]

        suite_passes = 0
        for r_idx in range(rounds):
            res = subprocess.run(cmd, capture_output=True, text=True, env=env)
            if res.returncode == 0:
                suite_passes += 1
                passed_runs += 1

        if suite_passes == rounds:
            verdict = "100% STABLE"
        else:
            verdict = f"FLAKY ({suite_passes}/{rounds})"
            flaky_targets.append(name)

        print(f"[*] {name:38} | {suite_passes}/{rounds} passed | {verdict}")

    flake_rate = (len(flaky_targets) / len(golden_files) * 100.0) if golden_files else 0.0
    print("-" * 70)
    print(f"TOTAL EXECUTION RUNS: {passed_runs}/{total_runs} ({(passed_runs/total_runs*100):.1f}%)")
    print(f"FLAKY TARGETS DETECTED: {len(flaky_targets)} (Flake Rate: {flake_rate:.2f}%)")
    print("=" * 70)
    return flake_rate

if __name__ == "__main__":
    t_res = re_evaluate_refined_targets()
    f_rate = run_flakiness_verification(rounds=5)
