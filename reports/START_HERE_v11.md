**Bản hoàn thiện mới nhất: Tieu_Luan_CNPMTT_Council_SOTA_v11.docx**

- [Word v11 (Bản hoàn thiện kiến trúc & bố cục)](Tieu_Luan_CNPMTT_Council_SOTA_v11.docx)
- [PDF v11](rendered/Tieu_Luan_CNPMTT_Council_SOTA_v11.pdf)
- [Word v10 (Bản đối soát thực nghiệm đã khóa)](Tieu_Luan_CNPMTT_Council_SOTA_v10.docx)
- [PDF v10](rendered/Tieu_Luan_CNPMTT_Council_SOTA_v10.pdf)
- Toàn bộ các phiên bản trước (v1 đến v10) và file gốc Downloads được giữ nguyên 100% để truy vết.

14B NF4/Kaggle là công trình đã thực thi: giữ log bộ nhớ, cold timeout,
warm-prefix, kết quả âm và kiểm thử thật. Chuyển sang Groq/GPT-OSS-20B vì
hạn chế vận hành/tiến độ là thay đổi backend và model, không phải bỏ giai đoạn cũ
hoặc đối chứng chất lượng chéo model.

Ứng dụng 14B: 12 test baseline được giữ nguyên; thêm hai test nguyên văn từ
lần sinh 14B có thật. Bộ 14 test replay 14/14 trong ba process mới; genty_args
18/20 → 20/20 dòng. Hai mutant iterator lịch sử: bộ cũ 0/2, bộ mới 2/2 killed.
Đây là bộ ứng dụng tuyển chọn và mutant hậu kiểm, không phải hiệu quả toàn thuật toán.

Đợt Groq bổ sung theo module frame công bố của CodaMOSA hoàn tất204/204 lượt,
34 target/12 project: source32/102, setup34/102. Bốn project đã dùng ở lịch sử105
lượt; tám project còn lại mở rộng ngoài tập đó và các cohort Groq trước.
Chênh lệch cân bằng12 project +1,85 điểm phần trăm, bootstrap95% [-6,48;10,19],
p sign-flip0,84375: chưa đủ bằng chứng khẳng định ưu thế thống kê.
66/66 artifact đạt tiêu chí replay độc lập và khớp coverage.

Screen cải tiến ngữ cảnh helper/AST+setup trên cùng tập đã quan sát:68/68 lượt,
source11/34 vs cải tiến12/34; SC17,50% vs19,52%;23/23 artifact replay khớp.
Đây là phát triển, không cộng thành mẫu xác nhận độc lập. Đợt9 project trước
(28/81 vs36/81, CI95% chứa0) và screen cap108 lượt vẫn giữ riêng.

Sáu cohort Groq gồm632 lượt mô hình, không phải632 quan sát độc lập.
Ngân sách theo sổ phân bổ bảo thủ0,605180 USD trong trần3 USD; usage có response
ước tính0,158223 USD, không phải hóa đơn và không cộng thành hai khoản chi.

Tái lập: [hướng dẫn](../research/REPRODUCIBILITY_GROQ.md). Lưu raw request/response,
pytest, coverage, source hashes, ledger, trạng thái lỗi và kế hoạch phân tích.
Gói bằng chứng hiện hành: ../deliverables/council_repro_20261119_v4.zip.
