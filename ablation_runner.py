"""Ablation Study Runner and Result Aggregator for Test4Py Council Paper."""
import argparse
import json
import os
from pathlib import Path
import sys
import time
from typing import Dict, Any, List

from pilot.common import BASE, reserve_output, write_json
from council.runner import run_council_pipeline

VARIANTS = {
    "full_14b": {
        "name": "Full Council (Proposed)",
        "coder_model": "Qwen/Qwen2.5-Coder-14B-Instruct",
        "critic_model": "Qwen/Qwen3-4B-Instruct-2507",
        "mode": "council",
        "no_repair": False,
        "desc": "Full Council with Fixture Architect, Coder 14B, and Critic Repair",
    },
    "no_fixture_14b": {
        "name": "w/o Fixture Architect",
        "coder_model": "Qwen/Qwen2.5-Coder-14B-Instruct",
        "critic_model": "Qwen/Qwen3-4B-Instruct-2507",
        "mode": "baseline",
        "no_repair": False,
        "desc": "Ablation: Removes Verified Setup Context (raw source only)",
    },
    "no_critic_14b": {
        "name": "w/o Critic Self-Repair",
        "coder_model": "Qwen/Qwen2.5-Coder-14B-Instruct",
        "critic_model": "Qwen/Qwen3-4B-Instruct-2507",
        "mode": "council",
        "no_repair": True,
        "desc": "Ablation: Disables Critic repair loop (single-shot Coder)",
    },
    "scale_7b": {
        "name": "Coder 7B Scale",
        "coder_model": "Qwen/Qwen2.5-Coder-7B-Instruct",
        "critic_model": "Qwen/Qwen3-4B-Instruct-2507",
        "mode": "council",
        "no_repair": False,
        "desc": "Model Scale: Coder 7B with Critic Repair",
    },
    "scale_3b": {
        "name": "Coder 3B Scale",
        "coder_model": "Qwen/Qwen2.5-Coder-3B-Instruct",
        "critic_model": "Qwen/Qwen3-4B-Instruct-2507",
        "mode": "council",
        "no_repair": False,
        "desc": "Model Scale: Coder 3B with Critic Repair",
    },
}


def compile_ablation_reports(runs_dir: Path) -> str:
    """Scan all summary.json in runs directory and produce a unified comparison table."""
    summaries = []
    for summary_path in sorted(runs_dir.rglob("summary.json")):
        try:
            data = json.loads(summary_path.read_text())
            data["_path"] = str(summary_path.parent.name)
            summaries.append(data)
        except Exception:
            continue

    if not summaries:
        return "No run summaries found to compile."

    lines = [
        "# Test4Py Council Architecture - Ablation Study Comparison",
        "",
        "| Configuration / Variant | Coder Model | Mode | Critic Repair | Samples | Suite Pass Rate | Avg Branch % | Avg Mutation Score |",
        "|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|",
    ]

    for s in summaries:
        coder = s.get("coder_model", "Unknown")
        if coder != "Unknown":
            coder = coder.split("/")[-1]
        mode = s.get("mode", "council")
        total_samples = s.get("samples", 0)
        passed_samples = s.get("passed_samples", 0)
        pass_rate = f"{(passed_samples / total_samples * 100):.1f}%" if total_samples > 0 else "N/A"

        no_rep = s.get("no_repair", False)
        repairs = s.get("critic_repairs", 0)
        if no_rep:
            repair_str = "Disabled (w/o Critic)"
        elif repairs > 0:
            repair_str = f"Repaired ({repairs})"
        else:
            repair_str = "Enabled"

        # Averages
        branches = [r["branch_pct"] for r in s.get("results", []) if r.get("branch_pct") is not None]
        avg_branch = f"{(sum(branches) / len(branches)):.1f}%" if branches else "N/A"

        mutations = [r["mutation_score"] for r in s.get("results", []) if r.get("mutation_score") is not None]
        avg_mut = f"{(sum(mutations) / len(mutations)):.2f}" if mutations else "N/A"

        run_tag = s["_path"]
        lines.append(f"| `{run_tag}` | `{coder}` | `{mode}` | {repair_str} | {passed_samples}/{total_samples} | **{pass_rate}** | {avg_branch} | {avg_mut} |")

    lines.append("")
    report_content = "\n".join(lines)
    out_file = runs_dir / "ablation_comparison.md"
    out_file.write_text(report_content)
    print(f"✓ Ablation comparison table generated at: {out_file}")
    return report_content


def run_single_variant(variant_key: str, samples: int, base_output: Path, mock: bool = False):
    cfg = VARIANTS[variant_key]
    out_dir = base_output / f"ablation_{variant_key}"
    print("\n" + "=" * 70)
    print(f"🔬 RUNNING ABLATION VARIANT: {cfg['name']}")
    print(f"  • Description: {cfg['desc']}")
    print(f"  • Coder: {cfg['coder_model']}")
    print(f"  • Critic: {cfg['critic_model']}")
    print(f"  • Mode: {cfg['mode']} | No-Repair: {cfg['no_repair']}")
    print(f"  • Output: {out_dir}")
    print("=" * 70, flush=True)

    class Args:
        pass

    args = Args()
    args.samples = samples
    args.mode = cfg["mode"]
    args.fast = False
    args.coder_model = cfg["coder_model"]
    args.critic_model = cfg["critic_model"]
    args.no_repair = cfg["no_repair"]
    args.max_new_tokens = 512
    args.load_in_4bit = True
    args.mock = mock
    args.output = out_dir

    return run_council_pipeline(args)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=list(VARIANTS.keys()) + ["all"], default="full_14b",
                        help="Specific ablation variant to run")
    parser.add_argument("--samples", type=int, default=2, help="Number of samples per variant")
    parser.add_argument("--output", type=Path, default=BASE / "runs" / "ablation_study")
    parser.add_argument("--mock", action="store_true", help="Run with mock LLM for offline validation")
    parser.add_argument("--compile", action="store_true", help="Compile existing summary files into Markdown table")
    args = parser.parse_args()

    if args.compile:
        report = compile_ablation_reports(args.output if args.output.exists() else BASE / "runs")
        print(report)
        return

    if args.variant == "all":
        for var_key in VARIANTS.keys():
            run_single_variant(var_key, args.samples, args.output, mock=args.mock)
        compile_ablation_reports(args.output)
    else:
        run_single_variant(args.variant, args.samples, args.output, mock=args.mock)
        compile_ablation_reports(args.output)


if __name__ == "__main__":
    main()
