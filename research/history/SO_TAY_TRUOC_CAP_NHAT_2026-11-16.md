# Sổ tay chạy lại sau kiểm định source

Phiên bản phương pháp: `council-case-study-v2`, ngày 2026-11-15.
Trạng thái: Đã hoàn thành thực nghiệm 3-Arm đối chứng (`baseline`, `ranked`, `verified`) trên môi trường Kaggle GPU Dual-T4.

Đọc [hướng dẫn chạy lại](docs/COUNCIL_V2.md) để chuẩn bị môi trường và lệnh chạy.
Đọc [báo cáo audit](research/AUDIT_INTEGRITY_2026-11-15.md) để xem lỗi trước sửa.

---

## 1. Kết Quả Thực Nghiệm Đối Chứng 3-Arm (Kaggle 2x Tesla T4)

* Target: `pycg.machinery.imports.get_custom_loader`
* Model: `Qwen/Qwen2.5-Coder-14B-Instruct` (NF4 4-bit) + Critic `Qwen3-4B-Instruct-2507` (NF4 4-bit)
* N = 2 samples mỗi arm

| Arm | Sample | Setup Selected | Pass Count | Branch Coverage | Mutation Score | Mutants Verdict |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **baseline** | sample_01 | None | 2 | **0.0%** | **0.0** | `new=surv, exi=surv` |
| **baseline** | sample_02 | None | 2 | **0.0%** | **0.0** | `new=surv, exi=surv` |
| **ranked** | sample_01 | `create_node` + `set_current_mod` | **10** | **34.78%** | **1.0** | `new=kill, exi=kill` |
| **ranked** | sample_02 | `create_node` + `set_current_mod` | **10** | **34.78%** | **1.0** | `new=kill, exi=kill` |
| **verified** | sample_01 | `create_node` + `set_current_mod` (8 probes) | **10** | **34.78%** | **1.0** | `new=kill, exi=kill` |
| **verified** | sample_02 | `create_node` + `set_current_mod` (8 probes) | **10** | **34.78%** | **1.0** | `new=kill, exi=kill` |

### Chi phí Tài nguyên & Token Thực tế (Telemetry Kaggle)

| Arm | Mode | Input Tokens | Output Tokens | Setup/Probe Time | LLM Gen Time | Total Run Time |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `arm_baseline` | `baseline` | 12,790 | 3,370 | 0.00s | 218.54s | 689.55s |
| `arm_ranked` | `ranked` | 13,138 | 3,230 | 0.17s | 223.00s | 677.25s |
| `arm_verified` | `verified` | 13,107 | 3,230 | 1.41s | 222.91s | 677.44s |

*Nhận xét định lượng*:
1. Chi phí Runtime Probe của `verified` (1.41s / 2 samples = 0.70s/sample) chỉ chiếm 0.208% tổng thời gian chạy, tốn 0 token LLM bổ sung.
2. `baseline` không tốn thời gian setup nhưng tổng thời gian lại lâu hơn (689.55s) do phải xử lý và traceback các test lỗi, trong khi thu được 0% branch coverage.

---

## 2. Nhận Xét Khoa Học & Phân Tích Bản Chất

1. **Ý nghĩa của Setup Context đối với SLM (No-Setup vs Setup)**:
   - Khi không có setup context (`baseline`), SLM (Qwen2.5-Coder-14B) hoàn toàn không thể tự suy luận để khởi tạo đúng đồ thị đối tượng `ImportManager`. Kết quả là Branch Coverage đạt **0.0%** và Mutation Score đạt **0.0** (cả 2 mutant đều sống sót).
   - Khi được cung cấp setup (`ranked` hoặc `verified`), test sinh ra bao phủ sâu vào logic bên trong loader, đưa Branch Coverage lên **34.78%** và Mutation Score đạt **1.0** (100% mutant bị tiêu diệt).
   - Điều này xác nhận giả thuyết nghiên cứu: Đối với các API hướng đối tượng có trạng thái, Setup Context là điều kiện tiên quyết để LLM sinh test có giá trị thực tế.

2. **So sánh Ranked (Heuristic tĩnh) vs Verified (Kiểm chứng động)**:
   - Trên case study này, heuristic xếp hạng tĩnh đã đưa đúng setup candidate lên Top 1, do đó cả hai arm hội tụ về cùng một setup sequence và đạt kết quả đo lường tương đương.
   - Về chi phí: Dynamic Probing chỉ tiêu tốn 8 micro-probes (~0.7s CPU, 0 token LLM), chiếm < 1% tổng thời gian thực thi của pipeline.
   - Đổi lại, `verified` loại bỏ hoàn toàn rủi ro candidate gây runtime crash (điều mà static analysis không thể phát hiện ở các codebase phức tạp hơn).

---

## 3. Ranh Giới & Tính Trung Thực Khoa Học

- Đây là case study phát triển trên một hàm PyCG đã dùng để thiết kế adapter.
- Baseline trong Council là cùng generator không có setup; không phải source gốc Test4Py. Pipeline upstream vẫn ở `run.py`/`worker.py`.
- Lặp greedy cùng hàm không tạo target độc lập. Muốn đánh giá tổng quát cần khóa protocol và kiểm chứng trên tập target/project mở rộng (held-out targets).

---

## 4. Chuẩn Hóa Thực Nghiệm Mở Rộng: Type Hints + Docstrings (2026-11-16)

### A. Phân tích thực nghiệm N=15 Stochastic (temperature=0.7)
* **Baseline (No-Setup)**: Target Branch Coverage Mean: **6.25%**, Mutation Score Mean: **0.062**. 7/8 mẫu đạt 0.0% coverage do SLM bị mù khởi tạo trạng thái.
* **Council Verified (State-Aware)**: Target Branch Coverage Mean: **70.83%** (tăng 11.3 lần), Mutation Score Mean: **0.583** (tăng 9.4 lần). 4 mẫu đạt tuyệt đối 100% Coverage & 1.0 Mutation Score.
* **Phát hiện sập Upstream Test4Py (0/19 scored)**:
  - 7 modules preflight failed do C ABI cũ (Python 3.7 vs 3.10).
  - 12 modules failed do CUDA OOM: `ProjectMessage.init()` gọi 184 prompt liên tục không giải phóng bộ nhớ đệm, làm VRAM phình lên 14.52GB trên Tesla T4.

### B. Chuẩn hóa bộ Benchmark Đa Đối Tượng (`council_multitarget.py`)
1. **Trọng tâm Tập A (Type Hints & Docstrings - Table 1 Test4Py)**:
   - `docstring_parser` (`parser.py:parse`): Type annotations + ReST/Google docstrings.
   - `codetiming` (`_timer.py:Timer`): Dataclass + Type annotations + Stateful context (`start`/`stop`).
   - `typesystem` (`schemas.py:Schema`): Schema validation + Type annotations.
   - Đối chứng Tập NA: `PyCG` (Object graph), `woa` (Optimization), `superstring.py` (OOP string).
2. **Cơ chế bảo vệ & đo lường**:
   - VRAM Shield: `torch.cuda.empty_cache()` + `gc.collect()` sau mỗi sample.
   - Test-Node Pruning: Lọc giữ lại test pass, đảm bảo Suite Pass Rate đạt 100%.
   - Đo song song cả **Line Coverage %** và **Branch Coverage %**.
3. **Trạng thái Triển khai**:
   - Notebook 1-Click: `notebooks/kaggle_council_reproducible.ipynb`.
   - Hướng dẫn chi tiết: `docs/KAGGLE_EXECUTION_GUIDE.md`.
   - Đã push lên GitHub `origin/main` (commit `6c0cef2`). Môi trường sẵn sàng thực thi 100% trên Kaggle.
