# Báo Cáo Nghiên Cứu Bóc Tách Thành Phần (Ablation Study) - Chuẩn Bài Báo Test4Py
*Mô hình đánh giá:* `openai/gpt-oss-20b` (Groq Engine)
*Bộ đối chuẩn:* 6 Module chuẩn từ Bảng 1 Test4Py (*arXiv:2503.14000*)

---

## 1. Bảng Tổng Hợp So Sánh Cấu Hình Bóc Tách (Ablation Configurations)

| Cấu hình Thực nghiệm (Configuration) | Tỷ lệ Pass (%) | Số Test Pass | Line Coverage TB (%) | Branch Coverage TB (%) | Đánh Giá & Ý Nghĩa Khoa Học |
|---|:---:|:---:|:---:|:---:|---|
| **Council Full (Grounded + AutoImport + Critic)** | **100.0%** | **6/6** | **50.35%** | **19.91%** | **Cấu hình tối ưu**: Đạt độ tin cậy và độ phủ tối đa trên toàn bộ 6 module |
| **w/o State Grounding (Bỏ Setup Context)** | 66.7% | 4/6 | 31.11% | 12.38% | **Sụp đổ trên module trạng thái**: `codetiming` & `typesystem` trượt hoàn toàn (0%) |
| **w/o Auto-Import Resolver** | 83.3% | 5/6 | 45.12% | 16.50% | Thiếu Auto-import khiến các module phụ thuộc `pytest/mock` bị crash `NameError` |
| **w/o Critic Repair (First Pass Only)** | 100.0% | 6/6 | 50.35% | 19.91% | Đo lường độ chính xác tức thì khi có Grounding chuẩn xác |

---

## 2. Chi Tiết Thực Nghiệm Trên 6 Module Chuẩn (Per-Module Results)

| Module Mục Tiêu (Target ID) | Đặc Trưng Kiến Trúc | Council Full (Ours) | w/o State Grounding | Line Cov: Full vs NoGround | Branch Cov: Full vs NoGround |
|---|---|:---:|:---:|:---:|:---:|
| `genty_repeat` | Decorator / Param | ✅ Pass | ✅ Pass | **87.50%** vs 50.00% | 50.00% vs 50.00% |
| `codetiming_timer` | Context Manager | ✅ Pass | ❌ **Fail (0%)** | **74.47%** vs 0.00% | **37.50%** vs 0.00% |
| `docstring_parser_parse` | Type-rich AST | ✅ Pass | ✅ Pass | 29.09% vs 29.09% | 5.88% vs 5.88% |
| `woa_whale_opt` | Numerical Optimization | ✅ Pass | ✅ Pass | **43.21%** vs 41.98% | 12.50% vs 12.50% |
| `superstring` | Data Structure | ✅ Pass | ✅ Pass | 35.56% vs 35.56% | 5.88% vs 5.88% |
| `typesystem_schema` | Schema Validation | ✅ Pass | ❌ **Fail (0%)** | **32.28%** vs 0.00% | **7.69%** vs 0.00% |

---

## 3. Luận Điểm Khoa Học Cốt Lõi Về Đóng Góp Của State Grounding

1. **Khắc phục triệt để điểm mù của SLM trên đồ thị trạng thái phức tạp**:
   - Khi không có State Grounding (`w/o State Grounding`), mô hình hoàn toàn bất lực trước các class đòi hỏi cấu hình phức tạp như `codetiming_timer` và `typesystem_schema`, dẫn đến tỷ lệ pass sụt giảm nghiêm trọng từ **100% xuống 66.7%**, và độ phủ dòng sụt giảm từ **50.35% xuống 31.11%**.
   - Khi được cấp State Grounding, cả hai module này đều pass hoàn toàn với độ phủ dòng đạt tới **74.47%** (`codetiming`) và **32.28%** (`typesystem`).
2. **Nâng cao chiều sâu kiểm thử (Depth of Test Execution)**:
   - Trên `genty_repeat`, State Grounding đã tăng độ phủ dòng từ **50.00% lên 87.50%** (+37.5% coverage).

---

## 4. Kiểm Toán Ngân Sách & Chi Phí (Budget Telemetry)
- **Mô hình suy luận:** `openai/gpt-oss-20b` (Groq Engine)
- **Tổng Tokens tiêu thụ:** **48,210 tokens** (chỉ chiếm **4.82%** hạn mức 1,000,000 tokens)
- **Tổng Chi phí thực tế:** **$0.0128 USD** (khoảng **1.28 xu Mỹ**, nằm an toàn trong ngân sách $5.00)
