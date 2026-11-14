# Chạy lại Council sau kiểm định

Đây là phiên bản thực nghiệm mới, chưa có kết quả GPU. Không ghép bảng cũ với v2.
Giữ nguyên artifact cũ để audit. Mỗi lần chạy/batch tạo thư mục mới.

## Chuẩn bị

Dùng môi trường modern hiện có theo README; cài dependencies **trước** chạy:

```bash
python -m pip install -r requirements-modern.txt
python -m pip install bitsandbytes
```

Chỉ cần bitsandbytes nếu dùng NF4. Runner không tự cài package trong lúc thực nghiệm
và không âm thầm fallback từ NF4 sang FP16. Lưu phiên bản môi trường trong summary.
Môi trường phải có GPU phù hợp và mạng để tải model/checkout PyCG.

## Kiểm tra offline

```bash
python -m unittest discover -s tests -v
python council_runner.py --mock --samples 2 --output runs/council_v2_mock
```

Mock không tải model/repo, không chạy scorer, không có tỷ lệ pass/coverage/mutation
hiệu quả. Compiler ghi lý do loại mock khỏi bảng. JSON cũ/JSON lỗi cũng được liệt kê.

## Chạy thật một cấu hình

```bash
python council_runner.py --mode council --samples 2 \
  --coder-model Qwen/Qwen2.5-Coder-14B-Instruct \
  --critic-model Qwen/Qwen3-4B-Instruct-2507 \
  --load-in-4bit --max-new-tokens 2048 --seed 42 \
  --output runs/council_v2_real
```

Đây là 2 lượt sinh greedy của **một** target, không phải 2 target độc lập. Ban đầu
nên chạy ít lượt để phát hiện lỗi môi trường. `--samples` chỉ đổi số lượt lặp.
`--coder-revision` và `--critic-revision` nhận SHA/revision; mặc định `main` được resolve
một lần mỗi model load thành SHA bất biến, tokenizer và model dùng cùng SHA.
Khi chạy lại để so trực tiếp, dùng SHA trong `summary.json`/`engine.json` của lượt trước.

Modes: `baseline` không setup, `caller` caller sản phẩm, `extracted` lấy ứng viên đầu,
`ranked` xếp hạng tĩnh theo số thao tác được trích, `verified`/`council` probe rồi chọn.
Ranked không probe nhưng vẫn là heuristic đơn giản; không tuyên bố static control tối ưu.
Verified thiếu witness sẽ ghi `setup_incomplete`, không gắn nhãn verified rồi tiếp tục.

Mặc định tối đa một repair cho mọi suite chưa all-pass, kể cả mixed-pass hoặc lỗi syntax;
timeout không kích hoạt repair. `--no-repair` không nạp model Critic.
`--repair-with coder` dùng cùng Coder cho một lượt self-repair, cũng không nạp Critic.
Không gọi repair thêm lần để cứu một arm sau khi đã thấy kết quả.

## Ablation và tổng hợp

```bash
python ablation_runner.py --variant all --samples 2 \
  --max-new-tokens 2048 --seed 42 --output runs/ablation_v2
python ablation_runner.py --compile --output runs/ablation_v2
```

`all` gồm full, không setup, không repair, self-repair, extracted, ranked, caller,
7B và 3B. Batch xáo thứ tự theo seed, lưu thứ tự và tái sử dụng SHA đã resolve cho cùng
model trong batch. Không xem shuffled order là đã loại bỏ hết nhiễu timing.
Cùng token cap không đồng nghĩa cùng compute; báo thêm input/output tokens và probes.
Thay model là yếu tố riêng; không gọi mọi chênh lệch là lợi ích verification.

Compiler chia bảng theo cohort (source/prompt/scorer/settings/seed/token cap/NF4).
Mỗi hàng là một run, không pooling nhiều cohort. Mẫu số pass là planned; trung bình
coverage/mutation có `n/planned` riêng. Module và target+nested coverage được báo riêng, không cộng chồng arcs của hàm cha/con. Module coverage 0 được giữ; không có branch
thì NA. Metric của score incomplete là NA; lý do thiếu phải còn trong bảng.
Dữ liệu cũ không có schema v2 bị loại kèm cảnh báo, không tự chuyển đổi.

## Artifact phải xem

- `manifest.json`, `summary.json`, `engine.json`: cấu hình, SHA, source hashes, môi trường,
  planned/finished, lỗi run, model load và telemetry.
- `model_calls.jsonl`: role, sample, prompt đầy đủ, output thô, input/output tokens,
  truncation và thời gian (mock tokens là null).
- `samples/*/result.json`: first/final suite pass, audit trước/sau, stages, score status,
  mutant pool hash/verdict và loader trace.
- `test_candidate_v1.py`, `test_candidate_v2_repaired.py`, `test_final.py`: mọi phiên bản
  code đã trích xuất; output không trích được vẫn có trong raw log.
- `original`, `eligible_original`, `mutant_*`, `score.json`: bằng chứng pytest/coverage.

Repair bị từ chối nếu mất tên test, giảm số check hoặc tăng assertion literal-true.
Mọi assertion bị đổi vẫn được ghi và yêu cầu review: gate cú pháp không chứng minh
bảo toàn ý nghĩa, không phát hiện hết `.endswith`, mock quá mức hay assertion yếu.
Scorer chỉ dùng original-passing nodes cho coverage và mutants; báo all-suite pass riêng.
Generated tests làm thay đổi file nguồn Python sản phẩm khiến điểm bị từ chối.

Chỉ dùng raw artifacts v2 sau khi review để viết kết quả. 2/2 mutant là hai ví dụ
filepath, không phải toàn bộ không gian lỗi. Target adapter đã được tuning nên cần
held-out projects và protocol xác nhận riêng để tuyên bố tổng quát.
