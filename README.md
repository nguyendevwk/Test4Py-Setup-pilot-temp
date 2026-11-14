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

## Chưa có dữ liệu kết quả? Chạy trọn gói để tự tạo dữ liệu thật

Source PyCG ở commit ghim là dữ liệu đầu vào của pilot. Không cần chuẩn bị một CSV
kết quả trước. [research/pilot-data.json](research/pilot-data.json) mô tả repository,
target và hai tình huống; đó là input specification, không phải số đo đã có.

Trên Kaggle bật Internet/GPU, dùng cell sau để tự bootstrap, tải source/model,
validate, chạy bốn arm trên tối đa hai GPU, tạo report/figures rồi đóng gói ZIP:

```python
import os
import subprocess
project = '/kaggle/working/Test4Py-Setup-pilot-temp'
subprocess.run(['git', '-C', project, 'pull', '--ff-only'], check=True)
os.chdir(project)
from pilot.notebook import run_research
result = run_research(jobs=2, gpus='auto', rounds=1, refresh=10)
print(result)
```

Không gọi `analyze.py` trước khi có artifact nếu muốn tạo dữ liệu mới. `run_research`
chủ động chạy thí nghiệm thật, nên cần thời gian GPU; không dùng số mẫu giả thay
cho inference. Dashboard vẫn là một bảng cập nhật tại chỗ. Dictionary trả về chỉ
đường dẫn artifact, Markdown report, figures và `results.zip`. Giữ/download ZIP
hoặc lưu Notebook Version để mang kết quả sang session khác.

CLI tương đương (không cần venv hoặc output sẵn):

```bash
python run_research.py --jobs 2 --gpus auto --rounds 1 --output /kaggle/working/test4py-research
```

Các file tạo ra: `input-specification.json`, `research-run.json`, `experiment/`
chứa artifact thật, `report/` chứa CSV/biểu đồ và `results.zip`. Nếu experiment có arm lỗi nhưng đã có artifact, báo cáo vẫn giữ đủ các arm và
ghi `partial_failure`; không thay lỗi bằng điểm 0. Lỗi bootstrap/validation không
có artifact sinh test sẽ dừng trước analysis. Bundle giữ bằng chứng lỗi của các bước đã chạy.
ZIP loại model weights, thư viện CUDA và checkout có thể tải lại; giữ generated
pytest, log model/probe, coverage, mutant verdicts, revision và báo cáo.

## Đánh giá khoa học và xuất bảng/biểu đồ

Xem [research/REVIEW.md](research/REVIEW.md) cho đánh giá phê bình so với paper,
đóng góp còn cần chứng minh, đối chứng, threats, kế hoạch thống kê và ứng dụng.
[research/METRICS.csv](research/METRICS.csv) ghi định nghĩa, đơn vị, mẫu số và các chỉ
số chưa đo được. [research/README.md](research/README.md) hướng dẫn dùng `analyze.py`
để xuất CSV, paired differences và figures SVG/PDF/PNG từ kết quả thật trên Kaggle.
Không có kết quả hoàn tất thì NA, không tự tạo biểu đồ hiệu quả hoặc CI/p-value.

Dashboard nay có cả mẫu số: các bước launcher, arm / 4, các bước initialization
được theo dõi, rounds hoàn tất / cấu hình, LLM calls kết thúc / đã bắt đầu,
probes / budget và mutants đã chấm / tổng. Mẫu số probe là ngân sách tối đa, không
phải số việc bắt buộc; số bước init không đồng nghĩa phần trăm thời gian. Tổng
LLM calls của upstream chưa biết trước, nên không đưa ra phần trăm tổng giả.

Bên dưới bảng có SVG charts GPU utilization, GPU memory và token cộng dồn. Chỉ giữ
60 mẫu gần nhất trong dashboard, không thêm output mới mỗi lần refresh; raw telemetry
vẫn lưu đầy đủ. Đây là biểu đồ vận hành; biểu đồ đánh giá khoa học tạo riêng bằng
Matplotlib sau khi có artifact đo được.

## Bảng trạng thái gọn trên Kaggle — khuyến nghị

Để tránh output dài làm chậm browser, dùng **hàm Python trong notebook** thay cho
`!python ...` nếu muốn bảng cập nhật tại chỗ:

```python
import os
import subprocess
project = '/kaggle/working/Test4Py-Setup-pilot-temp'
subprocess.run(['git', '-C', project, 'pull', '--ff-only'], check=True)
os.chdir(project)
from pilot.notebook import run_notebook
reports = run_notebook(
    output='/kaggle/working/pilot-dashboard',
    jobs=2, gpus='0,1', rounds=1, refresh=10,
)
```

Chỉ một bảng hiển thị được thay nội dung mỗi 10 giây qua
[IPython DisplayHandle.update](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html).
Bảng có stage, tiến độ 0/4 arm, GPU utilization/VRAM, call counter, token, token/giây,
pass và mutation score khi chấm xong. Không thêm một bảng mới cho mỗi event.
Không hiển thị output thô của model, danh sách hàng nghìn package hay toàn bộ traceback.

`reports` là thư mục thực tế: `<output>/run/` hoặc sibling mới nếu output đã tồn tại.
`launcher.log` nằm ngay dưới `<output>/`; log từng bước và báo cáo nằm trong `run/`.
Bảng chỉ đọc `progress.json`, `gpu_latest.json`, report JSON nhỏ; không quét
`model_calls.jsonl` hay đọc lại toàn log mỗi lần refresh. Phần tail fallback cũng
chỉ đọc tối đa vài KB. Metadata đầy đủ ở `run/environment/environment.json`.

Muốn xem một run có sẵn mà không khởi chạy thí nghiệm khác:

```python
from pilot.notebook import watch_run
watch_run('/kaggle/working/pilot-two-gpu', refresh=10)
```

Watch phải chạy trong kernel có quyền đọc thư mục đó; kernel notebook đang bận
chạy một cell đồng bộ thì cell watch khác phải chờ. Bản dashboard launcher ở trên
kết hợp việc khởi chạy và theo dõi trong cùng cell. Nếu ngắt cell, helper cố dừng
cả cây process (Kaggle có psutil), giữ nguyên log.

CLI mặc định dùng `--console compact`: dòng tổng hợp được giới hạn và model/GPU
log được throttle, toàn bộ raw output vẫn ghi trước khi lọc. `--console quiet`
giảm output hơn; `--console full` dành cho debug. `check_environment.py` chỉ in
vài phiên bản quan trọng; danh sách package đầy đủ chuyển sang JSON. Các chế độ
console không đổi prompt, model, token cap, pipeline hoặc bộ chấm.

## Tiến độ trực tiếp và hai GPU

Bản mới hiển thị output subprocess ngay trong cell, đồng thời giữ log đầy đủ.
Mỗi arm có `events.jsonl` và `progress.json`: model load, initialization, từng
model call bắt đầu/kết thúc, vòng sinh test, scoring và trạng thái cuối. Log model
call có input/output token, token/giây, VRAM allocated/reserved và peak allocated.
Không in output thô của model vào tiến độ; vẫn lưu nó trong `model_calls.jsonl`.

Khi không có dòng mới, heartbeat báo thời gian chờ sau khoảng 15 giây. Không đoán
phần trăm initialization vì số lời gọi phụ thuộc pipeline upstream. Số arm hoàn tất
`completed=... total=4` là số đo thực tế. Sau cùng in bảng pass, module branch coverage,
mutation score, token và thời gian; báo cáo JSON vẫn chứa coverage chi tiết từng hàm.

Hai GPU của Kaggle có thể chạy **hai arm độc lập song song**, mỗi GPU giữ một bản
SLM và embedding. Dùng `--jobs 2 --gpus 0,1` cho cả `kaggle_run.py` hoặc `run.py`:

```python
import subprocess
import sys
project = '/kaggle/working/Test4Py-Setup-pilot-temp'
subprocess.run(['git', '-C', project, 'pull', '--ff-only'], check=True)
subprocess.run([sys.executable, 'kaggle_run.py', '--runtime', 'modern',
                '--jobs', '2', '--gpus', '0,1', '--rounds', '1',
                '--output', '/kaggle/working/pilot-two-gpu'], cwd=project, check=True)
```

Nếu venv modern đã sẵn sàng và validation đã pass, chạy riêng phần so sánh:

```python
!/tmp/test4py-modern/bin/python run.py --runtime modern --mode compare --jobs 2 --gpus 0,1 --rounds 1 --output /kaggle/working/compare-two-gpu
```

Lịch chạy cấp slot rảnh cho arm tiếp theo, không quá một arm trên cùng GPU. Mỗi
arm có checkout/process/cache import riêng; chỉ dùng chung file model cache đã tải
trước. GPU index là tương đối với các GPU notebook đang thấy, có xét biến
`CUDA_VISIBLE_DEVICES` kế thừa. GPU trong mỗi worker được ánh xạ lại thành `cuda:0`,
đúng với API upstream. Tham khảo [PyTorch CUDA visibility](https://docs.pytorch.org/docs/2.11/cuda_environment_variables.html).

`--jobs 1` (mặc định) chạy tuần tự. `--jobs 2 --gpus auto` tự dùng tối đa hai GPU
thấy được; nếu chỉ thấy một thì chạy một arm mỗi lượt. `--gpus 0,1` báo lỗi nếu
không có đủ hai GPU. Không chia một model qua hai GPU và không cộng VRAM hai card.
Mức 11.2/15 GiB trên GPU đầu là một dấu hiệu có thể thử một arm tương tự trên GPU
thứ hai, chưa bảo đảm mọi prompt lớn đều vừa bộ nhớ.

`gpu_usage.jsonl` ở thư mục comparison lấy utilization/VRAM vật lý từ nvidia-smi
khoảng 15 giây/lần; thiếu nvidia-smi không làm thất bại thí nghiệm. Có tổng wall time
và tổng thời gian từng arm riêng. Chạy song song có tranh chấp CPU/IO, nên không
coi đó là số liệu tốc độ tuần tự hoặc bảo đảm nhanh gấp đôi. Model/revision, prompt,
repair, rounds, seed và token cap giữ chung cho bốn arm. Mỗi arm mặc định một CPU
thread để giảm tranh chấp; `run.py --cpu-threads` được ghi trong manifest.

## Chạy chuẩn trên Kaggle

Trong **Settings**, bật Internet và GPU. [Tài liệu Notebook Kaggle](https://www.kaggle.com/docs/notebooks)
cho phép gọi shell bằng `!`, nhưng các lệnh `!` riêng biệt không tự dừng chuỗi cell
khi một lệnh trả exit code khác 0. Dùng entrypoint tuần tự sau để không chạy
validation trên một môi trường cài đặt lỗi:

```python
import subprocess
import sys
from pathlib import Path
project = Path('/kaggle/working/Test4Py-Setup-pilot-temp')
subprocess.run(['git', '-C', str(project), 'pull', '--ff-only'], check=True)
subprocess.run([sys.executable, str(project / 'kaggle_run.py'), '--runtime', 'modern',
                '--output', '/kaggle/working/test4py-pilot'], check=True, cwd=project)
```

Entry point chạy bootstrap, validation, rồi compare; chỉ chạy bước sau khi bước
trước thành công. Không xóa venv dở hoặc log cũ. Nếu output tồn tại, tạo sibling mới.
Xem đường dẫn in ra: `notebook-run.json`, `bootstrap.log`, `validation.log`,
`comparison.log`; báo cáo nghiên cứu nằm trong `comparison/comparison.json`.
Log được ghi trong khi subprocess chạy, nên có thể mở file từ giao diện Kaggle.
Venv/cache vẫn nằm dưới `/tmp`, output nằm trong `/kaggle/working` để lưu Notebook Version.

Lỗi `invalid value ... --only-binary` đã được sửa ở cả hai bootstrap: `uv` nhận
một cờ cho từng package, ví dụ `--only-binary numpy --only-binary tokenizers`.
Đây là [cú pháp uv](https://docs.astral.sh/uv/reference/cli/), không phải cấu hình Kaggle.
Thêm regression test gọi uv thật với wheel fixture, offline và dry-run, để kiểm tra
parser mà không tải dependencies hoặc thay đổi môi trường.

## Tùy chọn thư viện mới trên Python 3.13

Profile **modern** bổ sung Transformers 4.57.6, Chroma 1.3.5, NumPy 2.2.6 và
LangChain Core 1.0.7. Đây là các phiên bản mới hơn được chọn để kiểm tra API;
không tuyên bố là tất cả phiên bản mới nhất hoặc đã pass pipeline trên Kaggle.
Bản legacy bên dưới vẫn giữ để đối chiếu. Không trộn hai file requirements.

Modern tái dùng Python và Torch CUDA có sẵn của Kaggle, không tải lại Torch/CUDA.
Một venv `--system-site-packages` nhận các thư viện modern cục bộ và đọc các package
còn lại từ image Kaggle. Vì vậy phải giữ cả Docker image version, `environment.json`
và freeze khi tái lập; đây không phải môi trường hoàn toàn độc lập image.

```python
%cd /kaggle/working/Test4Py-Setup-pilot-temp
!python -m pip install uv==0.6.17
!python bootstrap_modern.py --report-dir /kaggle/working/modern-environment
!/tmp/test4py-modern/bin/python run.py --runtime modern --validate-only --output /kaggle/working/validate-modern
```

Sau khi validation báo complete:

```python
!/tmp/test4py-modern/bin/python run.py --runtime modern --mode compare --rounds 1 --output /kaggle/working/pilot-modern
```

Bootstrap bắt buộc smoke-check import và Chroma add/query. `pip-check.txt` ghi cả
xung đột từ package kế thừa của image, nên cần xem log nếu có cảnh báo. Chưa có
Internet/GPU tại workspace để chạy kiểm tra tích hợp. Chỉ diễn giải kết quả sau khi
validation thật pass; kiểm tra này chưa thay cho một lượt sinh test thật.

Cả bốn arm phải chạy trong cùng profile. Không dùng baseline legacy so với verified
modern để quy tác động cho setup. Phần phân tích, suy luận kiểu, generation/repair
của upstream vẫn giữ nguyên. API của Chroma mới và Python 3.13 phải được xác minh
thêm qua validation và vòng sinh test thật.

Nguồn phiên bản: [Transformers](https://pypi.org/project/transformers/4.57.6/),
[Chroma](https://pypi.org/project/chromadb/1.3.5/),
[NumPy](https://pypi.org/project/numpy/2.2.6/).

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

### Audit an existing completed run without generating again

```python
import subprocess, sys
subprocess.run(["git", "pull"], cwd="/kaggle/working/Test4Py-Setup-pilot-temp", check=True)
subprocess.run([sys.executable, "analyze.py", "--input", "/kaggle/working/pilot-dashboard/run",
               "--output", "/kaggle/working/pilot-evaluation", "--plots"],
              cwd="/kaggle/working/Test4Py-Setup-pilot-temp", check=True)
```

`arms.csv` includes execution status separately from test outcome, measured token cost,
passing tests per million tokens, cost per passing test (undefined when zero pass),
truncation and probe counts. `model_operations.csv` separates initialization and
individual generation/repair operations; `model_phases.csv` and `stages.csv` provide
phase costs. `diagnostics.json` retains three clipped recent error messages per arm;
full raw logs remain in the original run. Error categories are heuristic event counts,
not independently labeled test failure rates. Probe acceptance is conditioned on the
ordered early-stopping search, not an unbiased candidate success probability.

Completion means execution ended; it does not establish usefulness. With zero passing
tests, mutation score stays NA and no positive generation benefit can be claimed.
Coverage not measured stays NA. One target and one round support descriptive paired
comparisons only; do not compute significance from four treatment arms as replicates.
Dual-GPU speedup requires a matched single-GPU execution; token/s alone cannot establish it.
Use actual artifacts to diagnose zero-pass runs before repeating model generation.

### Quality-first 2026 cohort: run smoke before the pilot

Default generator is now `Nanbeige/Nanbeige4.1-3B`, with the February2026
research report https://arxiv.org/abs/2602.13367 and official model card
https://huggingface.co/Nanbeige/Nanbeige4.1-3B . This is a source-backed candidate,
not a measured best-model claim. Its profile uses an8192 output-token cap,
slow tokenizer, explicit chat EOS166101, and separates completed reasoning
from the final answer. Raw reasoning/output and token costs are retained.
An incomplete reasoning answer fails explicitly. This budget is experimental,
not the vendor's full recommended budget or a guarantee of quality.

```python
import subprocess, sys
project = "/kaggle/working/Test4Py-Setup-pilot-temp"
subprocess.run(["git", "pull"], cwd=project, check=True)
subprocess.run([sys.executable, "bootstrap_modern.py"], cwd=project, check=True)
subprocess.run([
    "/tmp/test4py-modern/bin/python", "run.py",
    "--runtime", "modern", "--model-smoke",
    "--model", "Nanbeige/Nanbeige4.1-3B",
    "--output", "/kaggle/working/test4py-model-smoke",
], cwd=project, check=True)
```

Smoke loads the pinned model revision and generates one tiny Python answer,
parses it and writes `smoke.py`, `smoke.json`, `model_calls.jsonl`, `experiment.json`.
It does not execute generated code, run Test4Py initialization, or establish
pilot effectiveness. On failure preserve `comparison.json` and raw logs.
Do not start the full comparison until the smoke result is reviewed.
For a non-thinking control use `--model Qwen/Qwen3-4B-Instruct-2507`.
Qwen3.5 is explicitly rejected pending a validated architecture/runtime adapter.

The new shared `source-grounded-v2` prompt policy appends actual production
imports, factory and receiver-method excerpts to generation/repair in every arm;
these override conflicting generated usage summaries without exposing probe
observations or oracle outputs. Single complete Python-block extraction is
uniform across arms; ambiguous/incomplete fenced answers fail explicitly.
Candidate AST quality and every static/runtime checker result are archived.
These are new experimental conditions and must not be pooled with old runs;
`analyze.py` includes prompt policy, extraction, token cap and model profile in
comparability cohorts. `--prompt-policy original` omits source grounding but
retains the new extraction policy, so it is not an exact historical replay.
See `research/QUALITY_FIRST.md` for the scientific protocol.
