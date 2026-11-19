# BÁO CÁO NGHIÊN CỨU CHUYÊN SÂU TRÌNH ĐỘ THẠC SĨ (BẢN HIỆN HÀNH: v17)

**Bản nghiên cứu chính thức: Tieu_Luan_CNPMTT_Council_SOTA_v17.docx**

- [Word Monograph v17](file:///home/heurix/Documents/Test4Py_Setup/reports/Tieu_Luan_CNPMTT_Council_SOTA_v17.docx)
- [PDF Rendered v17 (51 trang)](file:///home/heurix/Documents/Test4Py_Setup/reports/rendered/Tieu_Luan_CNPMTT_Council_SOTA_v17.pdf)
- [Báo cáo Đặc tả Thay đổi v17](file:///home/heurix/Documents/Test4Py_Setup/reports/Tieu_Luan_CNPMTT_Council_SOTA_v17.changes.md)
- [Biên bản Kiểm định và Toàn vẹn Học thuật](file:///home/heurix/Documents/Test4Py_Setup/reports/VALIDATION_v17.json)
- [Thư mục Biểu đồ Độ phân giải cao](file:///home/heurix/Documents/Test4Py_Setup/reports/Tieu_Luan_CNPMTT_Council_SOTA_v17_assets)

---

## Các Điểm Nâng cấp Trọng tâm trong Bản v17:
1. **Chuẩn mực Học thuật & Chiều sâu Kỹ thuật Phần mềm (Master's Level Rigor):**
   - Loại bỏ hoàn toàn các giải thích mã nguồn nội bộ (không có code walkthrough hay hướng dẫn lập trình).
   - Mô hình hóa bài toán hình thức, công thức toán học và hai thuật toán chuẩn mã giả (Pseudocode) cho Bao đóng AST $\mathcal{C}(f, M, B)$ và Hộp cát Đánh giá Pytest với Vòng lặp Sửa lỗi Chẩn đoán (Diagnostic Feedback).
   - Phân tích sâu sắc bài toán Test Oracle, các rào cản định kiểu động Python và Hiện tượng **"Ảo tưởng Độ phủ" (The Coverage Illusion)**.
2. **Phân loại 21 Dự án theo 3 Tầng Kỹ thuật Phần mềm (Engineering Tiers):**
   - **Tầng 1 (Hiệu quả cao / Tương thích thuận lợi: +6,5 pp đến +20,0 pp):** `docstring_parser`, `cookiecutter`, `sanic`, `python-string-utils`, `youtube-dl`, `thefuck` (mã thuần Python, hàm thuần túy, module hóa cao).
   - **Tầng 2 (Trung bình & Ổn định: -3,1 pp đến +6,1 pp):** `httpie`, `tqdm`, `pypara`, `tornado`, `flutes` (độ phức tạp trạng thái cao, I/O loop, socket).
   - **Tầng 3 (Suy biến Kỹ thuật / Thất bại Hệ thống - "Mổ xẻ thực nghiệm xấu"):** `PySnooper` (C-extensions `sys.settrace`), `dataclasses-json` (metaclass & MRO dynamic), `apimd` (AST visitor constraints), `isort` và `flutils` (Token Crowding & Context Distraction).
3. **Chất lượng Test Oracle và Khảo sát 187 Đột biến AST:**
   - Phân rã độ nhạy 4 họ toán tử: SIR (82,61%), AOR (33,33%), ROR (32,89%), BVR (0,00%).
   - Minh chứng phân kỳ giữa Độ phủ câu lệnh và Điểm đột biến qua hai ca đối lập `codetiming_timer` (80,85% coverage vs 20% MS) và `pycg_classes` (41,74% coverage vs 90% MS).
   - Duy trì kết quả ứng dụng mô hình 14B NF4 trên thư viện `genty`: 14/14 tests pass, coverage `genty_args` tăng 18/20 -> 20/20 dòng, tiêu diệt 2/2 đột biến hành vi.
4. **Hệ thống 5 Biểu đồ Đồ họa Mới (Publication-Grade Figures):**
   - Hình 3.1: Sơ đồ kiến trúc 4 giai đoạn của quy trình sinh và đánh giá kiểm thử.
   - Hình 4.1: Biểu đồ rừng (Forest Plot) ước lượng chênh lệch tỷ lệ chấp nhận và khoảng tin cậy 95%.
   - Hình 4.2: Phân loại thực nghiệm 21 dự án theo 3 Tầng Kỹ thuật Phần mềm.
   - Hình 4.3: Phân tích độ nhạy toán tử đột biến và Hiện tượng "Ảo tưởng Độ phủ".
   - Hình 4.4: Đánh đổi kinh tế giữa chi phí trên mỗi bộ test đạt và sản lượng kiểm thử hoàn chỉnh.
5. **Đặc tả Toàn diện Môi trường & Khả thi Kinh tế:**
   - Môi trường phần cứng: Kaggle Dual NVIDIA Tesla T4 (32GB VRAM) & Groq LPU.
   - Môi trường phần mềm: CPython 3.10.22, pytest 9.2.0, coverage.py 7.16.2, MutPy 0.6.1.
   - Chi phí thực tế: $1,425 USD trên toàn bộ 3.870 lượt chạy (dưới trần $3,00 USD); $0,311 USD / bộ test đạt chuẩn; độ trễ dưới 10 giây/lượt, sẵn sàng tích hợp CI/CD.

---

## Lưu ý về Bảo tồn Dữ liệu và Đa Agent:
- Toàn bộ các phiên bản trước (`v1` đến `v14`, và `v15` do agent song song thực hiện) được bảo tồn nguyên vẹn 100%, không bị sửa đổi hay ghi đè.
- Không có bất kỳ xung đột nào xảy ra trong codebase.
