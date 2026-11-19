# Đóng góp hiện có và điều kiện để kết luận

Phần đã triển khai là API contract lấy từ AST production, phân biệt descriptor,
chữ ký và lexical owner của closure, kết hợp thay phần mô tả sinh sẵn bằng source
thật. Hai ablation tách việc thay source khỏi việc thêm facts. Đây là cơ chế có
thể kiểm thử và tái lập; chưa mặc nhiên là đóng góp nghiên cứu mới hoặc hiệu quả.

## Đối chiếu công trình trước

| Công trình, nguồn sơ cấp | Thành phần đã có | Hệ quả cho tuyên bố đóng góp |
|---|---|---|
| [Test4Py](https://arxiv.org/html/2503.14000v2) | Call-graph summaries, suy luận kiểu và iterative repair | Chỉ chuyển sang model nhỏ hoặc bổ sung context không tự chứng minh cải tiến |
| [CoverUp](https://arxiv.org/abs/2403.16218v4) | Kết hợp coverage, code context và error feedback | Không gọi vòng lặp feedback nói chung là cơ chế mới |
| [TestART](https://arxiv.org/abs/2408.03095v6) | Template-based repair kết hợp generation và coverage feedback | Cần đối chiếu cụ thể nếu thêm repair theo mẫu |
| [PANTA](https://arxiv.org/abs/2503.13580v2) | Phân tích tĩnh control flow và động coverage để hướng dẫn sinh test | Kết hợp static/dynamic nói chung chưa đủ phân biệt phương pháp |

Đây là đối chiếu sơ bộ theo mô tả của tác giả, không phải systematic literature
review hoặc xác nhận tính mới. Không so sánh trực tiếp số coverage công bố của
các paper với subset local có model, version, số vòng và acceptance gate khác.

## Bằng chứng hiện có

Development source-first-v2: 5 target, 2 module, 1 project, 1 seed; 15 lượt gồm
upstream prompt 0/5, source-only 2/5, source+facts 3/5 suite ổn định và có target
coverage. Facts giúp hai getter nhưng thua source-only ở closure. Chưa thể suy
từ số này ra lợi ích trên project khác. Getter assertions đã được review theo
source; pool mutant cũ không có mutant đủ điều kiện cho getter, nên không gán
fault score bằng 100% hoặc 0% cho chúng.

Tập độc lập giữ nguyên 12 module/bốn project, ba seed, 72 lượt. Control là source
thật, khác biệt duy nhất là API facts. Đây là kiểm chứng thành phần, không phải
toàn pipeline Test4Py. Prompt/source/budget/scoring đã khóa trước inference.
Mọi lỗi và target khó phải còn trong kết quả. Kết luận phải dựa vào report cuối,
không dựa vào một vài lượt pass và không xem lặp seed là project độc lập.

Bộ ứng dụng riêng có cải thiện đã đo: giữ nguyên 12 test cũ và thêm hai test model
không chỉnh sửa; 14/14 pass trong ba process, genty_args line 18/20 lên 20/20.
Hai lỗi iterator bổ sung sống sót ở bộ cũ và bị bộ mới phát hiện. Đây là extension
được chọn để dùng, với fault phát triển chọn sau review; không dùng nó làm kết
quả xác nhận phương pháp hay bài báo. Evidence và giới hạn nằm trong
`research/application/14b_genty_extended_20261117/`.

## Điều còn thiếu

Muốn kết luận cơ chế tốt hơn, cần lợi ích trên target/project ngoài phát triển,
assertions đúng và khả năng phát hiện lỗi phù hợp, cùng chi phí/budget. Tăng
coverage do bỏ test hoặc làm yếu oracle không đạt tiêu chí. Chênh lệch không có
ý nghĩa rõ không chứng minh tương đương; muốn nói 7B ngang 14B phải có phép đo
riêng và biên tương đương khóa trước. Chưa có thực nghiệm 7B ở cohort này.

Các lỗi setup/cache/fixture và helper context còn thiếu cho thấy API shape không
đủ mô tả trạng thái hợp lệ. Hướng cần đánh giá tiếp, nếu component hiện tại không
tổng quát hóa, là source slice có dependency cần thiết và kiểm chứng setup bằng
việc gọi đúng target, hoàn tất bình thường trên production. Đây mới là giả thuyết
tiếp theo, chưa có kết quả và chưa được chứng minh mới so với prior art. Không
đổi cơ chế giữa cohort held-out để làm số liệu đẹp hơn; các thay đổi dựa vào kết
quả này sẽ cần tập xác nhận mới.
