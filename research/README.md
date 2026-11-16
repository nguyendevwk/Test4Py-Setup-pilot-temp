> **Công việc hiện hành:** [upstream paired pilot 14B NF4](../docs/UPSTREAM_NF4_PILOT.md); xem quyết định R5 trong nhật ký. Kết quả Council v4 không thay cho đối chứng upstream.

> **Nhật ký hiện hành:** [NHAT_KY_NGHIEN_CUU.md](NHAT_KY_NGHIEN_CUU.md). Kaggle v3 có 0/6 suite all-pass; v4 có 3/8 final all-pass (first-pass 1/8). Xem R4 để đánh giá hallucination, test quality và giới hạn suy luận. Các giới hạn và đính chính ở [sổ tay](SO_TAY_HIEN_HANH.md).

# Bộ đánh giá nghiên cứu

- `REVIEW.md`: đánh giá đóng góp, đối chiếu paper, audit thiết kế, RQ, thống kê và ứng dụng.
- `METRICS.csv`: định nghĩa chỉ số, mẫu số, nguồn dữ liệu và chỉ số còn thiếu instrumentation.
- `protocol.json`: proposal minh bạch; chưa phải thí nghiệm đã thực hiện.

Kết quả Kaggle chưa hoàn tất: không có số nào ở đây chứng minh verified vượt baseline.
Các fixture trong `tests/test_research.py` chỉ kiểm tra logic thống kê/collector, không phải dữ liệu thực nghiệm.

Nếu chưa có artifact, dùng `run_research.py` hoặc `pilot.notebook.run_research()`
để tự chạy pipeline và tạo kết quả thật, sau đó tự gọi phân tích và tạo `results.zip`.
Không cần `--input` có sẵn. File `pilot-data.json` mô tả input; không chứa số kết quả
bịa/synthetic. Hướng dẫn cell đầy đủ ở README gốc. Các lệnh bên dưới dành cho trường
hợp đã có artifact và chỉ muốn phân tích lại.

Phân tích dùng Python hiện tại của notebook (`sys.executable`), không cần venv GPU
trong `/tmp`. Venv tạm có thể mất giữa các session. Sau khi một lượt chạy hoàn tất,
phân tích ngay trên Kaggle để không cần tải log lớn vào cell:

```python
import subprocess
import sys
subprocess.run([
    sys.executable, 'analyze.py',
    '--input', 'auto',
    '--output', '/kaggle/working/pilot-research-report', '--plots',
], cwd='/kaggle/working/Test4Py-Setup-pilot-temp', check=True)
```

`--input auto` tìm artifact mới nhất trong `/kaggle/working` và `/kaggle/input`,
không chọn theo điểm chất lượng; loại validation-only khỏi auto-selection. Dùng
`--list-runs` để xem các đường dẫn và `--input PATH` để chọn chính xác. Có thể chỉ định
`--search-root PATH` khi output đã được gắn qua Add Input. Search có giới hạn độ sâu
và số thư mục, bỏ qua checkout/cache để tránh quét dữ liệu rất lớn.

Nếu không có artifact: source repo không chứa kết quả Kaggle của bạn. Thêm output
Notebook đã lưu hoặc Dataset qua **Add Input** rồi tìm lại. Nếu kết quả trước đó
chưa được lưu và đã mất khỏi session, không thể dựng lại số liệu từ source; cần
chạy thí nghiệm mới. Không tạo thư mục input rỗng để bỏ qua lỗi.

Nếu dùng `run_notebook`, thay `--input` bằng biến `reports` trả về từ helper.
Đổi thư mục input theo run thực tế, kể cả hậu tố rerun. Matplotlib thường có trong
image Kaggle; nếu import thiếu, báo cáo CSV vẫn tạo và `summary.json` ghi rõ charts
chưa sinh. Nếu cần, cài `requirements-analysis.txt` bằng đúng interpreter chạy phân tích.
Không tự tải package hay vẽ số giả để che thiếu dữ liệu.

Output:

- `arms.csv`: tất cả arm có thể nhận diện, cả failed/running/missing; NA giữ nguyên.
- `experiments.csv`: trạng thái cấp experiment; validation oracle có nhãn riêng.
- `paired_differences.csv`: verified − baseline/caller/extracted; kiểm tra cohort/seed/target/candidate pool và mutant pool.
- `mutants.csv`, `probes.csv`, `stages.csv`, `model_phases.csv`, `gpu_trace.csv`: provenance chi tiết.
- `analysis_manifest.json`: hash source phân tích và artifact đầu vào, cùng cờ file có đổi trong lúc hash.
- `summary.json`, `report.md`: tổng hợp có cảnh báo và số lượng target thật.
- `figures/*.svg`, `*.pdf`, `*.png`: quan sát quality/cost khi có dữ liệu hoàn tất.

Không gộp các revision/config/environment không tương thích. Các biểu đồ là quan sát
mô tả của pilot, không có CI/p-value suy rộng từ một target. Cùng function greedy
chạy nhiều lần không trở thành nhiều function độc lập. Các file validation oracle
không được trộn vào hiệu quả generated tests. Nếu chưa có dữ liệu hoàn tất,
bảng sẽ ghi NA và không vẽ biểu đồ hiệu quả.
