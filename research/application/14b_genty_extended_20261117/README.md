# Bộ test genty mở rộng từ kết quả 14B thật

Giữ nguyên từng byte của hai file chứa12test cũ, thêm nguyên văn hai test mới
từ arm source-first+API facts. Không sửa assertion, bỏ test hoặc sửa production.
Đây là bộ test ứng dụng được chọn từ development, không phải tỷ lệ thành công
của phương pháp trên benchmark. Cohort phát triển có3/5suite API-contract đạt
tiêu chí; các lỗi khác được giữ trong archive nghiên cứu.

Project genty commit `85f7c960a2b67cf9e58e0d9e677e4a0bc4f05081`.
Model sinh test mới: Qwen2.5-Coder-14B-Instruct NF4 revision
`aedcc2d42b622764e023cf882b6652e646b95671`. Nguồn model/candidate/hash
được lưu ở manifest.json; hai file cũ giữ provenance baseline riêng.

Trong thư mục bundle, với checkout genty ở `/path/to/genty` và Python đã có
pytest/six, chạy:

```bash
PYTHONPATH=/path/to/genty python -m pytest -o addopts= test_genty_genty_args_tgenty_args0.py test_genty_genty_repeat_tgenty_repeat0.py selected_tests -q
```

Kiểm chứng local Python3.12, ba process mới:14/14pass, cùng node sets;
0,912/0,860/0,866giây gồm pytest+coverage, không gồm sinh LLM. Không kết luận
nhanh hơn bộ cũ từ các thời gian ngắn này. Production hashes không đổi.

| Chỉ số | Bộ cũ12test | Bộ mở rộng14test |
|---|---:|---:|
| genty_args line |18/20|20/20|
| genty_args branch |NA(0/0)|NA(0/0)|
| genty_repeat line |8/8|8/8|
| genty_repeat branch |2/2|2/2|
| Hai lỗi iterator bổ sung phát hiện |0/2|2/2|

Hai lỗi bổ sung là bỏ format positional args và đảo thứ tự kwargs khi iterate.
Chúng được chọn sau khi review test phát triển, khác pool mutant khóa ban đầu.
Đây là kiểm tra regression cho ứng dụng này; không dùng làm bằng chứng xác nhận
vượt paper hoặc tổng quát hóa. Cả hai suite được chạy cùng source/interpreter
và cùng hai fault; không chỉ chạy test thuận lợi. Evidence đầy đủ ở
verification.json và verification-evidence.zip. Chưa kiểm tra toàn bộ vòng đời
class-decoration/test-runner của genty hoặc mọi kiểu dữ liệu iterator.
