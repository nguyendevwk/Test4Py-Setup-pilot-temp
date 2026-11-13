# Kiểm tra tại workspace — 2026-11-13

Đã triển khai source và kiểm tra trên Python **3.15.2** của máy hiện tại.
Môi trường này không phải môi trường notebook Python 3.10–3.12 đã hướng dẫn.

| Hạng mục | Kết quả thực tế |
|---|---|
| CLI `--help`, mode và tham số không hợp lệ | Pass |
| Parse AST của các file Python bàn giao | Pass |
| 21 unittest offline | Pass; xem `runs/offline-checks.txt` |
| Ghim checkout Git và từ chối commit sai | Pass trên repo fixture cục bộ |
| Hai trạng thái, thứ tự ứng viên, fresh-process/object, budget/timeout | Pass trên fixture nhỏ có nhãn rõ |
| Hai operator mutant và logic chỉ chấm test pass bản gốc | Pass trên fixture/mock, chưa chạy pytest thật |
| Một arm lỗi vẫn chạy cả các arm sau | Pass bằng worker mô phỏng |
| Checkout Test4Py/PyCG thật | Bị chặn bởi DNS `Could not resolve host: github.com` |
| PyCG thật + probe thật + pytest/coverage/mutation thật | Chưa chạy được do không checkout được và thiếu dependencies |
| Vòng sinh test SLM thật | Chưa chạy được |

`torch`, `transformers`, `pytest`, `coverage`, `pytest_jsonreport` đều chưa cài.
Máy có executable `nvidia-smi`, nhưng lệnh query thất bại vì không liên lạc được với
NVIDIA driver. Do đó chưa xác nhận được CUDA/GPU hoạt động, không báo đã chạy GPU.

Đã thực sự gọi:

```bash
python run.py --validate-only --output runs/local-real-validation
python run.py --mode compare --rounds 1 --output runs/local-compare-attempt
```

Cả hai kết thúc `preflight_failed`, exit 1 tại fetch upstream.
Log nguyên nhân, traceback, cấu hình được giữ tại:

- `runs/local-real-validation/comparison.json`
- `runs/local-compare-attempt/comparison.json`
- `runs/environment.json`

Đã đọc trực tuyến bốn module Test4Py ở commit được yêu cầu, requirements upstream,
README chính thức và paper arXiv v2 để thiết kế adapter. Đọc trực tuyến không đồng nghĩa
với đã checkout/chạy toàn pipeline. Chưa có số coverage hoặc mutation score nghiên cứu;
không dùng kết quả fixture thay cho kết quả target thật.

## Bản sửa Kaggle Python 3.13

Theo log người dùng, notebook dùng Python 3.13 và pip báo xung đột tokenizers.
Đã đổi Transformers 4.46.3 + tokenizers 0.20.3, thêm bootstrap Python 3.11.11/Torch
2.5.1 cu121 tách khỏi kernel. Bootstrap có `pip check` và smoke check Chroma để
kiểm chứng dependency thực tế trước khi chạy pipeline.

Đã thêm kiểm tra offline cho output tồn tại: giữ log cũ, tạo sibling mới; kiểm tra
bootstrap dry-run không tạo môi trường/không tải gì. Đã thử `uv pip compile` nhưng bị lỗi DNS khi truy cập PyPI (`pypi.org/simple/astor/`).
Chưa khẳng định pip resolver,
bootstrap CUDA hoặc pipeline PyCG thật đã pass khi mạng tại máy này còn bị chặn.

## Lệnh chạy tiếp trên Kaggle

```python
%cd /kaggle/working/Test4Py-Setup-pilot-temp
!python -m pip install uv==0.6.17
!python bootstrap_kaggle.py --venv /tmp/test4py-venv --report-dir /kaggle/working/pilot-environment
!/tmp/test4py-venv/bin/python run.py --validate-only --output /kaggle/working/validate-real
```

Sau khi validation báo complete:

```python
!/tmp/test4py-venv/bin/python run.py --mode compare --rounds 1 --output /kaggle/working/pilot-qwen-1b
```

Nếu đã có output, xem đường dẫn mới được in ở `Reports:`. `comparison.json` nằm
trong đường dẫn đó. Không dùng Python 3.13 của notebook để chạy trực tiếp stack cũ.

## Profile modern (chưa kiểm chứng tích hợp)

Thêm `bootstrap_modern.py`, `requirements-modern.txt` và `--runtime modern` để
thử Python 3.13 với thư viện mới. Kiểm tra offline xác nhận dry-run không tạo venv,
không lên kế hoạch cài Torch và dùng interpreter hiện tại. Profile này tái dùng
Torch/CUDA từ image Kaggle; cần ghi nhận image và môi trường thực tế. Chưa chạy
pip resolver/import/model/upstream thực tế ở profile modern do giới hạn mạng.

## Sửa cú pháp uv và thứ tự chạy Kaggle

Người dùng đã tái hiện lỗi parser trên uv 0.6.17 vì giá trị `--only-binary` chứa
nhiều tên cách nhau bằng dấu phẩy. Hai bootstrap giờ dùng cờ lặp cho từng package.
Đối chiếu source parser tại tag 0.6.17 và tài liệu CLI uv. Regression test thực thi
uv cục bộ (0.13.5), cài wheel fixture ở chế độ offline/dry-run, pass cả hai bootstrap.
Chưa chạy được binary 0.6.17 tại workspace vì tải release bị lỗi DNS.

Theo docs Kaggle, source và report ở `/kaggle/working`, venv/cache ở `/tmp`, bootstrap
phải chạy lại trong session Save & Run All. `kaggle_run.py` điều phối từng bước,
dừng nếu bootstrap/validation thất bại và giữ log process. Test lỗi bootstrap và
lỗi validation xác nhận comparison không bị chạy tiếp. Test log xác nhận stdout
và stderr được lưu. Validation worker lỗi giờ in phần cuối traceback ra CLI.

## Tiến độ và multi-GPU

Thêm streaming stdout vào notebook + log file, heartbeat, event JSON, token/giây,
VRAM allocated/reserved và telemetry nvidia-smi. Scheduler chạy các arm trong process
riêng, tối đa một arm cho mỗi GPU slot. Test concurrency dùng barrier hai thread,
chứng minh hai slot có thể hoạt động cùng lúc, một lỗi không chặn các arm khác và
không có hai arm trùng slot. Test CUDA visibility dùng UUID kế thừa. Test streaming
chứng minh dòng đầu xuất hiện trước khi process kết thúc, log giữ đủ và timeout
kết thúc process. Chưa có hai GPU hoạt động tại workspace để đo tốc độ hay peak VRAM
thực tế; không báo hệ số tăng tốc thực nghiệm.

## Bằng chứng Kaggle và giảm tải output

Theo log người dùng cung cấp ngày 2026-11-14: Python 3.13.16, Torch 2.11 cu130,
Transformers 4.57.6, Chroma 1.3.5 đã qua smoke check; validation PyCG thật pass hai
trạng thái và bộ chấm hai mutant oracle nội bộ. Hai worker trên GPU 0/1 đã nạp
model (2.88 GiB mỗi worker trước embedding). Chưa nhận báo cáo generated-test
coverage/mutation cuối cùng nên không kết luận chất lượng hay tăng tốc.

Bỏ in toàn bộ package metadata ra console, chuyển sang file JSON. Thêm console
compact/quiet và limiter; test với 1000 dòng xác nhận browser chỉ nhận tối đa
ngưỡng cấu hình + một thông báo, raw log vẫn đủ 1000 dòng. Dashboard chỉ dùng một
DisplayHandle và update định kỳ, không tích lũy các bảng. Test fake display xác
nhận tạo một handle, update nhiều lần; test tail đọc có giới hạn và HTML được escape.
Chưa kiểm tra trực tiếp DOM của frontend Kaggle tại workspace này.
