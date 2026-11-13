# Test4Py: pilot tìm và kiểm chứng setup

Mở rộng tách khỏi upstream, dừng ở `pycg.machinery.imports.get_custom_loader`.
Test4Py ghim `3c8b45410545183a9a579a784ffefae722a158a6`, PyCG ghim
`8d5dc40837803beef1d8d379fbf2cdad6cd94641`. Không có ZIP bổ sung trong workspace ban đầu;
đã tái sử dụng launcher và ý tưởng adapter từ các file đã giải nén hiện có.

| Mode | Ngữ cảnh bổ sung sau suy luận kiểu upstream |
|---|---|
| baseline | Không thêm setup |
| caller | Function chứa lời gọi chuẩn bị object trong mã sản phẩm |
| extracted | Setup đầu tiên của từng tình huống trong danh sách AST |
| verified | Setup đầu tiên qua probe từ cùng danh sách và thứ tự |

Tất cả dùng cùng SLM, revision, mô tả tình huống, sinh pytest, repair, coverage và bộ chấm.
Mặc định Qwen 1.5B; embedding BGE giữ backend upstream. Xem
[đối chiếu paper/source và các giới hạn](docs/PIPELINE_REVIEW.md).

## Kaggle hoặc Colab

Bật **Internet và GPU**, dùng Python 3.10–3.12 và PyTorch CUDA của notebook.
Giải nén source vào thư mục ghi được. Nếu đã upload `Test4Py_Setup.zip`:

```python
import zipfile
with zipfile.ZipFile('/kaggle/working/Test4Py_Setup.zip') as z:
    z.extractall('/kaggle/working')
%cd /kaggle/working/Test4Py_Setup
!python -m pip install -r requirements-notebook.txt
!python run.py --mode compare --rounds 1
```

Colab dùng `/content` thay `/kaggle/working`; Kaggle Dataset ZIP thường nằm dưới
`/kaggle/input/...`, cần thay đường dẫn ZIP tương ứng. Không ép cài lại Torch của notebook.
Lần đầu tải cả source, model sinh và embedding; khởi tạo upstream gọi model nhiều lần.

Nên kiểm tra trước bằng lệnh không cần model/GPU (vẫn cần Internet và dependencies pytest):

```bash
python run.py --validate-only --output runs/validate-real
python run.py --mode compare --rounds 1 --output runs/compare-1b
python run.py --mode verified --rounds 1 --output runs/verified-1b
python run.py --mode compare --model Qwen/Qwen2.5-Coder-3B-Instruct --output runs/compare-3b
```

`--validate-only` lấy đúng hai commit, chạy hai trạng thái thật của PyCG, probe,
và kiểm tra bộ chấm bằng oracle nội bộ phải kill cả hai mutant. Oracle nội bộ
không được trộn vào generated pytest hoặc prompt.

Để tái lập, lấy `model_revision` và `embedding_revision` từ `experiment.json`:

```bash
python run.py --mode compare --rounds 1 --model Qwen/Qwen2.5-Coder-1.5B-Instruct \
  --model-revision <MODEL_SHA> --embedding-revision <EMBEDDING_SHA> \
  --output runs/replay
```

Output phải là thư mục mới. Chạy mỗi arm trong process và checkout riêng để tránh cache
import notebook. Mỗi arm lỗi vẫn lưu log và tiếp tục arm kế tiếp; lỗi chung như không tải
được upstream/model được lưu ở cấp experiment và dừng vì mọi arm đều phụ thuộc vào đó.
Exit code khác 0 nếu có lỗi; không suy diễn một lượt lỗi thành điểm chất lượng 0.

## Artifacts

- `experiment.json`: commit, revision thực tế, config và hash source extension.
- `comparison.json`: trạng thái, chi phí dùng chung, thời gian/metrics từng arm,
  candidate/mutant hash và trường hợp extracted chọn cùng setup với verified.
- `<mode>/PyCG/Test4DT_tests/test_*.py`: pytest do pipeline Test4Py sinh và giữ lại.
- `<mode>/attempts/*.py`, `test_attempts.jsonl`: cả các bản trước repair hoặc bị xóa.
- `<mode>/report.json`, `process.json`, `failure.txt` nếu lỗi.
- `<mode>/model_calls.jsonl`: prompt, output thô, token, giai đoạn và thời gian từng call.
- `<mode>/candidates.json`, `selection.json`, `probes.jsonl`: bằng chứng AST và lý do loại.
  Baseline không extraction; probe log rỗng ở mode không chạy probe.
- `<mode>/errors.jsonl`: lỗi generation/import/setup/assertion theo heuristic.
- `<mode>/score.json`, `original/`, `eligible_original/`: test pass bản gốc,
  branch coverage module/function và process/pytest JSON.
- `<mode>/mutant_pool.json`, `mutant_*/`, `mutants/`: cùng hai mutant, từng verdict,
  log chạy và source đã biến đổi. Chỉ test pass bản gốc mới được chấm mutant.
- `validation/validation.json`: kiểm tra PyCG thật khi chạy `--validate-only`.

Thời gian model được chia theo phase và operation, token bao gồm cả initialization/repair.
Thời gian toàn experiment gồm checkout/tải chung; thời gian từng arm gồm checkout,
model load, AST/probe, pipeline và chấm. Đây không phải thí nghiệm cùng tổng token.

## Kiểm tra tại workspace này

```bash
python -m unittest discover -s tests -v
python run.py --help
```

Các test offline dùng fixture nhỏ được ghi rõ là fixture, kiểm tra logic adapter,
Git pin cục bộ, timeout, candidate order và scoring verdict. Không phải kết quả trên PyCG thật.
Xem [báo cáo kiểm tra thực tế](docs/VALIDATION.md) cho trạng thái Internet/GPU và lệnh chạy tiếp.
