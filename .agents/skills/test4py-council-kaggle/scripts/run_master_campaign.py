"""Master Evaluation Runner for Kaggle Notebooks.

This script executes both:
1. Micro Evaluation: Multi-sample statistical comparison (N=15, temp=0.7)
2. Macro Evaluation: Upstream Test4Py benchmark across 19 modules / 9 projects
"""
import os
import sys
from pathlib import Path

# 1. Ensure working directory is in the repository root
repo_markers = list(Path("/kaggle/working").glob("**/council_runner.py"))
if repo_markers:
    repo_dir = repo_markers[0].parent
    os.chdir(repo_dir)
    print(f"📍 Set working directory to repository: {repo_dir}")
else:
    print("❌ Repository not found. Please ensure repo is cloned to /kaggle/working.")
    sys.exit(1)

# 2. Update repository and install runtime packages
print("🔄 Updating source from GitHub...")
os.system("git pull origin main")

print("📦 Installing required evaluation packages...")
os.system("pip install -q pytest-json-report coverage bitsandbytes")

# 3. Micro Evaluation (Statistical Arm Study)
out_root = Path("/kaggle/working/MASTER_EVALUATION")
out_root.mkdir(parents=True, exist_ok=True)

modes = ['baseline', 'ranked', 'verified']
samples = 15
temp = 0.7

print("\n" + "=" * 80)
print(f"🚀 STAGE 1: MICRO EVALUATION (N={samples}, Temperature={temp})")
print("=" * 80)

for mode in modes:
    arm_out = out_root / f"stat_arm_{mode}"
    print(f"\n▶️ Running Arm: {mode.upper()} -> {arm_out}")
    cmd = (
        f"python council_runner.py "
        f"--mode {mode} "
        f"--samples {samples} "
        f"--temperature {temp} "
        f"--coder-model Qwen/Qwen2.5-Coder-14B-Instruct "
        f"--critic-model Qwen/Qwen3-4B-Instruct-2507 "
        f"--load-in-4bit "
        f"--max-new-tokens 2048 "
        f"--seed 42 "
        f"--output {arm_out}"
    )
    ret = os.system(cmd)
    if ret != 0:
        print(f"⚠️ Warning: Arm {mode} exited with code {ret}")

print("\n" + "=" * 80)
print("🚀 STAGE 2: MACRO EVALUATION (19 MODULES / 9 PROJECTS)")
print("=" * 80)

bench_dir = out_root / "bench19_upstream"
model_name = "Qwen/Qwen2.5-Coder-14B-Instruct"

# Step 2.1: Plan
print("\n▶️ Planning module allocation...")
os.system(f"python benchmark19.py --action plan --output {bench_dir} --model {model_name}")

# Step 2.2: Prepare venvs & checkout 9 repos
print("\n▶️ Preparing venvs and cloning 9 repos...")
os.system(f"python benchmark19.py --action prepare --resume --output {bench_dir} --model {model_name}")

# Step 2.3: Run upstream test generation with SLM 14B
print("\n▶️ Executing upstream test generation...")
os.system(f"python benchmark19.py --action run --resume --output {bench_dir} --model {model_name}")

print("\n" + "🏁" * 40)
print("🏆 MASTER EVALUATION CAMPAIGN FINISHED!")
print("🏁" * 40)
