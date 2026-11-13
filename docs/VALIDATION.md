# Kiểm tra tại workspace — 2026-11-13

Đã triển khai source và kiểm tra trên Python **3.15.2** của máy hiện tại.
Môi trường này không phải môi trường notebook Python 3.10–3.12 đã hướng dẫn.

| Hạng mục | Kết quả thực tế |
|---|---|
| CLI `--help`, mode và tham số không hợp lệ | Pass |
| Parse AST của 11 file Python bàn giao | Pass |
| 8 unittest offline | Pass; xem `runs/offline-checks.txt` |
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

## Lệnh chạy tiếp trên Kaggle/Colab

Sau khi giải nén, đổi vào thư mục source, bật Internet/GPU, dùng Python 3.10–3.12:

```python
!python -m pip install -r requirements-notebook.txt
!python run.py --validate-only --output runs/validate-real
!python run.py --mode compare --rounds 1 --output runs/pilot-qwen-1b
```

`validate-real` phải pass hai test oracle nội bộ và kill hai mutant trước khi diễn giải
kết quả sinh test. Nếu validation không pass, xem `validation_process.json` và các JSON
trong `validation/`; không sửa oracle/pool sau khi nhìn kết quả từng cấu hình.
So sánh chính ở `runs/pilot-qwen-1b/comparison.json`, chi tiết từng mode ở `report.json`.
Dừng ở một hàm này trước khi mở rộng.
