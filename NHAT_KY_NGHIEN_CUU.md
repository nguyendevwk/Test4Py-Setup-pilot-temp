# Nhật ký nghiên cứu và quyết định

Ngày cập nhật: **2026-11-16**. Đây là nhật ký bằng chứng, bao gồm kết quả âm.
Nguồn vận hành hiện hành: [sổ tay](SO_TAY_HIEN_HANH.md) và
[protocol v4](../docs/MULTITARGET_V4.md).

Mỗi mục mới phải ghi: run/protocol, giả thuyết, cấu hình đã khóa, artifact/hash,
quan sát, diễn giải có giới hạn, quyết định và những gì chưa xác nhận. Không sửa
âm thầm số liệu cũ; thêm đính chính có lý do. Local fixture, preflight, GPU screen
và efficacy study phải được gắn nhãn khác nhau.

## 2026-11-16 — R0: Bảo toàn và đính chính sổ tay cũ

Đã giữ nguyên [bản trước cập nhật](history/SO_TAY_TRUOC_CAP_NHAT_2026-11-16.md).
SHA-256: `f94e55db19eacb058e2c3872ac8f6f1d72e9aef1b220a4a84d5d2ccea4f99614`.

Các kết luận cũ không tiếp tục sử dụng làm bằng chứng hiện hành:

- “Setup là điều kiện tiên quyết”, “SLM hoàn toàn không thể”: chỉ có quan sát trên
  một case phát triển; chưa có thiết kế để kết luận tính cần thiết/tổng quát.
- “Verified loại bỏ hoàn toàn runtime crash”: probe chỉ bao phủ lần chạy/phạm vi đã
  quan sát. Chưa kiểm chứng mọi input, môi trường hoặc method.
- “Pruning đảm bảo suite pass 100%”: pass của tập đã chọn không phải pass của suite
  ban đầu; loại test fail làm đổi mẫu số và cần báo riêng.
- “Môi trường sẵn sàng thực thi 100%”: source tests không bảo đảm output model đúng,
  không OOM hoặc chạy mọi project thành công.
- Bảng N=15 nhưng ghi 7/8 và các điểm PyCG cũ: chưa có raw artifact được đối chiếu
  trong lần cập nhật này; chưa xác minh mẫu số, không dùng để so với v3/v4.
- Quy nguyên nhân timing chậm cho traceback hoặc OOM cho cache chưa đủ trace nhân
  quả. Không giữ các lời giải thích đó như phát hiện đã được chứng minh.

**Bài học:** không xóa lịch sử sai, nhưng tách lịch sử khỏi hướng dẫn hiện hành;
phát biểu phải có đúng phạm vi, mẫu số và nguồn bằng chứng.

## 2026-11-16 — R1: Audit ZIP đa target đời đầu

Artifact local: `/home/heurix/Downloads/EVALUATION_OUTPUT.zip` (99.712 bytes).
SHA-256: `c28c2cb4288b71afb7d0ecfcc10a944aa576ffa18fa24d4b19cf80cd29c935ac`.
Đây là batch phát triển 2 target × 3 arm × 1 lượt; không có đầy đủ source/model
revision để replay chính xác. Không gắn nhãn protocol v2 chỉ vì summary có schema=2.

**Quan sát từ artifact:**

- Sáu candidate đầu đều không collect được test do import/syntax.
- Parse baseline: Critic sửa qua collection; 2 pass/8 test. Sau pruning chỉ còn
  2/2. Đây là thu hồi hai test, không phải repair suite hoàn chỉnh.
- “Line 26,97%” sai nhãn: counts là 19/55 statements (34,55%) và 5/34 branches
  (14,71%); 26,97% = (19+5)/(55+34), chỉ số kết hợp.
- Năm hàng “0/1 nodes” là lỗi stdout fallback: pytest JSON ghi collected=0.
- Fragment repair có thông báo ImportError hoặc một dòng code. Không có raw output
  nên chưa chứng minh Critic đã sinh một block hoàn chỉnh thứ hai bị parser bỏ mất.

**Quyết định:** bỏ stdout fallback, tính coverage từ counts, lưu raw output,
compile/extract chặt chẽ, không pruning để tăng headline pass. Không gọi kết quả
này là “đột phá” hoặc “Critic hiệu quả 100%”.

## 2026-11-16 — R2: Screen v3 chạy trên Kaggle thật

Run id: `SCREEN_V3_20261116T074857429670Z`.
Protocol: `council-development-screen-v3`; planned=6, finished=6, mock=false.
Artifact local: `/home/heurix/Downloads/SCREEN_V3_20261116T074857429670Z.zip`
(4.479.125 bytes).
SHA-256: `fcff68101ff7bbe4e87bfc577d359499d24cfdec21d8133f9a2ba001362fd5e3`.

Môi trường theo engine/manifest: Python 3.13.16; torch 2.11.0+cu130;
transformers 4.57.6; 2 Tesla T4; NF4.
Coder: `Qwen/Qwen2.5-Coder-7B-Instruct@c03e6d358207e414f1eca0bb1891e29f1db0e242`.
Critic: `Qwen/Qwen3-4B-Instruct-2507@cdbee75f17c01a7cc42f958dc650907174af0554`.
Source hashes của năm file runner/helper/Council trong manifest đã được đối chiếu
với source local tại thời điểm phân tích, trước khi sửa v4.

| Target | Arm | Ban đầu pass/total | Cuối pass/total | Thời gian sample (s) |
|---|---|---|---|---:|
| parse | baseline | 2/7 | 2/7 | 103,946 |
| parse | ranked | 0/3 | 1/3 | 64,698 |
| parse | verified | 0/3 | 1/3 | 64,835 |
| Timer | baseline | 2/4 | 2/4 | 70,870 |
| Timer | ranked | 0/3 | 0/3 | 214,978 |
| Timer | verified | 0/3 | 0/3 | 31,051 |

Không cộng các node thành target độc lập. Các hàng là các lượt phát triển có lặp
code; không dùng bảng này để suy luận thống kê hoặc chứng minh generalization.

**Quan sát:**

- Cả hai model nạp xong trên cuda:0/cuda:1; không có OOM được ghi nhận trong run.
  Cảnh báo CUDA đầu log không chặn lượt này; không suy ra mọi cảnh báo đều vô hại.
- Cả 6 candidate đầu compile/collect được. Không suite nào all-pass. Các lỗi
  import/collection đời đầu không tái hiện ở batch này, nhưng không được quy cải
  thiện đó chỉ cho một thành phần vì điều kiện đã thay đổi.
- Parse dùng sai `Docstring.args`, coi function parse là namespace, trộn input
  ReST với parser GOOGLE, kỳ vọng sai exception. Repair chưa sửa hết hiểu sai API.
- Timer thiếu import math, đọc last trước stop, coi elapsed float là chuỗi log,
  hiểu sai logger=None và patch logger ở class. Source cho thấy last chỉ cập nhật
  khi stop; logger nhận chuỗi riêng. Đây là chẩn đoán development, không phải
  expected values được phép hardcode vào generator để cứu target.
- Timer/ranked Critic: đúng 2048 output tokens, truncated=true, code fence chưa
  đóng; raw output có comment dài và dừng giữa chừng. Đây là truncation xác nhận
  được, khác giả thuyết extraction ở R1.
- Parse baseline repair bị từ chối vì mất một test. Các repair khác có assertion
  thay đổi được gắn review. Không pruning nên fail vẫn hiển thị.
- Ranked và verified có raw Coder giống nhau trên từng target. Probe v3 không
  đưa target invocation witness vào context; không có bằng chứng lợi ích riêng
  của verification trong batch này.
- Coverage v3 là NA vì policy chỉ đo suite all-pass, **không phải coverage đo được 0**.
  Stable=false khi chưa replay cũng không phải bằng chứng flaky.

**Chi phí từ telemetry:** Coder 6 calls, 9.138 input/2.256 output tokens,
162,634 s; Critic 6 calls, 15.161 input/3.640 output tokens, 374,879 s.
Critic chiếm khoảng 69,7% tổng thời gian inference hai role; không sửa suite nào
thành all-pass. Đây chưa bao gồm toàn chi phí tải/nạp model và chuẩn bị.

**Kết luận được phép:** hạ tầng đã hoàn tất hàng đợi; chất lượng test/oracle chưa
đạt. Kết quả chưa chứng minh cải tiến so với upstream hoặc paper. Gate exit=2 và
AssertionError cuối notebook là chặn chất lượng, không phải nguyên nhân test fail.

## 2026-11-16 — R3: Quyết định thiết kế v4, chưa có số liệu GPU

**Giả thuyết:** source của kiểu trả về/dependency và nhiệm vụ nhỏ giúp SLM giảm
đoán API/trạng thái. Invocation witness có thể hỗ trợ khả năng gọi target; chưa
chứng minh assertion đúng hay đóng góp riêng của verification.

**Các thay đổi có thể áp dụng qua nhiều project:**

1. Bounded AST dependency retrieval, ưu tiên return annotation; hỗ trợ relative
   import, src-layout và qualified methods. Không nhánh theo tên project/target.
2. Prompt một test/một hành vi; token budgets rõ; overflow/truncation thành lỗi
   được lưu, không cắt ngầm hoặc chọn block dài nhất để cứu điểm.
3. Witness qua signature và setup values: function entry + normal completion;
   class constructor only. Không quan sát/đưa return values vào expected assertion.
4. Bốn arm baseline/grounded/ranked/verified để tách context, hint và witness.
5. Một repair; giữ assertion expressions. Đề xuất thay assertion lưu review,
   không tự credit pass. Cú pháp không chứng minh bảo toàn ngữ nghĩa.
6. Full-suite metrics giữ nguyên. passing_subset là chỉ số phụ có eligible/planned,
   replay hai lần và NA khi không ổn định; không sửa file suite hoặc đổi suite fail.
7. Tách harness_ready khỏi generation_quality_ready; giữ strict gate và exit=2.
   Phân biệt replay not_run/unstable; model-call ids có target/arm/sample.
8. External benchmark JSON yêu cầu production paths và commit SHA bất biến;
   không lọc target theo kết quả. Các hint vẫn là input thủ công phải công khai.

**Kế hoạch screen khóa trước:** 2 target × 4 arm × 1 seed (42), temperature=0,7,
output cap 2048, input cap 8192. Coder/Critic giữ SHAs ở R2. Cùng policy giữa các arm.
Không đổi self-repair/Critic, seed hoặc target sau khi xem điểm. Không tự chạy full.
Hai target này là development set; phải có project held-out để kiểm chứng tiếp.

**Bằng chứng hiện có:** 102 tests local pass trên Python 3.12.13, gồm 37 tests
đa target; fixture/scripted output được ghi rõ không phải dữ liệu model. Preflight
source thật pass. Clone + snapshot integration ở bước trước pass 36 tests khi đó;
snapshot cuối đã kiểm tra byte/hash và compile các cell. Chi tiết và hạn chế ở
[validation v4](../docs/MULTITARGET_V4_VALIDATION.md).

**Chưa xác nhận:** accuracy/coverage/mutation v4, runtime và VRAM trên Kaggle,
khả năng tổng quát trên benchmark khác, lợi ích so với Test4Py upstream. Không viết
“đã cải thiện” khi mới có thay đổi source và local tests.

## 2026-11-16 — R4: Audit Kaggle v4 và lỗi giả định sai truyền qua repair

Run id: `SCREEN_V4_20261116T083124958628Z`, protocol v4; planned=8,
finished=8, mock=false. Artifact local:
`/home/heurix/Downloads/SCREEN_V4_20261116T083124958628Z.zip` (6.032.152 bytes).
SHA-256: `a02046055233681a75758b995aa54afa816b9805f877fb991120c1fec14c091d`.
Đây là kết quả GPU thật được nhận sau mục R3; R3 mô tả trạng thái trước run này.
Không sửa ngược R3 để biến local tests thành bằng chứng GPU.

| Target | Arm | First/final suite pass | Module line/branch | Đánh giá chính |
|---|---|---|---|---|
| parse | baseline | false/false | NA/NA | Description kỳ vọng chuỗi rỗng; thực tế None; repair đổi assertion bị từ chối |
| parse | grounded | true/true | 34,55%/11,76% | Assertion nội dung params/default/return có ý nghĩa; replay stable |
| parse | ranked | false/false | NA/NA | Attribute Kind không export; Critic đổi thành import Kind cũng sai |
| parse | verified | false/false | NA/NA | Input ReST nhưng chọn GOOGLE; Critic thêm len(params)>=1, không sửa mâu thuẫn |
| Timer | baseline | false/false | NA/NA | Thiếu math; Critic thêm import nhưng đổi ==False thành is False, nên bị gate từ chối |
| Timer | grounded | false/false | NA/NA | Kỳ vọng TimerError cho Exception do chính test raise; Critic vẫn giữ giả định sai |
| Timer | ranked | false/true | 80,85%/37,50% | Thêm import math/time, giữ nguyên assertion vòng đời; replay stable |
| Timer | verified | false/true | 80,85%/37,50% | Code cuối giống ranked; witness constructor không chứng minh lợi ích riêng |

**Bằng chứng dương có giới hạn:** first-pass=1/8, final suite pass=3/8; Critic
sửa all-pass 2/7 lượt repair, hai lượt thuộc cùng target và có code cuối giống nhau.
Các test pass không có pruning hoặc thay assertion được tự credit. Đọc source/test
cho thấy các kiểm tra có ý nghĩa nhưng chưa review độc lập hoặc đo mutation/lỗi thật.
Parse grounded dùng params_by_name, type/default/optional và returns theo nội dung
input. Timer kiểm tra last trước/sau context cùng _start_time; chưa kiểm tra độ đúng
của thời gian hoặc nội dung logger. Không gọi 3/8 là assertion accuracy.

Coverage function cho parse là 4/11 statements và 3/10 branches; 34,55%/11,76%
trong bảng là MODULE. Timer 80,85% module gồm 21 dòng ở scope module; start chỉ
2/8 branches và stop 4/8. Không diễn giải 80,85% thành bao phủ hết vòng đời/API.

**Anti-hallucination — điều đã quan sát:**

1. Coder sai namespace Kind; Critic không xác minh provider mà chỉ chuyển cách
   viết, gây collection error. Đó là thay biểu hiện, không sửa căn cứ.
2. Coder gán input ReST cho GOOGLE; Critic thêm assertion về params nhưng giữ
   nguyên giả định không được source xác nhận. Thông tin có trong context chưa
   đồng nghĩa model đã kiểm tra nó.
3. Timer grounded nhầm exception của test với lỗi Timer; Critic thêm imports và
   comment nhưng không sửa nguyên nhân. Một function chứa nhiều scenario còn
   có các kỳ vọng thời gian gần zero chưa được chạy tới; không tính chúng là pass.
4. Freeze assertion ngăn sửa expected value tùy tiện nhưng không ngăn giả định sai
   về import/input/setup. Gate cũng chặn một proposal có sửa import hữu ích chỉ vì
   đổi hình thức bool assertion. Không nới gate để lấy điểm; ưu tiên tách repair
   cú pháp/import xác thực khỏi sửa oracle và giảm thay đổi ngoài phạm vi.

**Chi phí:** 8 Coder calls, 24.194 input/1.435 output tokens, 170,780 s;
7 Critic calls, 21.563 input/1.288 output tokens, 171,459 s. Không call nào chạm
output cap theo model log. Tổng inference khoảng 342,239 s; chưa bao gồm model load,
preflight và toàn bộ replay. Không so tốc độ trực tiếp với v3 vì task/context đổi.

**Đánh giá hướng mục tiêu:** có tín hiệu dùng được của source grounding trên parse
và setup context trên Timer trong development set. Chưa nhất quán: grounded Timer
fail và hint làm đổi parse từ pass sang fail ở lượt quan sát này. Không có bằng
chứng verified hơn ranked trên Timer. Một seed và hai project đã tuning không đủ
kết luận tổng quát hoặc vượt Test4Py upstream/paper. Cần ưu tiên đo chất lượng test,
không chỉ đạt green gate cho mọi baseline.

**Phương án anti-hallucination đề xuất, CHƯA triển khai ở mục này:**

- Fact registry từ source/runtime API: symbol/provider/signature, provenance và
  trạng thái verified/unknown/contradicted. Lời giải thích Coder/Critic không tự
  được nâng thành fact. Source tồn tại không tự chứng minh một behavioral claim.
- CPU validation import/call trước và sau repair; không chuyển sang bước sau với
  giả định bị bác bỏ. Ambiguous/dynamic cases phải ghi unknown, không đoán provider.
- Repair nhận diagnostics xác thực và source gốc; giả định của candidate được
  đánh dấu chưa tin cậy. Chỉ sửa lỗi có bằng chứng, không thêm assertion để che lỗi.
- Tách import-only patch có kiểm chứng khỏi oracle repair. Giữ raw first-pass,
  post-patch và chi phí riêng; không giả rằng patch là output gốc của model.
- Bind invocation witness với đúng callable/arguments/mode được test sử dụng,
  không lấy witness AUTO/constructor làm chứng cứ cho GOOGLE hoặc method khác.
- Yêu cầu một scenario có precondition/action/observation; một def test_ chứa nhiều
  hành vi không đáp ứng mục tiêu giảm gánh nặng cho SLM. Không tự xóa phần fail.
- Mọi thay đổi guard phải thành cohort mới, áp dụng theo protocol chung/ablation,
  không hardcode symbol/expected của hai case hoặc dùng mutant verdict để sửa test.

**Quyết định:** giữ nguyên archive v4. Không chỉnh source trong lượt audit này.
Ưu tiên một cơ chế kiểm chứng facts/repair gọn cho SLM và đánh giá fault detection
trên held-out targets; không thêm agent/call hoặc mở rộng instrumentation nếu không
phục vụ giảm lỗi, tăng test hữu ích hay đo công bằng với upstream.

## 2026-11-16 — R5: Quay về pipeline paper, triển khai paired pilot 14B NF4

**Mục tiêu đã chốt lại với người dùng:** tái chạy một phần nghiên cứu Test4Py và
so cùng model Qwen2.5-Coder-14B-Instruct NF4 ở baseline/cải tiến. Không tiếp tục dùng
Council baseline thay upstream; không dùng 14B Coder/4B Critic như một thay đổi ẩn.
Tất cả vai trò dùng cùng checkpoint. Phải kiểm tra VRAM với context + decode thật.

**Source đã sửa:** NF4 fail-closed, không fallback FP16/offload; kiểm tra input+
output budget trước GPU transfer; giải phóng tensor/frame references; CPU embedding
qua AST adapter; sửa lỗi collection report không có tests; phân tích toàn package,
chỉ giới hạn module generation; lỗi framework không được che thành candidate fail.
Cải tiến gồm lọc member/type có bằng chứng, class context từ source/signature,
kiểm chứng import/namespace trước repair, bổ sung import stdlib có audit, và veto
assertion-changing reductions. Prompt repair cải tiến không yêu cầu chép actual
output. Baseline giữ prompt/reduction gốc để so đúng phương pháp đã công bố.

**Kinh nghiệm mới:** upstream `repair_assert_error` có hướng dẫn thay assertion để
khớp actual output. Đây là chính sách regression của source gốc, không tự chứng minh
hành vi gian lận. Cần báo riêng thay đổi oracle/reduction và đo fault detection;
không dùng pass rate đơn độc để kết luận assertion chính xác. Bảo toàn AST assertion
ở bản cải tiến có thể từ chối sửa tương đương và phải nêu trade-off này.

**Chọn subset theo source/preflight, trước điểm model:** đề xuất ban đầu pyrthon/
superstring/woa chưa được khóa. Kiểm tra thực cho thấy pyrthon.console không có
function; superstring có 37 functions. Chốt pilot thực tế genty_repeat, genty_args
và whale_optimization (3 module, 2 project NA), đúng commit paper. Không gọi đây là
5 module/3 project hoặc mẫu đại diện 183 module. Small genty_repeat: 1 seed/1 round/
2 arm. Larger pilot: 3 module/2 seed/3 round/2 arm, tổng 12 module trials.

**Tối ưu thời gian có kiểm soát:** initialization greedy có cache prompt chính xác
chung cho A/B, gắn model/config/source fingerprint. Không cache generation, repair,
pytest hoặc mutants. Generation seeds reset sau init; các seed không phải lặp độc
lập toàn bộ summary pipeline. Tách logical/fresh tokens và cache hits; không gán
lợi ích warm-cache theo thứ tự chạy thành lợi ích phương pháp. Không chia toàn bộ
chi phí project cho mỗi module rồi cộng trùng.

**Kiểm tra đã chạy local:** unit/integration CPU và actual upstream fixture đã qua;
actual genty/woa source import và ProjectMessage.init qua với scripted summaries/
embedding. Fixture initialization ghi 95 và 59 calls tương ứng. Fake model/embedding
được gắn nhãn, không xuất thành số liệu Qwen. Chi tiết và số test cuối ở
[validation](../docs/UPSTREAM_NF4_VALIDATION.md).

**Chưa chạy được local:** nvidia-smi báo không kết nối driver. Không có bằng chứng
NF4 14B inference/VRAM hoặc hiệu quả A/B mới tại đây. Notebook
`kaggle_upstream_nf4_paired.ipynb` clone Git + snapshot SHA-256, chạy source checks,
prepare, fixture, forced-decode stress từng GPU rồi small A/B; dừng trước larger.
Gate larger cần stress đúng model/plan/GPU, small không lỗi framework/resource;
không đòi baseline phải all-pass. Giữ mọi trial fail, unknown và artifact.

**Bộ chấm:** pools toán học/comparison nhỏ, cố định trước inference, tối đa 4 mutant/
module; genty_args hiện không có operator phù hợp nên mutation NA. Không đổi pool
sau khi thấy score. Timeout/import/setup không phải kill. Đây không phải mutation
benchmark tổng quát; assertion accuracy vẫn cần review. Protocol chi tiết:
[UPSTREAM_NF4_PILOT.md](../docs/UPSTREAM_NF4_PILOT.md).

## R6 — Lỗi chuẩn bị Kaggle và kiểm toán phép đo (2026-11-16)

Log người dùng cung cấp: genty fail trước inference vì runner đưa
`requirements-paired.txt` vào pip như tên package; woa prepared. Đây là lỗi dựng
lệnh của harness, không phải bằng chứng benchmark/model thất bại. Sửa cả nhánh
editable và requirements-only, giữ constraints, không fallback sửa source.
Thêm kiểm thử pip thật offline và kiểm thử failure giữ trạng thái failed; bộ
126 CPU tests đã qua trước khi bổ sung measurement. Chưa có kết quả GPU 14B.

Kiểm toán phát hiện `passed` upstream là số node, không phải all-pass suite.
Coverage dùng passing subset replay; không được kể là coverage toàn bộ candidate
suite. Bổ sung retained-suite counts, mẫu số raw coverage, mutant killed/survived/
unresolved, planned/measured/missing và telemetry vào exports. Assertion accuracy
và hallucination rate để null đến khi review bằng cùng taxonomy/source evidence.
Không suy từ pass, hai replay hay coverage một module thành oracle đúng hoặc
vượt trung bình 183 module của paper. Pool mutant nhỏ có equivalent chưa lọc.

Người dùng gửi console Council 80 trials: không nhập thành raw dataset đã xác minh.
ZIP EXP_OVERNIGHT_V5 chưa có local tại thời điểm audit. Không gộp vào cohort upstream
14B. Sửa phần mềm dùng output/plan mới; giữ archive lỗi trước đó.

## R7 — Screen có ngân sách một giờ trước pilot lớn (2026-11-16)

Người dùng còn 3–8 giờ, yêu cầu kiểm tra tập nhỏ khoảng một giờ rồi mới chạy lớn.
Khóa small ở hai module genty, seed 42, một vòng, hai arm: 4 module-trials trong
hai worker. Main vẫn ba module/hai project, hai seed, ba vòng: 12 module-trials.
Đây là larger pilot đã cấu hình, không phải toàn bộ 183 module của paper.

Notebook hiện dùng chung 4096 input/512 output cho hai arm và cả hai giai đoạn;
nguồn default CLI 6144/1024 vẫn có nhưng không được gọi là cấu hình notebook.
512 token có rủi ro output bị cắt; lưu raw/candidate errors, không cứu bằng pruning.
Thêm shared deadline 3600 giây từ stress tới small, bao gồm download/load model
và embedding; CPU bootstrap/prepare/fixture tính riêng. Stress hai T4 chạy song
song và bị giới hạn 1800 giây/probe. Small dùng thời gian còn lại; hết giờ giữ
planned rows/NA, không suy thành 0 coverage hay tự đổi model/budget.

Main chỉ mở khi small hoàn tất phần framework/resource và thực sự đo được ít
nhất một đường coverage từ test model sinh. Không đòi baseline all-pass; không
lấy tiêu chí phát triển này làm bằng chứng efficacy/held-out. Notebook mặc định
RUN_LARGER=False, cần review rồi bật. Hai module small không chứng minh mọi nhánh
model thực của woa đã chạy; chỉ dependency/import và CPU init của woa đã được
kiểm tra trước small. Chưa có bằng chứng GPU 14B hoặc cam kết hoàn tất trong một giờ.

Validation cuối R7: **131 CPU tests đạt trong 73.267 giây**. Fresh Git + đúng
overlay notebook đạt 26 paired tests và cả hai upstream fixture arms (model/
embedding scripted). Timeout/scheduling được kiểm tra bằng fixture; không tính
thành đo tốc độ/model quality thực. Notebook compile và RUN_LARGER=False.

## R8 — Kaggle không chặn root; SDPA OOM ở 4K (2026-11-17)

Đọc notebook1aa30d2af4 và ZIP UPSTREAM_NF4_20261116T170358791891Z do người dùng
cung cấp. 131 tests, prepare hai project và CPU fixtures đều qua trên Kaggle.
Hai T4 load model ~9.29 GiB; bài 2048+512 qua, margin ~2.90 GiB. Bài 4096 input
OOM trong SDPA, cần 2.50 GiB nhưng chỉ còn 1.65 GiB. Không có evidence quyền root
bị Kaggle chặn. Ghi probe/hash nguồn tại artifacts/upstream_nf4_20261116_gpu_audit.json.

Đối chiếu HF 4.57.6 và PyTorch 2.11: native GQA có thể đẩy T4 sang math kernel
tốn bộ nhớ. Đây là suy luận cơ chế từ source/trace, không phải kernel profiler.
Thêm runtime adapter chung t4-efficient-sdpa-v1: HF explicit repeat_kv + giới hạn
CUDA generation vào efficient SDPA. Giữ model NF4 14B, 4096/512 và margin1.5;
không sửa weights, không giảm ngưỡng gate và không trộn cohort runtime cũ/mới.
Nếu efficient kernel không hỗ trợ phải fail rõ, không fallback ngầm.

Sửa bootstrap uv vào venv, thêm failure latch chặn cell sau, in lỗi/memory probe
trực tiếp. Không thêm sudo/nâng quyền, remote server hoặc né quota. Chính sách
tài khoản/competition vẫn do Kaggle quyết định; không hứa chứng nhận toàn bộ AUP.
Phải qua stress GPU với runtime mới trước khi tuyên bố 4K fit hoặc chạy larger.

## R9 — Quick attention stress đã qua trên Kaggle (2026-11-17)

ZIP NF4_14B_OOM_CHECK_20261116T172805400121Z do người dùng cung cấp, SHA256
e3980f3a8ef62bd2a0896ae72873ca0a926d7a2800626f8b55f38338800ffe8c.
Kiểm tra hash wrapper khớp provenance, cả hai process returncode0/không timeout.
Hai GPU, mỗi GPU hai lần 4096 input + 512 output, cả bốn phép thử đều passed.
Peak allocated 10.554807 GiB; peak reserved10.761719 GiB; margin3.670715 GiB.
Process GPU0 309.960s, GPU1 317.493s, chạy song song. Từng bài decode ~79–90s.
Model Qwen2.5-Coder-14B NF4, revision aedcc2d42b622764e023cf882b6652e646b95671,
Torch2.11.0+cu130, Transformers4.57.6, TeslaT4.

So với R8, attention adapter giải quyết OOM trong đúng bài stress4K đã đo.
Không suy thành mọi real prompt đều an toàn, test accuracy cao hoặc vượt paper.
Chưa sinh test upstream thật trong diagnostic; không chỉnh stress.json/gate cũ
thành passed. Giữ hai archive độc lập; bước tiếp theo là small A/B thật rồi mới
mở larger. Raw probe/hash/provenance đã lưu tại
artifacts/nf4_14b_efficient_attention_pass.json.

## R10 — Small A/B tiếp nối, tái sử dụng có kiểm chứng (2026-11-17)

User yêu cầu tiếp tục và tránh lặp CPU/stress đã đạt. Tạo notebook small_resume
3 Code cells cho cùng phiên Kaggle; source clone local mới + snapshot, output mới.
Tái kiểm tra commits, toàn bộ production hashes, pip freeze, runtime versions,
model/settings và wrapper/probe memory diagnostic trước reuse. Không cài package,
không chạy unit/CPU fixtures/stress lại và không sửa source/plan/gate cũ.

NEW stress.json ghi rõ derived calibration từ diagnostic4K+512 đã đo, copy raw
evidence giữ nguyên origin. Đây là quyết định reuse hardware calibration cho
runtime adapter cùng policy, không biến diagnostic thành efficacy/main-ready.
Do diagnostic cũ thiếu GPU UUID, binding chỉ same-session/two-T4 profile; ghi
giới hạn này trong receipt. Đối chiếu ZIP thật: config/frame/seeds/model revision
khớp plan mới; ba unit tests chống reuse sai đều đạt, fresh clone + đúng overlay
cũng qua. Không đòi người dùng rerun full unit suite trên Kaggle.

Small vẫn chạy model thật cho full upstream init/type/RAG, hai genty modules,
seed42, một vòng, hai arms (4 module-trials), cùng14B NF4 và4096/512; deadline60
phút tính riêng lượt small mới, chi phí calibration cũ báo riêng. Chưa có outcome
small, chưa chạy larger. Cần review ZIP mới trước khi mở larger configured pilot.

## R11 — Council160: dữ liệu khớp artifact, chưa có cải tiến tổng thể (2026-11-17)

Archive EXP_COUNCIL_LARGESCALE_160TRIALS_20261116T165709Z, SHA256
31c7ca1efea55883b71f3a8ffd5f2a22044c26d67262bfb3cbebea24d46b3161.
Audit plan/CSV/summary/160 result khớp;11.720 product source files khớp hashes;
44 pass khớp raw pytest/process, coverage tử/mẫu số và replay. Không thấy sửa
source để lấy pass; đây không phải tái chạy độc lập hoặc chứng minh oracle đúng.

Baseline13/40(32,5%), grounded11/40(27,5%), ranked10/40(25%), verified10/40(25%).
Tổng44/160, first41/160. Critic cứu3/119(2,52%): hai bỏ importTimers, một thêmmath;
ba assert AST giữ nguyên. 50 repair proposals không credit cần review, không
được mặc định gọi tất cả là cheating. Không có mutation/assertion semantic score.
Timer ranked4/10 so với baseline2/10 là tín hiệu cục bộ, không phải “0→82,98%”
success hoặc vượt83% trung bình paper. Sáu Superstring ranked/verified joint-pass
tests giống byte. Cả4arms cóCritic, không phải single-vs-multiagent ablation.

Ghi nhận kết quả bất lợi này; không đổi seed/target/metric để đạt mục tiêu.
160 attempts vẫn chỉ4target clusters đã phát triển. Giữ riêng Council7B+4B với
smallupstream14B, không chỉnh run14B đang chạy từ dữ liệu Council này. Chi tiết
analysis/COUNCIL_160_20261116.md và artifacts/council_160_*. Audit script chỉ đọc
archive và ghi bảng đối chiếu, không đổi score/algorithm.

## R12 — Small14B bị timeout, chưa có số liệu efficacy (2026-11-17)

ZIP UPSTREAM_NF4_RESUME_20261116T174754946339Z, SHA256
603266e8f6360ae0fc86d93d2bed7edc131db23a81448017a80202518d566b3a.
Hai worker -9/timeout ~3587s; cả4 module-trials chưa tới final scoring, coverage/
mutation/paired effect đềuNA. Không gọi bookkeeping0/2 là modelaccuracy0%.
95callsinit/worker, firstgen ở2627s (~43m47), chỉ còn~16phút cho7functions.
Ước lượng1h cho cold fullpipeline quá lạc quan. Baseline122calls xong,
improved121; gen27/26; init5callscapped ởmỗiarm, gencapped4/3; extractionerrors3/2.
Không có model-call exception đã ghi; timeout không phải OOM. Baseline2file
intermediateaccepted không phải module success. Một improved repair đượcupstream
chấp nhận sau bỏ/sửa checks đã bị auditveto, không credit.

Sửa future reporter timeout terminal, táchplaceholder4 khỏicompleted0, all-unmeasured
rateNA. Thêm progressitems trongtừngstep, function/round, module/mutant, workers,
remainingtime; thêm function_database_index thànhstep11. Không coi10/10 cũ là
toànbộinitđãxong hoặcmodelcallcountlàtổngbiếttrước. Consolegiữstructuralevents.
Xem analysis/UPSTREAM_14B_SMALL_TIMEOUT_20261116.md.

## R13 — Remote monitoring, exact-prefix reuse và tránh GPU trùng (2026-11-17)

User cấp URL Jupyter chính thức của Kaggle; chỉ giữ credential trong bộ nhớ,
không ghi source/nhật ký. Kết nốiAPI/kernel được. Prefixreuse xác minh95/95
promptkeys vàrawoutputs,190logicalcalls/95freshcalls,95uniqueprompts,5capped
summaries giữ nguyên. Chỉ reusegreedyinit, không importtest/repair/outcome;
giữchi phícoldrun riêng. Unit/fixture vàfull143tests qua sauprogress/cachefix.

Có một smallretry đã chạy ởUPSTREAM_NF4_RETRY_20261116T190701623856Z. Agent thiếu
kiểmtravRAMđangbậntrướckhởiđộngthêm retry190848039637Z, gâyloadOOMdohaiworker
khácđãgiữ~10,4GiB/GPU. Giữ lỗi190848riêng, khôngkilljobđangchạy. Xácnhậnjob190701
cùng14BNF4/4096+512/seed42/1round/4moduletrials vàđủ95prefix; chỉtheodõinólạikhông
khởiđộngthêm. Không quy loadOOMtrùngtài nguyên thành chấtlượngmodel.

Thêm future GPUlease theoUUIDvàcurrentfreeVRAMchecktrướcmodel, khôngkillprocess,
khôngđổimodel/budgethaynéquota. Sửa hardware_budget_ok khiOOMxảyra trongmodel
constructor trước khi backendđượcgán. Full145CPUtests vàfocusedGPUlease/progress
testsqua; không thay code/source của job190701 đang chạy. Largerstillnotlaunched.

## Quy tắc ghi nhận từ lượt tiếp theo

- Chốt cấu hình/plan trước inference; giữ bản run fail và mọi sửa đổi protocol.
- Gắn nhãn development/held-out; không chuyển hai target đã tuning sang held-out.
- Báo mọi outcome và mẫu số planned/finished/scored/eligible; missing khác zero.
- Tách quan sát khỏi suy đoán nguyên nhân; không gán công cho Critic/setup khi
  nhiều biến cùng đổi. Không suy từ model load hoặc pass rate ra oracle accuracy.
- Khóa tiêu chí metric, fault pool và exclusions trước đánh giá; giữ test/spec/oracle
  và mutant verdict khỏi retrieval của generator theo protocol.
- Review assertion dựa trên source/spec độc lập; không đơn thuần chép actual output.
- Khi muốn tuyên bố thay model lớn của Test4Py, cần matched upstream controls,
  held-out projects và fault-detection evidence; không so hai aggregate khác cohort.
- Mỗi lần chạy tiếp theo phải thêm mục nhật ký mới kèm ZIP hash và kết quả thực tế,
  kể cả không có cải thiện. Không sửa R2 thành kết quả thuận lợi hơn.


### R8 bổ sung — chỉ kiểm tra lỗi đang chặn

Theo yêu cầu khẩn, cung cấp kaggle_14b_quick_oom_check: chạy trong phiên Kaggle cũ, dùng source/venv/weights đã có, không cài thêm và không sửa plan/source cũ. Chỉ thử 4096+512 hai lần/GPU, chạy hai GPU song song, timeout 900 giây/process. Dùng wrapper attention trong process, lưu config/wrapper/probe hashes và ZIP riêng. Đây là diagnostic, không được dùng để tự đánh dấu full gate ready hoặc báo efficacy. Bỏ qua unit/prepare/fixture vì lượt trước đã qua; không bỏ qua stress sau thay runtime. Bản tích hợp đã qua 135 CPU tests; numerical equivalence HF repeat_kv được kiểm tra trên CPU, GPU fix vẫn pending.


## R12 — Small 14B thật: baseline có kết quả, improved bị gate loại (2026-11-17)

Qua Jupyter Kaggle do người dùng cung cấp, hoàn tất warm-prefix screen
UPSTREAM_NF4_RETRY_20261116T190701623856Z: 4/4 module-trials, wall2053,06s.
ZIP SHA256 604d75c7e03bca094984d51bf4421860b6772c589df69f6866b1fbed11a0dcf6.
Baseline: repeat5 nodes, line8/8, branch2/2, mutant1/1; args15 nodes,
line18/20, branch0/0=NA. Ba file retained không mất/đổi assertion theo audit;
review source xác nhận constructor/properties/metadata, nhưng không có
iteration và không chứng minh lifecycle toàn hệ thống.

Improved không có test được tự động công nhận:3 candidate bị cắt/khối code
không hoàn chỉnh;3 repair proposals được upstream chấp nhận nhưng thay đổi
hoặc bỏ assertion/test nên bị preservation gate loại;1 proposal upstream
không chấp nhận. Không gọi mọi thay đổi assertion là sai ngữ nghĩa.
Coverage/mutation thiếu giữ NA. Gate larger_ready trong ZIP là readiness
kỹ thuật, không phải chất lượng phương pháp; quyết định thực tế không mở larger.
Kiểm toán raw đã đối chiếu12 file production, exit, cache, pytest replay và
coverage tử/mẫu số. Xem analysis/NF4_SMALL_REMOTE_20261117.md và
artifacts/nf4_14b_warm_small_audit_20261117.json.

Chuẩn bị single-test-v1 dùng chung cả hai arm để xử lý output nhiều test bị
cắt ở512tokens; không đổi model, budget hay scoring gate.159 CPU tests pass;
overlay79file fresh clone qua18 targeted tests và2 scripted upstream fixtures.
Đã launch compact ở phiên cũ nhưng chưa lấy được output trước khi URL timeout;
không gán điểm cho lượt chưa xác nhận. Phiên mới rootworking trống, Transformers
base5 nên dựng venv4.57.6, prepare và stress mới; chỉ reuse summary14B được
kiểm chứng, không reuse calibration phiên cũ. Fresh compact hiện đang chạy,
local monitor tải ZIP khi xong. Chưa có kết quả mới để kết luận cải thiện.

Người dùng chấp nhận số module nhỏ, chọn module tốt cho ứng dụng thực tế.
Phải ghi curated/development, review oracle và replay, đo latency; không suy
ra ngang/vượt toàn bộ183module paper từ một subset chọn thuận lợi.


## R14 — Cơ chế API contract riêng, chưa có kết luận hiệu quả (2026-11-17)

Theo yêu cầu phải có đóng góp thực sự và tránh hai mẫu bị bias, triển khai
api-contract-v1: AST-only phân biệt property/method và lexical ownership của
closure, có chữ ký/hash source, tối đa2500chars, không sinh expected output.
Hai arm baseline/api_contract dùng chung chỉ dẫn file pytest ngắn (cho phép
nhiều test) và preservation gate trong adapter upstream. Không trộn bundle
legacy improved vào treatment này. single-test-v1 đã thất bại khi model trả
file nhiều test; không dùng lại restriction đó cho cơ chế mới.

Khóa development probe5target genty/10lượt sinh, một seed42, không repair/prune.
Dùng initial prompts thật từ upstream đã lưu, chỉ bổ sung API facts ở treatment;
đây là component diagnostic, không phải end-to-end hay held-out confirmation.
173 kiểm tra CPU và hai scripted upstream fixtures đã qua; các số đó không
đo chất lượng LLM. Mã nguồn chạy được freeze trong archive notebook.

Phiên Kaggle API_CONTRACT_DEV_20261117T020312879124Z: cả hai T4 đã qua stress
4096+512 lặp, conservative headroom tối thiểu3,67GiB. Đang sinh10candidate14B;
chưa có kết quả hoàn chỉnh, chưa tuyên bố tăng chất lượng. Có monitor tải ZIP
khi terminal; không ghi credential/Jupyter URL vào repo.

Khóa frame12module/bốn project ngoài development,3seed42/43/44=72armtrials
trước outcomes. SHA256frame:
c2ceaae4e0c8374a2e18ebc6ddbbd900f7e5f6bb0d237d12bd4aba10b1c3a9c3.
Đây mới là selection frame; chuẩn bị dependencies/import riêng trước inference.
Không thay module thất bại bằng module điểm tốt. Bốn project là bốn cluster,
không coi36target-seed pairs là36project độc lập hay đảm bảo ý nghĩa thống kê.
Xem docs/API_CONTRACT_MECHANISM.md. Chưa có kết quả7B hoặc superiority so paper.


### R14 kết quả development v1 và ablation tiếp theo

API_CONTRACT_DEV_20261117T020312879124Z hoàn tất10/10lượt, ZIP SHA256
6dfc29d3c83fc1d13ec77bfc64ba68fa1636c6baf7c86ed0e8bfff4b242c221d.
Suite ổn định và reach target: baseline0/5, APIcontract1/5. Candidate tốt có
6/6test pass, line8/8, branch2/2 trên repeat; không sửa/prune test. Lỗi
FileExistsError ở đường dẫn report mutant được giữ trong archive gốc. CPU
recovery trên cùng runtime/candidate replay6/6 rồi kill mutant biên cũ1/1;
không thêm LLMcall. Recovery ZIP SHA256
8a77dac7bf543e8eddfb5987fe367b52827ce23da9e646c4e4f36b8c4663b422.
Đã sửa đường dẫn scoring cho các run sau, thêm regression thực thi mutant.

Review: suite tốt kiểm tra metadata, zero/positive/large counts, ValueError
âm, TypeError thiếu tham số và metadata composition với dataset. Không
kiểm tra exact exception message hoặc toàn bộ runner thực sự lặp test. Các
suite độc lập có assertion/scenario khác nhau, không giả là cùng oracle.
Inputtokens5869→7141(+21,67%), generationtime240,87→255,18s(+5,94%).
Property-call sai và import nestedwrap vẫn tồn tại cả hai arm. Một target
tốt hơn trong một project không đủ kết luận phương pháp cải thiện tổng quát.

Quan sát development cho thấy generatedusage upstream mâu thuẫn production
decorators/closure scope. Khóa cohort mới source-first-v2, ba arm baseline,
source_only, api_contract;5target/15lượt, cùng model/seed/budget, không poolv1.
source_only thay mô tả sinh sẵn bằng source AST-rendered; api_contract thêm
facts trên cùng source. ManifestSHA256
e769c5fe9037dfff7bf1f707bbeb004439f5b84f74f4537438e7ccee0a7ceeb0.
Đang chạy API_SOURCE_FIRST_DEV_20261117T023613600950Z, giữ sourcefreeze
riêng; chưa có kết luận. Các model outcomes held-out vẫn chưa chạy.

Preflight CPU cuối đã import đúng12/12module/4project, sourceproduction
không đổi. dfsql dùngPy3.9 do collections.Iterable; cácprojectkhácPy3.11,
pytest8.3.5/coverage7.6.1 chung. Đã giải quyết dependency scikit-learn bị
thiếu trong setup.py của pymssa; record mọi fail kỹ thuật trước đó, không
thay target. Packagebuild/lib không phải production source; không sửa source
để import pass. Manifest/freeze xem artifacts/api_contract_heldout_preflight_20261117.json.


## R15 — Source-first v2 xong, held-out component72lượt và ứng dụng14test

Cohort API_SOURCE_FIRST_DEV_20261117T023613600950Z hoàn tất15/15: baseline
0/5, source_only2/5, source+facts3/5suite ổn định/reach target. Facts thắng
hai property nhưng thua closure; cả hai arm source đều fail factory. Tổng
inference236,05/208,12/167,46s theo arm; không gồm model load và preparation.
ZIP SHA25633a54ca54b9fe200934fec4be70d89f972a84ddc61f05f2093d824132e709a6d.
Review các getter và iterator assertions theo source, không sửa expected
values. GentyArgs không có mutant hợp lệ trong pool cũ nên faultscoregetter
vẫnNA. Đây là một project phát triển, chưa phải kết luận tổng quát.

Sau review, khóa componentheldout source_only vs source+facts,12module/4project,
seeds42/43/44=72trials, model14BNF4, cap4096/512, zero repair/pruning.
ManifestSHA256e89de4086cf3ba2ab2d62fafe59709a792a5e129dd297c801002f404e78bf6e5.
Không gọi đây là baseline Test4Py đầy đủ: cả hai arm dùng source thật, khác
APIfacts. Mục đích đo contribution riêng trên project chưa dùng phát triển.
Run API_HELDOUT_COMPONENT_20261117T025213627216Z đã qua12/12imports trên
Kaggle rồi bắt đầu inference; không đổi source/prompt/scoring theo outcomes.
Đã giữ engineeringpreparation failures và resolvedlocks trong ZIP SHA256
762a1bfd8e55f2bb344c6e7577d7e50eebc7c7b8a6ce874652276e2cefdca6c9.
Bug mutantpool nestedBinOp cùngstartcoordinates được sửa trước inference;
regressiona*b*c xác nhận hai fault khác nhau.180 regressiontests local pass
trong80,073s; đây là engineeringchecks, không phải tỷ lệ LLM.

Ứng dụng riêng: giữ nguyên12test baseline curated, thêm nguyên văn2test từ
API-v2 args/iterator, không bỏ/sửa bất kỳ assertion cũ. Ba freshprocessPy3.12
pass14/14, argsline18/20→20/20, repeatgiữ8/8 vàbranch2/2. Hai iteratorfault
bổ sung(app development, chọn sau review, không phải pool nghiên cứu khóa)
sống sót cả hai ở bộ12test và bị killcả hai ở bộ14test. Đó là regression
improvement cho bộứngdụng, không phải kết quả thuật toán vượt paper.
Bundle research/application/14b_genty_extended_20261117.zip SHA256
cd9936b59adb216224d073caca7936a6cb03bd172ffb2cf83918589cc0c74018.


### R15 kết quả held-out cuối: tín hiệu nhỏ, chưa đạt mục tiêu

Đã lấy đủ72/72lượt, rawZIP SHA256
99eb3c3d117424c64984441b20d51e317600070e86c6d18657279b7ec479b1be,
CRC đúng, sourceintegrity72/72. Fullsuitepass/replay: source_only2/36,
APIfacts4/36. Tiêu chí positivePython targetcoverage:1/36vs3/36. Hai lượt
thắng đều ởKafkaCompleter.is_cluster_command(seed43,44); một target trong
một project, không coi là hai phép xác nhận độc lập. Seed43killfaultbiên
LtE→Lt, seed44khôngkill. NativeNumba vtmat_ts_startidxseed42pass/replay cả
haiarm nhưngPythonbodycoverage0; giữrawmetricvàbáogiớihạnđo, không gọi
đó là bằng chứng targetkhôngđượcgọi. Socketsetupseed44passcảhaiarm, checks
còn yếuvàportcốđịnh cần review; không gánsemanticaccuracy100%.

Inputtokens23865→35187(+47,44%), inference1530,81→1555,02s(+1,58%).
Không có speedup ngoài development. Tỷ lệ tuyệt đối thấp:24/21pytestfails,
10/11cappedoutputs theoarm. Không mởfullpaper, chưa chạy7B hoặc chứngminh
ngang/vượtTest4Py. Source-onlycontrol là ablation thànhphần, khôngphải
toànpipelineupstream. Report analysis/API_SOURCE_HELDOUT_V2_20261117.md,
accounting artifacts/api_source_heldout_v2_analysis_20261117.json.

Auditport:4reportAddressinuse, ba candidatecóNameErrorsocket trước các
lỗikếtiếp vàmộtcase doublebind. ReplayCPUlocaltuầntựnguyên4candidate
vẫnfail;2casebịPermissionError doportthấptrênlocal, nênkhônggọiđólà
replaycùngmôitrườngKaggle. Giữnguyên72outcomes, khôngđổioracle.
Bộứngdụng14testcảitiếnđãđo làcurateddevelopmentriêng, khôngdùngđểche
kếtquảheldoutthấp. Cácđiềuchỉnhdựavàoheldoutnàycầntậpxácnhậnmới.
