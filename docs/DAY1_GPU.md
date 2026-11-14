# Ngày 1: kiểm tra pipeline GPU sau audit

Mục tiêu: kiểm tra end-to-end, không đo ưu thế nghiên cứu. Chạy đúng một sample;
không tăng số lượt để tìm kết quả đẹp. Giữ cả trường hợp fail và artifact.

## Kaggle

Bật GPU và Internet; giải nén gói source, chuyển cwd tới thư mục có `bootstrap_modern.py`.
Các lệnh shell dưới đây dùng interpreter Kaggle có sẵn CUDA Torch:

```bash
python -m pip install uv==0.6.17
python bootstrap_modern.py --venv /tmp/test4py-modern --report-dir /kaggle/working/day1-environment
uv pip install --python /tmp/test4py-modern/bin/python bitsandbytes
/tmp/test4py-modern/bin/python -m unittest discover -s tests -v
/tmp/test4py-modern/bin/python run.py --runtime modern --validate-only --output /kaggle/working/day1-validation
```

Dừng nếu bước nào lỗi; giữ log, không tiếp tục chấm chất lượng trong môi trường lỗi.
Validation dùng oracle viết tay kiểm tra hạ tầng; không được đưa số của nó vào
bảng generated tests.

Sau khi validation pass, chạy một cấu hình đã chọn trước:

```bash
/tmp/test4py-modern/bin/python council_runner.py --mode verified --samples 1 \
  --coder-model Qwen/Qwen2.5-Coder-14B-Instruct \
  --critic-model Qwen/Qwen3-4B-Instruct-2507 \
  --load-in-4bit --no-repair --max-new-tokens 2048 --seed 42 \
  --output /kaggle/working/day1-verified
```

Chỉ nạp Coder; tạm tắt repair để kiểm tra rõ lần sinh đầu và giảm số thành phần.
Đây là kiểm tra kỹ thuật, không phải phép so sánh hay minh chứng cơ chế có lợi.
Không tự thay model/budget/prompt sau khi thấy fail mà giữ nguyên tên cohort.

## Đọc kết quả và quyết định tiếp

1. Kiểm tra `summary.json`: `mock=false`, `run_kind=real`, SHA model, source hashes,
   planned/finished và lỗi. `complete` chỉ nghĩa hoàn tất quy trình, chưa chắc test tốt.
2. Kiểm tra `selection.json`, `probes.jsonl`: hai scenario có witness, không lẫn
   probe observation vào prompt trong `model_calls.jsonl`.
3. Đọc `test_candidate_v1.py`/`test_final.py`, pytest và loader trace: có đi tới
   loader, kiểm tra hành vi thực, không chỉ `assert True`, mock toàn bộ hoặc skip.
4. Đối chiếu target+nested coverage với module coverage; kiểm tra từng mutant verdict,
   không đọc 2/2 là khả năng phát hiện mọi lỗi.
5. Nếu lỗi môi trường/scorer: sửa hạ tầng và tạo phiên bản/lượt mới; giữ log cũ.
   Nếu test sinh sai: đó là outcome phải lưu, không tự coi là pipeline hỏng.

Sau khi artifact được audit, mới khóa ba arm cùng model/budget/repair:
`baseline`, `ranked`, `verified`. Pin `--coder-revision` theo SHA lượt đầu.
Trước đánh giá xác nhận phải tách target phát triển khỏi target đánh giá.

Xuất nguyên thư mục `day1-verified`, `day1-validation` và `day1-environment` từ
Kaggle để kiểm tra; không chỉ giữ ảnh tỷ lệ pass. Gói source chứa
`SOURCE_SNAPSHOT.json` để đối chiếu file trước upload.
