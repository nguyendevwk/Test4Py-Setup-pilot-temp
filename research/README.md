# Bộ đánh giá nghiên cứu

- `REVIEW.md`: đánh giá đóng góp, đối chiếu paper, audit thiết kế, RQ, thống kê và ứng dụng.
- `METRICS.csv`: định nghĩa chỉ số, mẫu số, nguồn dữ liệu và chỉ số còn thiếu instrumentation.
- `protocol.json`: proposal minh bạch; chưa phải thí nghiệm đã thực hiện.

Kết quả Kaggle chưa hoàn tất: không có số nào ở đây chứng minh verified vượt baseline.
Các fixture trong `tests/test_research.py` chỉ kiểm tra logic thống kê/collector, không phải dữ liệu thực nghiệm.

Sau khi một lượt chạy hoàn tất, phân tích ngay trên Kaggle để không cần tải log lớn vào cell:

```python
import subprocess
subprocess.run([
    '/tmp/test4py-modern/bin/python', 'analyze.py',
    '--input', '/kaggle/working/pilot-two-gpu',
    '--output', '/kaggle/working/pilot-research-report', '--plots',
], cwd='/kaggle/working/Test4Py-Setup-pilot-temp', check=True)
```

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
