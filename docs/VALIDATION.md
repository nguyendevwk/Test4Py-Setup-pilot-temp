# Kiểm tra tại workspace — 2026-11-13

Đã triển khai source và kiểm tra trên Python **3.15.2** của máy hiện tại.
Môi trường này không phải môi trường notebook Python 3.10–3.12 đã hướng dẫn.

| Hạng mục | Kết quả thực tế |
|---|---|
| CLI `--help`, mode và tham số không hợp lệ | Pass |
| Parse AST của các file Python bàn giao | Pass |
| 10 unittest offline | Pass; xem `runs/offline-checks.txt` |
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
