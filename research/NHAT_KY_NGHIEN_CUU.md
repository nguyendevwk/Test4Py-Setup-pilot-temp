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
