"""Analyze Telemetry and Cost Breakdown from Kaggle Experiment Summaries."""
import json
from pathlib import Path
import sys

def analyze(directory):
    root = Path(directory)
    summary_files = sorted(list(root.rglob("summary.json")))
    if not summary_files:
        print(f"No summary.json found in {root}")
        return

    print("=" * 105)
    print(f"{'Folder / Arm':<28} | {'Mode':<10} | {'In Tok':<9} | {'Out Tok':<9} | {'Setup (s)':<10} | {'Gen (s)':<10} | {'Total (s)':<10}")
    print("-" * 105)

    for s_file in summary_files:
        try:
            data = json.loads(s_file.read_text())
            folder = s_file.parent.name
            mode = data.get("mode", "unknown")
            telemetry = data.get("telemetry") or {}
            results = data.get("results") or []

            in_tok = telemetry.get("coder_input_tokens", 0) + telemetry.get("critic_input_tokens", 0)
            out_tok = telemetry.get("coder_tokens", 0) + telemetry.get("critic_tokens", 0)

            setup_time = sum(r.get("stages", {}).get("setup", 0.0) for r in results if isinstance(r, dict))
            gen_time = sum(r.get("stages", {}).get("generation", 0.0) for r in results if isinstance(r, dict))
            total_time = data.get("total_seconds", 0.0)

            print(f"{folder:<28} | {mode:<10} | {in_tok:<9} | {out_tok:<9} | {setup_time:<10.2f} | {gen_time:<10.2f} | {total_time:<10.2f}")
        except Exception as e:
            print(f"{s_file.parent.name:<28} | Error: {e}")
    print("=" * 105)

if __name__ == '__main__':
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"
    analyze(target_dir)
