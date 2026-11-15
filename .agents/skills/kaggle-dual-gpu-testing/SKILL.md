---
name: kaggle-dual-gpu-testing
description: >-
  Universal standard operating procedure and automation harness for deploying, benchmarking, and executing
  LLM-based test generation, regression testing, and code quality evaluations on ANY Python repository
  using Kaggle Dual-GPU (2x Tesla T4) environments with $0 API cost. Use whenever standardizing, reproducing,
  or running automated testing, multi-model evaluation, or coverage/mutation benchmarking on Kaggle for any project.
---

# Universal Dual-GPU Testing & Benchmarking on Kaggle (Zero-Bias SOP)

Quy trình chuẩn hóa **hoàn toàn độc lập** (Zero-Bias & Repository-Agnostic) để triển khai tự động sinh test, sửa lỗi và đo lường chất lượng kiểm thử bằng LLM trên **BẤT KỲ DỰ ÁN PYTHON NÀO**, tận dụng môi trường **Kaggle Dual-GPU (2x Tesla T4 15GB)** miễn phí 100% ($0 API cost).

> [!IMPORTANT]
> Quy trình này **không phụ thuộc** vào bất kỳ codebase, runner cũ hay tập dữ liệu cụ thể nào. Nó là một harness độc lập dùng thuần thư viện chuẩn (`ast`, `subprocess`, `pytest`, `coverage`, Hugging Face `transformers` và `bitsandbytes`).

---

## 1. Kiến Trúc Điều Phối Phần Cứng Kaggle (Dual-GPU MoA)

```
┌──────────────────────────────────────────────┐       ┌──────────────────────────────────────────────┐
│           GPU 0 (cuda:0) - CODER             │       │           GPU 1 (cuda:1) - CRITIC            │
│  - Mô hình: 7B hoặc 14B (ví dụ Qwen 14B)     │       │  - Mô hình: 3B hoặc 4B (ví dụ Qwen 4B)       │
│  - VRAM chiếm dụng: ~8.5 GB (4-bit NF4)      │       │  - VRAM chiếm dụng: ~3.2 GB (4-bit NF4)      │
│  - Vai trò: Khai phá & sinh test ban đầu     │       │  - Vai trò: Đọc traceback & sửa test lỗi     │
└──────────────────────────────────────────────┘       └──────────────────────────────────────────────┘
```

---

## 2. Quy Trình Chuẩn Hóa 4 Bước Áp Dụng Cho Mọi Dự Án

### Bước 1: Khởi Tạo Môi Trường Sạch Trên Kaggle (Preflight)
Trong một Cell Python của Kaggle Notebook, nạp dependencies tiêu chuẩn:
```python
import subprocess, sys

# Cài đặt bộ công cụ đo lường chuẩn hóa
subprocess.check_call([
    sys.executable, "-m", "pip", "install", "-q",
    "pytest", "pytest-json-report", "coverage", "bitsandbytes", "transformers", "accelerate"
])
```

### Bước 2: Clone hoặc Chỉ Định Dự Án Bất Kỳ
```python
import subprocess, os
from pathlib import Path

# Đặt link repo bất kỳ cần kiểm thử
REPO_URL = "https://github.com/pallets/click.git" # Hoặc fastapi, requests, bất kỳ repo nào
REPO_NAME = REPO_URL.split("/")[-1].replace(".git", "")
REPO_DIR = Path(f"/kaggle/working/{REPO_NAME}")

if not REPO_DIR.exists():
    subprocess.check_call(["git", "clone", REPO_URL, str(REPO_DIR)])

# Cài đặt dependencies nội tại của repo nếu có
if (REPO_DIR / "requirements.txt").exists():
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", str(REPO_DIR / "requirements.txt")])
```

### Bước 3: Thực Thi Sinh Test Bằng Standalone Dual-GPU Harness
Gọi script tổng quát [standalone_dual_gpu_tester.py](./scripts/standalone_dual_gpu_tester.py) để chạy đối chứng thống kê đa mẫu ($N \ge 15$, `temperature = 0.7`):

```python
import subprocess, sys

# Chỉ định target bất kỳ trong repo
cmd = [
    sys.executable, ".agents/skills/kaggle-dual-gpu-testing/scripts/standalone_dual_gpu_tester.py",
    "--repo", str(REPO_DIR),
    "--file", "src/click/core.py",          # Đường dẫn file chứa target
    "--module", "click.core",               # Module import
    "--symbol", "Command",                  # Tên class hoặc hàm cần test
    "--mode", "verified",                   # 'baseline', 'ranked', hoặc 'verified'
    "--samples", "15",                      # N=15 mẫu độc lập
    "--temperature", "0.7",                 # Stochastic sampling phục vụ tính p-value
    "--coder-model", "Qwen/Qwen2.5-Coder-14B-Instruct",
    "--critic-model", "Qwen/Qwen3-4B-Instruct-2507",
    "--load-in-4bit",
    "--output", f"/kaggle/working/EVAL_{REPO_NAME}_verified"
]

subprocess.run(cmd, check=True)
```

### Bước 4: Hàng Rào Chất Lượng (Quality Gate) & Báo Cáo
Harness tự động thực hiện:
1. **Pytest JSON Verification**: Kiểm tra trạng thái pass/fail thực sự.
2. **True Branch Coverage**: Chạy `coverage run --branch` đo độ phủ nhánh thực tế của module mục tiêu.
3. **Critic Repair**: Nếu Coder sinh test lỗi, Critic trên GPU 1 tự động đọc traceback lỗi và sửa mà không làm mất assertion.
4. **Telemetry Export**: Xuất file `summary.json` gồm chi phí token, thời gian probe CPU và thời gian GPU.

---

## 3. Ba Nguyên Tắc Tránh Thiên Lệch (Zero-Bias Principles)

1. **Không Hardcode Quy Tắc Của Một Repo Cụ Thể**:
   * Việc trích xuất phương thức trạng thái (`mine_candidate_setups`) hoàn toàn dựa trên AST tĩnh (tìm các tiền tố `set_`, `add_`, `create_`, `register_` v.v.).
   * Không chứa bất kỳ allowlist hay hằng số nào của repo cũ.
2. **Khách Quan Trong Kiểm Chứng Động (Runtime Probing)**:
   * Mọi ứng viên setup đều phải chạy qua sandbox Python độc lập (`subprocess`). Chỉ những chuỗi không gây crash runtime mới được đưa vào context của LLM.
3. **Độc Lập Thống Kê (Statistical Validity)**:
   * Tuyệt đối không dùng greedy decoding lặp lại để báo cáo "ổn định 100%".
   * Luôn sử dụng $N \ge 15$ mẫu với hạt giống ngẫu nhiên tăng dần (`seed + i`) và `temperature = 0.7` để có phân phối độ lệch chuẩn, phục vụ tính **Wilcoxon signed-rank test** ($p < 0.01$).
