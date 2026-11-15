---
name: test4py-council-kaggle
description: >-
  Standardized operational runbook and protocol for deploying, evaluating, and standardizing
  Test4Py Council Architecture and State-aware Regression Testing experiments on Kaggle
  Dual-GPU (2x Tesla T4) environments. Use whenever the user asks to run, reproduce, standardize,
  or benchmark Test4Py Council on Kaggle.
---

# Test4Py Council Kaggle Operational Skill

Quy trình chuẩn hóa (SOP - Standard Operating Procedure) cho toàn bộ dự án nghiên cứu **Test4Py Council Architecture** trên môi trường điện toán đám mây Kaggle (2x Tesla T4, 15GB VRAM, $0 API cost).

---

## 1. Nguyên Tắc Cốt Tử Khi Chạy Trên Kaggle

1. **Thực thi trong Cell Python (Native Jupyter)**:
   * **KHÔNG** dùng multi-line bash với `set -e` hoặc đặt dấu `!` ở mọi dòng (sẽ gây lỗi mất biến môi trường giữa các subshell).
   * **LUÔN** dùng vòng lặp Python `for mode in [...]` kết hợp nội suy biến `{mode}` trong lệnh `!python council_runner.py`.
2. **Quản lý Thư mục làm việc (`pwd`)**:
   * Khi khởi động phiên Kaggle mới, container mặc định đứng ở `/kaggle/working`.
   * Luôn đảm bảo đã `cd` vào đúng thư mục chứa repo trước khi chạy `git pull` hoặc gọi `council_runner.py`.
3. **Quản lý Bộ nhớ GPU (Tránh CUDA OOM)**:
   * Qwen2.5-Coder-14B (GPU 0) và Qwen3-4B (GPU 1) **bắt buộc** phải nạp ở chế độ **4-bit NF4 Quantization** (`--load-in-4bit`).
4. **Độ Tin Cậy Thống Kê (Tránh Desk Reject)**:
   * Để có phân phối thống kê hợp lệ, luôn đặt `--temperature 0.7` với $N \ge 10$ hoặc $15$ mẫu để mỗi sample có seed độc lập. Không dựa vào kết quả greedy $N=2$.

---

## 2. Quy Trình Chuẩn Hóa 4 Bước

```
┌────────────────────────────────────────────────────────────────────────┐
│                        QUY TRÌNH 4 BƯỚC CHUẨN HÓA                      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
    ┌───────────────────────────────┼───────────────────────────────┐
    ▼                               ▼                               ▼
【BƯỚC 1: PREFLIGHT】     【BƯỚC 2: MICRO EVAL】      【BƯỚC 3: MACRO EVAL】
- Cập nhật Git            - 3 Arm: baseline/ranked/   - 19 modules / 9 repos
- Cài dependencies          verified ($N \ge 15$)     - Benchmark upstream
- Kiểm tra 2x Tesla T4    - Đo p-value, Cliff's Δ     - Đo tính mở rộng
                                    │
                                    ▼
                         【BƯỚC 4: AUDIT & COST】
                         - Trích xuất Token / Stage time
                         - Cập nhật SO_TAY_NGHIEN_CUU.md
```

### Bước 1: Khởi động & Kiểm tra môi trường (Preflight)
Chạy cell chuẩn bị môi trường:
```python
# Cập nhật mã nguồn mới nhất
!git pull origin main

# Cài đặt bắt buộc các thư viện đo lường
!pip install -q pytest-json-report coverage bitsandbytes
```

### Bước 2: Thực thi Giai đoạn 1 — Nghiên cứu Thống kê Vi mô (Micro Study)
Chạy đối chứng 3 Arm với $N=15$ mẫu ngẫu nhiên:
```python
output_base = "/kaggle/working/MASTER_EVALUATION"

for mode in ['baseline', 'ranked', 'verified']:
    print("\n" + "=" * 70)
    print(f"🚀 BẮT ĐẦU CHẠY ARM: {mode.upper()} (N=15 SAMPLES, TEMP=0.7)")
    print("=" * 70)
    
    !python council_runner.py \
        --mode {mode} \
        --samples 15 \
        --temperature 0.7 \
        --coder-model Qwen/Qwen2.5-Coder-14B-Instruct \
        --critic-model Qwen/Qwen3-4B-Instruct-2507 \
        --load-in-4bit \
        --max-new-tokens 2048 \
        --seed 42 \
        --output {output_base}/stat_arm_{mode}
```

### Bước 3: Thực thi Giai đoạn 2 — Macro Benchmark Diện Rộng (19 Modules / 9 Repos)
Đánh giá năng lực tổng quát trên 9 repositories từ bài báo Test4Py:
```python
bench_dir = f"{output_base}/bench19_upstream"

# 1. Tạo plan phân bổ
!python benchmark19.py --action plan --output {bench_dir} --model Qwen/Qwen2.5-Coder-14B-Instruct

# 2. Checkout 9 repositories và dựng isolated venv
!python benchmark19.py --action prepare --resume --output {bench_dir} --model Qwen/Qwen2.5-Coder-14B-Instruct

# 3. Chạy sinh test upstream bằng SLM 14B
!python benchmark19.py --action run --resume --output {bench_dir} --model Qwen/Qwen2.5-Coder-14B-Instruct
```

### Bước 4: Kiểm toán Kết quả & Trích xuất Chi phí (Telemetry Audit)
Chạy script phân tích tự động để lấy số liệu Token và Thời gian từng giai đoạn:
```python
import json
from pathlib import Path

working_dir = Path("/kaggle/working/MASTER_EVALUATION")
for s_file in sorted(working_dir.rglob("summary.json")):
    data = json.loads(s_file.read_text())
    telemetry = data.get("telemetry") or {}
    results = data.get("results") or []
    in_tok = telemetry.get("coder_input_tokens", 0) + telemetry.get("critic_input_tokens", 0)
    out_tok = telemetry.get("coder_tokens", 0) + telemetry.get("critic_tokens", 0)
    probe_time = sum(r.get("stages", {}).get("setup", 0.0) for r in results if isinstance(r, dict))
    gen_time = sum(r.get("stages", {}).get("generation", 0.0) for r in results if isinstance(r, dict))
    print(f"{s_file.parent.name:<25} | In: {in_tok:<8} | Out: {out_tok:<6} | Probe: {probe_time:<6.2f}s | Gen: {gen_time:<6.2f}s | Total: {data.get('total_seconds', 0.0):<6.2f}s")
```

---

## 3. Tài Liệu Tham Chiếu Chi Tiết

* [Quy chuẩn khoa học & Ranh giới bài báo](./references/PROTOCOL_AND_FAIRNESS.md)
* [Sổ tay khắc phục sự cố Kaggle](./references/KAGGLE_PITFALLS.md)
* [Script tổng lực chạy tự động 11 tiếng](./scripts/run_master_campaign.py)
