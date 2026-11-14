"""CLI Runner for Council Architecture on Dual GPU."""
import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import time
import traceback
from typing import Dict, Any, List

from pilot.common import BASE, PYCG, checkout, command, reserve_output, write_json
from pilot.setup import extract, select
from pilot.quality import source_context
from pilot.scoring import score, pytest_run, passed_nodes
from council.engine import CouncilEngine
from council.generator import generate_test_with_coder
from council.critic import audit_test_quality, repair_with_critic


def run_council_pipeline(args) -> Dict[str, Any]:
    output = reserve_output(args.output)
    output.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()

    print("=" * 70)
    print("🚀 TEST4PY COUNCIL ARCHITECTURE (Dual-GPU MoA Engine)")
    print(f"  • Mode          : {args.mode}")
    print(f"  • Samples       : {args.samples}")
    print(f"  • Coder Model   : {args.coder_model}")
    print(f"  • Critic Model  : {args.critic_model}")
    print(f"  • Output Dir    : {output}")
    print("=" * 70, flush=True)

    # 1. Initialize Council Engine
    # Ensure dependencies are available in runtime
    try:
        import pytest_jsonreport
    except ImportError:
        import subprocess
        print("[Setup] Installing pytest-json-report in sandbox environment...", flush=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pytest-json-report"], check=False)

    if getattr(args, 'load_in_4bit', False):
        try:
            import bitsandbytes
        except ImportError:
            import subprocess
            print("[Setup] Installing bitsandbytes for 4-bit quantization on Kaggle T4...", flush=True)
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", "bitsandbytes"], check=False)

    engine = CouncilEngine(
        coder_model=args.coder_model,
        critic_model=args.critic_model,
        mock=args.mock,
        max_new_tokens=args.max_new_tokens,
        load_in_4bit=getattr(args, 'load_in_4bit', False),
    )

    # 2. Checkout target repository (PyCG)
    product = output / 'target_repo'
    checkout('https://github.com/vitsalis/PyCG.git', PYCG, product)

    settings = json.loads((BASE / 'pilot.json').read_text())
    settings['output'] = str(output)

    results = []

    for sample_idx in range(args.samples):
        sample_id = f"sample_{sample_idx+1:02d}"
        sample_dir = output / 'samples' / sample_id
        sample_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n▶ Executing [{sample_id}/{args.samples:02d}]...", flush=True)

        # Create fresh sandbox
        work_repo = sample_dir / 'PyCG'
        shutil.copytree(product, work_repo, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc', 'Test4DT_tests'))

        # A. Fixture Architect: Extract and Verify Setup Context (0.5s)
        t_setup = time.perf_counter()
        setup_context = ""
        if args.mode in ('council', 'verified'):
            extraction = extract(work_repo)
            setup_context, selection = select(work_repo, extraction, 'verified', sample_dir, settings)
            print(f"  [1/4 Fixture Architect] Setup verified via probe ({time.perf_counter()-t_setup:.2f}s)")
        else:
            print("  [1/4 Fixture Architect] Mode baseline: No setup context added")

        # B. Coder: Generate Initial Test Case (GPU 0)
        t_gen = time.perf_counter()
        target_src = source_context(work_repo)
        raw_test = generate_test_with_coder(
            engine=engine,
            module_name="pycg.machinery.imports",
            target_function="get_custom_loader",
            target_source=target_src,
            setup_context=setup_context,
            scenario_desc=settings.get('scenario_prompt', '')
        )
        (sample_dir / 'test_candidate_v1.py').write_text(raw_test)
        print(f"  [2/4 Coder GPU 0] Generated test suite ({time.perf_counter()-t_gen:.2f}s)")

        # C. Quality Audit
        audit = audit_test_quality(raw_test)
        print(f"  [Audit] Valid AST: {audit['valid_ast']} | Assertions: {audit['assertion_count']}")

        # D. Execute pytest in Sandbox
        test_dir = work_repo / 'Test4DT_tests'
        test_dir.mkdir(parents=True, exist_ok=True)
        test_file = test_dir / 'test_generated.py'
        test_file.write_text(raw_test)

        shutil.copyfile(BASE / 'pilot/screen_trace.py', test_dir / 'conftest.py')
        timeout_val = settings.get('pytest_timeout', 15)
        proc_v1, pt_res, _ = pytest_run(work_repo, sample_dir, 'v1_eval', ['Test4DT_tests'], timeout=timeout_val)
        passed_list = passed_nodes(pt_res)
        passed_count = len(passed_list)

        final_code = raw_test
        repaired = False

        # E. Critic: If failing, perform targeted repair on GPU 1
        if passed_count == 0 and audit['valid_ast'] and not args.no_repair:
            t_repair = time.perf_counter()
            print("  [3/4 Critic GPU 1] Pytest failed. Calling Critic to analyze traceback and repair...", flush=True)
            err_log = proc_v1.get('stderr', '') or proc_v1.get('stdout', '') or "Test execution failed."
            repaired_code = repair_with_critic(
                engine=engine,
                broken_code=raw_test,
                traceback_log=err_log[-4000:],
                target_source=target_src,
                setup_context=setup_context
            )
            (sample_dir / 'test_candidate_v2_repaired.py').write_text(repaired_code)
            test_file.write_text(repaired_code)
            proc_v2, pt_res_v2, _ = pytest_run(work_repo, sample_dir, 'v2_repair_eval', ['Test4DT_tests'], timeout=timeout_val)
            passed_repaired = passed_nodes(pt_res_v2)
            if len(passed_repaired) > 0:
                print(f"  ✓ Critic Repair SUCCESS! Tests now passing! ({time.perf_counter()-t_repair:.2f}s)")
                final_code = repaired_code
                repaired = True
            else:
                print(f"  ✗ Critic Repair did not pass. ({time.perf_counter()-t_repair:.2f}s)")

        # F. Score Final Result
        score_res = score(work_repo, sample_dir, settings)
        cov_obj = score_res.get('branch_coverage') or {}
        mod_obj = cov_obj.get('module') or {}
        branch_cov = mod_obj.get('covered_branches', 0)
        tot_branches = mod_obj.get('num_branches', 1)
        branch_pct = round(100 * branch_cov / tot_branches, 1) if tot_branches and branch_cov else None

        sample_summary = {
            "sample_id": sample_id,
            "status": "passed" if score_res.get('passed', 0) > 0 else "failed",
            "passed_tests": score_res.get('passed', 0),
            "repaired_by_critic": repaired,
            "branch_pct": branch_pct,
            "mutation_score": score_res.get('mutation_score'),
            "audit": audit
        }
        results.append(sample_summary)
        write_json(sample_dir / 'result.json', sample_summary)

    # 3. Export Global Report
    total_time = time.perf_counter() - started
    summary = {
        "mode": args.mode,
        "coder_model": args.coder_model,
        "critic_model": args.critic_model,
        "no_repair": getattr(args, 'no_repair', False),
        "samples": len(results),
        "passed_samples": sum(1 for r in results if r['passed_tests'] > 0),
        "critic_repairs": sum(1 for r in results if r['repaired_by_critic']),
        "telemetry": engine.telemetry,
        "total_seconds": round(total_time, 2),
        "results": results
    }
    write_json(output / 'summary.json', summary)

    # Generate Markdown Report
    lines = [
        "# Test4Py Council Architecture Evaluation Report",
        "",
        f"- **Mode**: `{args.mode}`",
        f"- **Coder Model (GPU 0)**: `{args.coder_model}`",
        f"- **Critic Model (GPU 1)**: `{args.critic_model}`",
        f"- **Samples Finished**: `{len(results)}/{args.samples}`",
        f"- **Successful Suites**: `{summary['passed_samples']}/{len(results)}`",
        f"- **Critic Repairs Succeeded**: `{summary['critic_repairs']}`",
        f"- **Total Time**: `{total_time:.2f}s`",
        "",
        "| Sample | Status | Pass Count | Critic Repaired | Branch % | Mutation Score |",
        "|---|---|---:|---|---:|---:|"
    ]
    for r in results:
        lines.append(f"| {r['sample_id']} | {r['status']} | {r['passed_tests']} | {r['repaired_by_critic']} | {r['branch_pct']}% | {r['mutation_score']} |")
    lines.append("")
    (output / 'report.md').write_text("\n".join(lines) + "\n")

    print("\n" + "=" * 70)
    print("🏁 COUNCIL PIPELINE COMPLETED!")
    print(f"  • Successful Samples : {summary['passed_samples']}/{len(results)}")
    print(f"  • Critic Repairs     : {summary['critic_repairs']}")
    print(f"  • Report Path        : {output / 'report.md'}")
    print("=" * 70, flush=True)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--samples', type=int, default=2, help='Number of test attempts to run (small scale test)')
    parser.add_argument('--mode', choices=('council', 'baseline', 'verified'), default='council')
    parser.add_argument('--fast', action='store_true', help='Use fast SLMs (4B/1.5B) for rapid Kaggle testing')
    parser.add_argument('--coder-model', default=None)
    parser.add_argument('--critic-model', default=None)
    parser.add_argument('--no-repair', action='store_true', help='Disable Critic repair loop')
    parser.add_argument('--max-new-tokens', type=int, default=512, help='Token limit (512 is fast and ample for pytest files)')
    parser.add_argument('--load-in-4bit', dest='load_in_4bit', action='store_true', default=None, help='Force 4-bit NF4 quantization')
    parser.add_argument('--no-4bit', dest='load_in_4bit', action='store_false', help='Disable 4-bit quantization and force FP16')
    parser.add_argument('--mock', action='store_true', help='Mock model generation for offline testing')
    parser.add_argument('--output', type=Path, default=BASE / 'runs' / 'council_run')
    args = parser.parse_args()

    # Model defaults
    if args.fast:
        args.coder_model = args.coder_model or "Qwen/Qwen3-4B-Instruct-2507"
        args.critic_model = args.critic_model or "Qwen/Qwen3-4B-Instruct-2507"
    else:
        args.coder_model = args.coder_model or "Qwen/Qwen2.5-Coder-7B-Instruct"
        args.critic_model = args.critic_model or "Qwen/Qwen3-4B-Instruct-2507"

    # Auto-detect 4-bit quantization for 7B+ models on 16GB GPUs to prevent CUDA OOM
    if args.load_in_4bit is None:
        model_str = (args.coder_model or "").lower()
        args.load_in_4bit = any(s in model_str for s in ["7b", "8b", "14b", "32b"])
        if args.load_in_4bit:
            print("[Council] Auto-detected 7B+ model: Enabling 4-bit NF4 quantization to fit within Kaggle T4 VRAM (15GB).")

    run_council_pipeline(args)


if __name__ == '__main__':
    main()
