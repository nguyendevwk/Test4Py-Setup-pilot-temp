---
name: kaggle-dual-gpu-testing
description: >-
  Universal standard operating procedure and automation harness for deploying, benchmarking, and executing
  LLM-based test generation, regression testing, and code quality evaluations on ANY Python repository
  using Kaggle Dual-GPU (2x Tesla T4) environments with $0 API cost. Use whenever standardizing, reproducing,
  or running automated testing, multi-model evaluation, or coverage/mutation benchmarking on Kaggle for any project.
---

# Universal Kaggle Dual-GPU Automated Testing & Benchmarking Skill

Quy trình chuẩn hóa tổng quát (Universal SOP) để triển khai, tự động sinh test và đo lường chất lượng kiểm thử bằng mô hình ngôn ngữ lớn (LLM) trên **BẤT KỲ DỰ ÁN PYTHON NÀO**, tận dụng tối đa phần cứng **Kaggle Dual-GPU (2x Tesla T4 15GB)** hoàn toàn miễn phí ($0 API cost).

---

## 1. Kiến Trúc Điều Phối Hai GPU Tổng Quát (Dual-GPU MoA)

Khi chạy trên Kaggle Dual-T4, luôn chia tải tách biệt giữa 2 GPU để tối ưu hóa VRAM và tốc độ suy luận:

```
┌─────────────────────────────────────────┐       ┌─────────────────────────────────────────┐
│              GPU 0: CODER               │       │             GPU 1: CRITIC               │
│  - Model: 7B hoặc 14B (Coder)           │       │  - Model: 3B hoặc 4B (Critic/Verifier)  │
│  - VRAM: ~8.5 GB (4-bit NF4)            │       │  - VRAM: ~3.2 GB (4-bit NF4)            │
│  - Nhiệm vụ: Sinh mã test & fixtures    │       │  - Nhiệm vụ: Sửa lỗi cú pháp & logic    │
└─────────────────────────────────────────┘       └─────────────────────────────────────────┘
```

---

## 2. Quy Trình Chuẩn Hóa 5 Bước Cho Bất Kỳ Repository Nào

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               5 BƯỚC THỰC THI CHUẨN HÓA TRÊN BẤT KỲ DỰ ÁN PYTHON NÀO                   │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
    ┌───────────────────────────────────────┼───────────────────────────────────────┐
    ▼                                       ▼                                       ▼
【BƯỚC 1: PREFLIGHT REPO】       【BƯỚC 2: STATE MINING】        【BƯỚC 3: DUAL-GPU GEN】
- Clone bất kỳ repo nào          - Phân tích AST mọi class       - Coder (GPU 0) sinh test
- Nhận diện dependencies         - Tìm setter/builder/init       - Critic (GPU 1) repair
- Cài isolated env               - Runtime micro-probing         - Bật Stochastic sampling
                                            │
                                            ▼
                                 【BƯỚC 4: QUALITY GATE】
                                 - Đo Branch Coverage thật
                                 - Chạy Mutation Testing
                                 - Lọc test rỗng (assert True)
                                            │
                                            ▼
                                 【BƯỚC 5: COST & TELEMETRY】
                                 - Tính Input/Output Token
                                 - Đo thời gian Probe vs Gen
                                 - Xuất báo cáo CSV & JSON
```

---

### Bước 1: Khởi Tạo Bất Kỳ Repository Nào Trên Kaggle (Preflight)

Trong Jupyter Notebook của Kaggle, luôn dùng **cell Python gốc** để kiểm soát thư mục làm việc và dependencies:

```python
import os
import subprocess
import sys
from pathlib import Path

# Cấu hình repository mục tiêu bất kỳ
TARGET_REPO_URL = "https://github.com/user/any-python-project.git"
REPO_NAME = TARGET_REPO_URL.split("/")[-1].replace(".git", "")
WORKDIR = Path(f"/kaggle/working/{REPO_NAME}")

# 1. Clone hoặc chuyển vào thư mục repo
if not WORKDIR.exists():
    print(f"📥 Đang clone repository: {REPO_NAME}...")
    subprocess.check_call(["git", "clone", TARGET_REPO_URL, str(WORKDIR)])
os.chdir(WORKDIR)
print(f"📍 Đang làm việc tại: {os.getcwd()}")

# 2. Cài đặt các thư viện đo lường & kiểm thử chuẩn mực
subprocess.check_call([
    sys.executable, "-m", "pip", "install", "-q",
    "pytest", "pytest-json-report", "coverage", "bitsandbytes", "transformers", "accelerate"
])

# 3. Cài đặt dependencies của chính repository mục tiêu (nếu có)
for req_file in ["requirements.txt", "pyproject.toml", "setup.py"]:
    if (WORKDIR / req_file).exists():
        print(f"📦 Đang cài đặt dependencies từ {req_file}...")
        if req_file == "requirements.txt":
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", req_file])
        elif req_file == "setup.py":
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-e", "."])
        break
```

---

### Bước 2: Tự Động Trích Xuất Ngữ Cảnh Trạng Thái (General State Mining)

Đối với các API hướng đối tượng có trạng thái (Stateful Objects), mô hình nhỏ (SLM) sẽ thất bại nếu không có chuỗi setup. Áp dụng quy trình khai phá AST tổng quát:

1. **Static AST Analysis**:
   * Quét class mục tiêu để tìm `__init__` và các phương thức thay đổi trạng thái (tiền tố `set_`, `add_`, `register_`, `create_`, `build_`, `init_`).
   * Quét toàn bộ codebase để tìm các lời gọi mẫu thực tế (Call-Site Mining).
2. **Dynamic Runtime Probing**:
   * Chạy thử các ứng viên setup trong tiến trình con (timeout 5–10s).
   * Loại bỏ ngay các ứng viên gây `TypeError`, `ValueError` hoặc `AttributeError` trước khi đưa vào prompt của LLM.

---

### Bước 3: Điều Phối Sinh Test Đa GPU (Multi-GPU Generation)

Sử dụng vòng lặp Python để chạy lần lượt các cấu hình với **Stochastic Sampling (`temperature = 0.7`)** nhằm đảm bảo ý nghĩa thống kê:

```python
coder_model = "Qwen/Qwen2.5-Coder-14B-Instruct"
critic_model = "Qwen/Qwen3-4B-Instruct-2507"
output_dir = Path("/kaggle/working/EVALUATION_RESULTS")
output_dir.mkdir(parents=True, exist_ok=True)

# Lặp qua các đối chứng: không setup vs có setup heuristic vs có setup kiểm chứng
for mode in ['baseline', 'ranked', 'verified']:
    print("\n" + "=" * 70)
    print(f"🚀 CHẠY ARM: {mode.upper()} (N=15, TEMP=0.7)")
    print("=" * 70)
    
    cmd = [
        sys.executable, "council_runner.py",
        "--mode", mode,
        "--samples", "15",
        "--temperature", "0.7",
        "--coder-model", coder_model,
        "--critic-model", critic_model,
        "--load-in-4bit",
        "--max-new-tokens", "2048",
        "--seed", "42",
        "--output", str(output_dir / f"stat_arm_{mode}")
    ]
    subprocess.run(cmd, check=True)
```

---

### Bước 4: Hàng Rào Chất Lượng Kiểm Thử (Quality Gates)

Một test suite thành công **không đơn thuần là pytest exit code 0**, mà phải vượt qua 3 hàng rào:

1. **Non-Vacuous Gate**: Loại bỏ các test rỗng chỉ chứa `assert True` hoặc không gọi tới logic của target.
2. **Real Branch Coverage**: Đo độ phủ nhánh thực sự của mã nguồn mục tiêu thông qua `coverage run --branch`.
3. **Fault Detection (Mutation Score)**: Chạy test trên tập mutants (các lỗi cố tình đưa vào logic của target) để xác nhận test có khả năng phát hiện lỗi thực sự hay không.

---

### Bước 5: Báo Cáo Đo Lường Chi Phí & Thống Kê (Cost & Statistics)

Sau khi chạy xong, thực thi script phân tích để trích xuất bảng tổng hợp:

```python
import json
from pathlib import Path

results_dir = Path("/kaggle/working/EVALUATION_RESULTS")
print(f"{'Arm':<20} | {'Input Tok':<10} | {'Output Tok':<10} | {'Probe (s)':<10} | {'Gen (s)':<10} | {'Total (s)':<10}")
print("-" * 75)

for summary_file in sorted(results_dir.rglob("summary.json")):
    data = json.loads(summary_file.read_text())
    telemetry = data.get("telemetry", {})
    results = data.get("results", [])
    
    in_tok = telemetry.get("coder_input_tokens", 0) + telemetry.get("critic_input_tokens", 0)
    out_tok = telemetry.get("coder_tokens", 0) + telemetry.get("critic_tokens", 0)
    probe_s = sum(r.get("stages", {}).get("setup", 0.0) for r in results if isinstance(r, dict))
    gen_s = sum(r.get("stages", {}).get("generation", 0.0) for r in results if isinstance(r, dict))
    total_s = data.get("total_seconds", 0.0)
    
    print(f"{summary_file.parent.name:<20} | {in_tok:<10} | {out_tok:<10} | {probe_s:<10.2f} | {gen_s:<10.2f} | {total_s:<10.2f}")
```

---

## 3. Các Quy Tắc Vàng Khi Chạy Bất Kỳ Task Nào Trên Kaggle

1. **Quy tắc 1 (Tránh Subshell Trap)**: Tuyệt đối không dùng bash script nhiều dòng với biến môi trường dạng `$VAR` trừ khi bọc trong lệnh Python `subprocess`. Trong Jupyter, luôn dùng Python để quản lý đường dẫn và tham số.
2. **Quy tắc 2 (4-bit Quantization)**: Mô hình Coder $\ge 7\text{B}$ trên Tesla T4 (15GB) bắt buộc phải nạp bằng 4-bit NF4 (`load_in_4bit=True`). Điều này giải phóng VRAM xuống còn ~8.5GB, cho phép chạy an toàn không bao giờ OOM.
3. **Quy tắc 3 (Phân bổ GPU rõ ràng)**: Coder trên `cuda:0` và Critic trên `cuda:1`. Không bao giờ nạp cả hai mô hình lớn lên cùng một GPU.
4. **Quy tắc 4 (Stochastic Sampling cho thống kê)**: Để kết quả có thể công bố được trên các bài báo/báo cáo khoa học, luôn dùng $N \ge 15$ mẫu với `temperature = 0.7` và seed ngẫu nhiên thay vì greedy decoding ($N=1$ duplicate).
