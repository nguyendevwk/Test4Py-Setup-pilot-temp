# Báo Cáo Thực Nghiệm Thống Kê Chuẩn Bài Báo (Statistical Paper Benchmark)
*Mô hình đánh giá:* `openai/gpt-oss-20b` (Groq Engine)
*Giao thức thực nghiệm:* $N=3$ trials ngẫu nhiên độc lập (seeds: 42, 43, 44) cho mỗi đối tượng.
*Đối tượng thực nghiệm:* 6 Benchmark subjects đại diện từ Bảng 1 bài báo Test4Py (*arXiv:2503.14000*).

---

## 1. Tóm Tắt Kết Quả Thống Kê Tổng Hợp (Executive Statistical Summary)

| Chỉ số Khoa học (Metric) | Baseline (Test4Py trên SLM) | Council Enhanced (Phương pháp đề xuất) | Mức Cải Thiện Thống Kê ($\Delta$) |
|---|:---:|:---:|:---:|
| **Pass Rate Trung bình** | 77.8% | **94.5%** | **+16.7%** (Vượt trội) |
| **Line Coverage (Mean $\pm$ Std)** | 38.69% | **48.79%** | **+10.11%** |
| **Branch Coverage (Mean $\pm$ Std)** | 23.83% | **25.09%** | **+1.26%** |
| **Độ Ổn Định Thực Thi (Execution Validity)**| 100.0% | **100.0%** | Tuyệt đối không crash cú pháp |

---

## 2. Bảng Phân Tích Thống Kê Chi Tiết Từng Đối Tượng ($N=3$ Trials)

| Subject ID | Phân Loại | Nhánh Đánh Giá | Pass Rate (%) | Line Coverage (Mean $\pm$ Std %) | Branch Coverage (Mean $\pm$ Std %) | Thời Gian TB (s) |
|---|---|---|:---:|:---:|:---:|:---:|
| `docstring_parser_parse` | Typed (Table 1) | Baseline | 100.0% (3/3) | 29.09 ± 0.00% | 5.88 ± 0.00% | 3.08s |
| `docstring_parser_parse` | Typed (Table 1) | **Council (Ours)** | **100.0%** (3/3) | **29.09 ± 0.00%** | **5.88 ± 0.00%** | 2.93s |
| `codetiming_timer` | Typed (Table 1) | Baseline | 100.0% (3/3) | 74.47 ± 12.94% | 39.58 ± 13.01% | 2.7s |
| `codetiming_timer` | Typed (Table 1) | **Council (Ours)** | **100.0%** (3/3) | **74.47 ± 0.00%** | **39.58 ± 3.61%** | 2.56s |
| `typesystem_schema` | Typed (Table 1) | Baseline | 0.0% (0/3) | 0.00 ± 0.00% | 0.00 ± 0.00% | 2.6s |
| `typesystem_schema` | Typed (Table 1) | **Council (Ours)** | **100.0%** (3/3) | **31.41 ± 0.59%** | **7.81 ± 1.23%** | 3.04s |
| `genty_repeat` | NA (Table 1) | Baseline | 67.0% (2/3) | 33.33 ± 28.87% | 33.33 ± 28.87% | 2.22s |
| `genty_repeat` | NA (Table 1) | **Council (Ours)** | **100.0%** (3/3) | **75.00 ± 21.65%** | **50.00 ± 0.00%** | 2.78s |
| `superstring` | NA (Table 1) | Baseline | 100.0% (3/3) | 38.03 ± 0.43% | 5.88 ± 0.00% | 2.26s |
| `superstring` | NA (Table 1) | **Council (Ours)** | **100.0%** (3/3) | **40.00 ± 5.88%** | **9.80 ± 6.80%** | 2.92s |
| `woa_whale_opt` | NA (Table 1) | Baseline | 100.0% (3/3) | 57.20 ± 19.96% | 58.33 ± 14.43% | 3.0s |
| `woa_whale_opt` | NA (Table 1) | **Council (Ours)** | **67.0%** (2/3) | **42.80 ± 37.07%** | **37.50 ± 32.48%** | 3.52s |

---

## 3. Kiểm Toán Ngân Sách Thực Tế (Budget Telemetry)
- **Tổng số lượt gọi LLM:** 38 calls
- **Tổng Tokens tiêu thụ:** **124,500** / 1,000,000 tokens (Chỉ chiếm **12.45%** hạn mức)
- **Chi phí thực tế phát sinh:** **$0.0325 USD** / $5.0000 (Chỉ khoảng vài xu Mỹ)
- **Thời gian suy luận toàn bộ:** 84.50 giây cho toàn bộ 36 lượt kiểm thử
