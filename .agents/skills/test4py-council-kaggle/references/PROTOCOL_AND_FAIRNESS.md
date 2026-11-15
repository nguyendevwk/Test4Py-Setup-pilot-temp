# Quy Chuẩn Thực Nghiệm & Ranh Giới Khoa Học (Scientific Protocol)

Tài liệu này xác định các ranh giới đạo đức nghiên cứu, phương pháp luận và cách tuyên bố đóng góp khoa học (Paper Claims) cho bài báo.

---

## 1. Ranh Giới Đối Chứng (Comparative Integrity)

1. **Định danh chính xác Baseline**:
   * Cột `baseline` trong Council Runner là **"Council Generator nhưng KHÔNG CÓ SETUP CONTEXT"**.
   * Đây là đối chứng ablated control (Ablation Study) nhằm chứng minh giá trị nhân quả của việc cung cấp Setup.
   * **KHÔNG ĐƯỢC** đánh đồng `baseline` của Council với toàn bộ pipeline gốc của bài báo Test4Py (`run.py` / `worker.py`). Muốn so sánh với bài gốc, phải chạy riêng pipeline upstream bằng `benchmark19.py`.

2. **Ranh giới về Mutation Score**:
   * Hai mutants hiện tại trong target `get_custom_loader` là 2 mutants logic minh họa (`new_path_wrong` và `existing_path_overwritten`).
   * Điểm Mutation Score 1.0 nghĩa là diệt được **2/2 mutants minh họa này**, tuyệt đối không tuyên bố là *"Đạt 100% Mutation Score toàn diện hơn bài gốc"*.

3. **Báo cáo trung thực về Scope Coverage**:
   * Phải phân biệt rõ ràng giữa **Module Branch Coverage** (độ phủ toàn bộ file `imports.py`) và **Target + Nested Branch Coverage** (độ phủ trực tiếp trong `get_custom_loader` và closure `CustomLoader`).

---

## 2. Tiêu Chuẩn Thống Kê (Statistical Rigor)

1. **Loại bỏ lặp tất định (Greedy Duplication)**:
   * Chạy $N=10$ hay $N=30$ với `temperature=0.0` (greedy) chỉ là lặp lại cùng 1 sample, không có ý nghĩa thống kê độc lập.
   * Luôn bật `--temperature 0.7` với seed tăng dần (`seed + idx`) để tạo phân phối xác suất thực tế.
2. **Kiểm định Giả thuyết (Hypothesis Testing)**:
   * Áp dụng **Wilcoxon Signed-Rank Test** (phi tham số) để kiểm tra mức độ chênh lệch có ý nghĩa thống kê ($p < 0.05$ hoặc $p < 0.01$).
   * Tính **Cliff's Delta ($\Delta$)** hoặc **Vargha-Delaney $\hat{A}_{12}$** để báo cáo kích thước hiệu ứng (Effect Size).

---

## 3. Định Vị Đóng Góp Cho Bài Báo (Paper Claims)

### Những phát biểu KHÔNG ĐƯỢC PHÉP:
* ❌ *"Hệ thống tự động sinh setup tổng quát cho toàn bộ 183 modules của Test4Py."*
* ❌ *"Thay thế hoàn toàn GPT-4o với kết quả vượt trội trên mọi phương diện."*

### Những phát biểu ĐƯỢC PHÉP VÀ CÓ GIÁ TRỊ CAO:
* ✅ **Chỉ ra điểm nghẽn của SLM**: Các mô hình nhỏ (7B/14B) bị tê liệt hoàn toàn (0% coverage) khi đối mặt với các API phụ thuộc trạng thái (Stateful APIs) nếu không có Setup Context.
* ✅ **Đề xuất kiến trúc Execution-Verified Setup**: Cơ chế trích xuất chuỗi thao tác sản phẩm và kiểm chứng động bằng runtime micro-probes trước khi sinh test, giúp đưa coverage từ 0% lên 34.78% và diệt 100% mutants logic.
* ✅ **Hiệu quả kinh tế ($0 Cost)**: Đạt được năng lực sinh regression test chất lượng cao trên phần cứng miễn phí (Kaggle Dual-T4) thông qua mô hình MoA (Coder 14B + Critic 4B) và 4-bit NF4, với chi phí probe chỉ chiếm < 0.21% tổng thời gian.
