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

## Kaggle / Colab, kể cả notebook Python 3.13

Log pip đã xác nhận hai vấn đề ở môi trường cũ: Transformers 4.48.3 đòi
`tokenizers>=0.21`, nhưng Chroma 0.5.23 giới hạn `<=0.20.3`; NumPy 1.26.4 và
HNSWLib của stack cũ cũng không phù hợp để cài trực tiếp vào notebook Python 3.13.
Requirements mới dùng Transformers **4.46.3**, tokenizers **0.20.3**, giữ Chroma
0.5.23 và ghim các dependency telemetry/native liên quan.

Bật **Internet**, chọn **GPU**. Với source đã ở đường dẫn yêu cầu:

```python
%cd /kaggle/working/Test4Py-Setup-pilot-temp
!python -m pip install uv==0.6.17
!python bootstrap_kaggle.py --venv /tmp/test4py-venv --report-dir /kaggle/working/pilot-environment
```

Bootstrap tạo `/tmp/test4py-venv/` riêng theo lệnh trên với **Python 3.11.11**, **Torch 2.5.1 CUDA 12.1**,
bắt buộc dùng wheel cho NumPy/tokenizers/HNSW/ONNX (cho phép build package Python thuần),
chạy `pip check`, kiểm tra import và truy vấn Chroma
với embedding nhỏ. Không cần đổi kernel notebook hay sửa packages của Python 3.13.
Không cài torchvision/torchaudio vì pipeline chỉ xử lý text. Chạy lại bootstrap sẽ
kiểm tra/tái dùng environment hiện có, không xóa nó. Sai phiên bản Python trong
venv thì chọn đường dẫn mới qua `--venv`.

Sau khi bootstrap báo `Environment ready`, mọi lệnh pilot phải dùng **Python trong venv**:

```python
!/tmp/test4py-venv/bin/python run.py --validate-only --output /kaggle/working/validate-real
```

Chỉ tiếp tục khi validation báo `Status: complete`:

```python
!/tmp/test4py-venv/bin/python run.py --mode compare --rounds 1 --output /kaggle/working/pilot-qwen-1b
```

`--validate-only` lấy đúng hai commit, chạy hai trạng thái thật của PyCG, probe,
và kiểm tra bộ chấm bằng oracle nội bộ phải kill cả hai mutant. Oracle nội bộ
không được trộn vào generated pytest hoặc prompt. Lần đầu tải source/model/embedding
và initialization upstream có nhiều lời gọi model.

Chạy riêng hoặc dùng 3B:

```python
!/tmp/test4py-venv/bin/python run.py --mode verified --rounds 1 --output /kaggle/working/verified-1b
!/tmp/test4py-venv/bin/python run.py --mode compare --model Qwen/Qwen2.5-Coder-3B-Instruct --output /kaggle/working/pilot-qwen-3b
```

Trên Colab thay `/kaggle/working` bằng `/content`. Nếu dùng ZIP, giải nén trước
rồi `%cd` vào thư mục có `run.py` và `bootstrap_kaggle.py`.

### Chạy lại và tái lập

Nếu output đã tồn tại, CLI giữ nguyên toàn bộ log cũ và tự tạo thư mục **cùng cấp**
có hậu tố `-rerun-<UTC>-<index>`. Đọc đường dẫn thực tế ở dòng `Reports:`.
`experiment.json` cũng lưu `requested_output` và `actual_output`. Không xóa output
cũ để chạy lại. Nếu output trỏ vào một file thì CLI báo lỗi rõ ràng.

`environment.json` lưu Python, interpreter và toàn bộ phiên bản package thực tế;
`/kaggle/working/pilot-environment/requirements-resolved.txt` là pip freeze sau khi bootstrap thành công.
File requirements chính ghim dependency trực tiếp và các điểm xung đột, chưa phải
lock đầy đủ mọi dependency bắc cầu. Giữ pip freeze để tái lập chính xác environment.

Để tái lập model, lấy `model_revision` và `embedding_revision` từ `experiment.json`:

```python
!/tmp/test4py-venv/bin/python run.py --mode compare --rounds 1 --model Qwen/Qwen2.5-Coder-1.5B-Instruct --model-revision <MODEL_SHA> --embedding-revision <EMBEDDING_SHA> --output /kaggle/working/replay
```

Chạy mỗi arm trong process và checkout riêng để tránh cache import notebook.
Mỗi arm lỗi vẫn lưu log và tiếp tục arm kế tiếp; lỗi chung như không tải được
upstream/model được lưu ở cấp experiment. Exit code khác 0 nếu có lỗi.

Nếu đã có Python 3.10–3.12 và Torch CUDA hoạt động trong môi trường riêng,
có thể dùng cách cài trực tiếp rồi chạy bằng interpreter đó:

```bash
python -m pip install --only-binary=numpy,tokenizers,chroma-hnswlib,onnxruntime -r requirements-notebook.txt
python check_environment.py
python run.py --mode compare --rounds 1
```

Nguồn đối chiếu dependency: [Transformers 4.46.3](https://github.com/huggingface/transformers/blob/v4.46.3/setup.py),
[NumPy 1.26.4](https://pypi.org/project/numpy/1.26.4/),
[uv managed Python](https://docs.astral.sh/uv/guides/install-python/),
[Torch CUDA wheels](https://pytorch.org/get-started/previous-versions/).

### Notebook chạy từ đầu đến cuối

Mở/upload [kaggle_pilot.ipynb](kaggle_pilot.ipynb). Notebook clone source nếu chưa có,
bootstrap vào `/tmp`, kiểm tra GPU, validate rồi chạy compare bằng `subprocess.run(check=True)`.
Mỗi bước lỗi sẽ báo ngay trong cell. Source và báo cáo nằm dưới `/kaggle/working`;
venv và cache model nằm dưới `/tmp` để không đưa thư viện nặng vào output snapshot.
Lưu Notebook Version bằng **Save & Run All**; session này chạy lại từ đầu, nên giữ
các cell bootstrap trong notebook. Ghi lại Docker image version của Notebook cùng
`environment.json` và revision model. Không giả định session tương tác sẽ được tái dùng.

Đối chiếu với [Kaggle Notebook docs](https://www.kaggle.com/docs/notebooks) về Settings,
Internet/GPU, image version, session riêng khi Save & Run All và output `/kaggle/working`.
[Dockerfile chính thức](https://github.com/Kaggle/docker-python/blob/main/Dockerfile.tmpl)
hiện có đường dẫn Python 3.13; vì thế không giả định Python notebook luôn là 3.10–3.12.

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
