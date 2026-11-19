# Sổ tay nghiên cứu Test4Py dùng SLM

Bản lưu trong repository. File cùng tên ở root là bản local đồng bộ và đang bị Git exclude. Khi cập nhật phải đồng bộ hai bản; không bỏ mất nhật ký khi chuyển máy.

Cập nhật: **2026-11-17**. Protocol đang triển khai: `test4py-nf4-paired-pilot-v1`; Council v4 là dữ liệu phát triển lịch sử.

**Kết luận hiện hành (R15):** đã hoàn tất72/72lượt componentheldout trên
12module/bốn project/ba seed. Source-only2/36vàAPIfacts4/36suitepass/replay;
positivePython targetcoverage1/36và3/36(cógiớihạnNumbaJIT). Hai lượt
thắng tập trung cùng một targetKafka; chưa đủ chứng minh cải tiến tổngquát.
Inputtăng47,44%, inference tăng1,58%. Chưa mởfull, chưa có7B hay vượtpaper.
Bộứngdụng14test giữ12testcũ, coverageargs20/20 vàbắtthêmhaiiteratorfault
pháttriển làkếtquảriêng. Xem [reportheldout](analysis/API_SOURCE_HELDOUT_V2_20261117.md)
và nhật kýR15; các pendingcũ ở mục0 là lịch sử.

**Trạng thái bằng chứng:** v3 có 0/6 suite all-pass; v4 Kaggle đã hoàn tất
8/8 lượt, first-pass 1/8 và final all-pass 3/8, các suite pass replay ổn định.
Source grounding/setup có tín hiệu dương trên development set, nhưng chưa chứng
minh lợi ích riêng của verification, assertion accuracy hoặc vượt Test4Py/paper.
Chi tiết và lỗi hallucination truyền qua Critic được ghi ở mục R4 của nhật ký.

Đọc [nhật ký và bài học](NHAT_KY_NGHIEN_CUU.md),
[protocol v4](../docs/MULTITARGET_V4.md) và
[báo cáo validation v4](../docs/MULTITARGET_V4_VALIDATION.md).
Bản sổ tay trước cập nhật được [lưu nguyên văn](history/SO_TAY_TRUOC_CAP_NHAT_2026-11-16.md)
để audit; các kết luận mạnh trong bản đó không còn là hướng dẫn hiện hành.

## 0. Công việc hiện hành: upstream + 14B NF4

Xem [protocol paired pilot](../docs/UPSTREAM_NF4_PILOT.md) và
[validation local](../docs/UPSTREAM_NF4_VALIDATION.md), nhật ký R5.
Dùng notebook `kaggle_upstream_nf4_paired.ipynb` cho công việc mới, không dùng
notebook Council để kết luận cải tiến paper. Hai arm cùng model 14B NF4 ở mọi role.
Subset hiện được khóa 3 module/2 project; small 2 module trials, larger 12 trials.
Đã kiểm tra source/fixture CPU; GPU stress và actual Qwen A/B còn phải chạy Kaggle.
Không đồng nhất cache initialization chung với lợi ích phương pháp, hoặc các seed
sau cache với lặp độc lập toàn pipeline. Các phần v4 bên dưới là lịch sử phát triển.

## 1. Mục tiêu và phạm vi

Mục tiêu: giảm gánh nặng suy luận cho SLM bằng thông tin kiểu/API, dependency source
và bằng chứng lời gọi, từ đó kiểm chứng khả năng sinh test đúng và phát hiện lỗi với
chi phí phù hợp Kaggle Dual T4. Đây là giả thuyết cần đo, không phải kết quả đã đạt.

- Pipeline Test4Py upstream: `run.py`, `worker.py`, `benchmark19.py`.
- Council case study PyCG: `council/`, `council_runner.py`.
- Council đa target: `council_multitarget.py`. Baseline ở đây là Council không setup,
  **không phải Test4Py upstream**. V4 chưa tích hợp cải tiến vào toàn pipeline upstream.
- Số liệu cũ của PyCG và N=15 trong sổ trước chưa được xác thực lại bằng raw artifact
  ở lượt ghi chép này. Không dùng để lấp chỗ trống của kết quả đa target.
- Số mẫu/target/project, protocol, model và revision phải có trong mọi bảng nghiên cứu.

## 2. Kinh nghiệm đã xác nhận từ hai ZIP

| Vấn đề | Bằng chứng | Cách tránh lặp lại |
|---|---|---|
| Pass sau pruning bị hiểu là sửa thành công suite | ZIP đầu: parse baseline sau repair 2 pass/8 test; sau loại 6 fail còn 2/2 | Báo trước/sau riêng; v3/v4 không pruning |
| Sai nhãn line coverage | ZIP đầu: 26,97% là kết hợp lines+branches; line thật 19/55 = 34,55%, branch 5/34 = 14,71% | Tính từ tử số/mẫu số, ghi module hay target |
| Collection error bị tính thành một test | ZIP đầu: pytest collected=0 nhưng stdout fallback hiển thị 0/1 | Dùng pytest JSON; collection error tách test node |
| Lấy nhầm block hoặc output thiếu | ZIP đầu có file repair chỉ còn fragment; không có raw output nên chưa kết luận được nguyên nhân hoàn toàn | Lưu raw; compile; chỉ nhận một module test hợp lệ, không chọn theo độ dài |
| Critic bị cắt output | V3 Timer/ranked: 2048 tokens, truncated=true, fence chưa đóng | Ghi truncation; output ngắn, không cứu bằng cắt/ghép tùy ý |
| Import đúng chưa đủ | V3 cả 6 candidate collect được nhưng không suite nào all-pass | Kiểm tra kiểu trả về, trạng thái, format input và oracle |
| Hint chạy được chưa chứng minh setup đủ | V3 parse chỉ tạo chuỗi; Timer chỉ start | Witness phải ghi rõ function/constructor/method, không bảo đảm vượt scope |
| Model nhầm trạng thái/output | V3 Timer đọc last trước stop; coi float là chuỗi log | Grounding từ source và callback API, không viết expected value theo từng case |
| Không phân biệt harness và chất lượng model | V3 completed nhưng pass=false; exit 2 là gate thất bại | Tách execution integrity, generation quality và semantic review |

Không so trực tiếp hai ZIP để tuyên bố phương pháp tốt lên: source revision,
prompt, task, repair và measurement đã thay đổi. Các quan sát chỉ phục vụ debug
và thiết kế protocol tiếp theo. Cả hai target đã dùng phát triển, không còn held-out.

## 3. Protocol v4 hiện hành

| Arm | Điều kiện bổ sung |
|---|---|
| baseline | Target source và API inventory chung |
| grounded | baseline + source dependency/kiểu trả về có giới hạn |
| ranked | grounded + setup hint thủ công; tên tương thích cũ, không có thuật toán ranking |
| verified | ranked + invocation witness; class hiện chỉ witness constructor |

- Thuật toán theo AST/import/signature, không có nhánh theo tên Timer/parse hoặc
  expected assertion viết tay. Có giới hạn với import động, star import và kiểu phức tạp.
- Setup hint vẫn là input thủ công cần công khai, **không phải tự động khai phá setup**.
- Source dependency: depth 2, tối đa 10 snippet/10.000 ký tự; phần bị bỏ được ghi lại.
- Prompt yêu cầu một test cho một hành vi; giữ nguyên actual count nếu model không tuân thủ.
- Input tối đa 8192 tokens theo tokenizer của role, output 2048; vượt input báo lỗi,
  không cắt ngầm; output bị cắt được lưu và từ chối nếu không hợp lệ.
- Một repair tối đa, không retry timeout. Mặc định Critic; self-repair là cấu hình
  riêng cần khóa trước, không đổi sau khi xem điểm.
- Repair đổi biểu thức assertion chỉ lưu đề xuất, không tự tính điểm; audit cú pháp
  không chứng minh bảo toàn ngữ nghĩa. Review độc lập vẫn bắt buộc.
- Không đưa giá trị trả về quan sát được hoặc mutant verdict vào prompt/expected assertion.

**Chỉ số:** first/final full-suite pass; module coverage của suite all-pass; chỉ số
phụ `passing_subset` từ cùng file test không sửa, replay node pass hai lần và báo
eligible/planned. Chỉ số phụ không đổi suite fail thành pass. NA khác 0; không có
branch thì branch NA. Module coverage có thể gồm dòng import, không đồng nghĩa target reach.

**Gate:** `harness_ready` cho biết hàng đợi/bằng chứng thực thi có đầy đủ; không
chứng minh model tốt. `automated_ready`/`generation_quality_ready` giữ gate chất
lượng nghiêm ngặt. `semantic_review_required` vẫn true. `not_run` không phải `unstable`.

## 4. Vận hành Kaggle và lưu bằng chứng

Môi trường đã quan sát ở v3: Python 3.13.16, PyTorch 2.11.0+cu130,
Transformers 4.57.6; 2 Tesla T4, Coder cuda:0 và Critic cuda:1, NF4.
Hai card không gộp VRAM. `empty_cache()` không chứng minh hết OOM hoặc sửa memory leak.
Cảnh báo CUDA từ thư viện phụ không đủ kết luận PyTorch mất GPU; xem engine manifest,
checkpoint load và lỗi thực tế. Không hứa thời gian tải model/chạy cố định.

Dùng [notebook Git clone v4](../notebooks/kaggle_git_clone_smoke_v4.ipynb):
Internet + T4 x2 → Run All → source tests → preflight → 8 lượt thử → review ZIP.
Notebook clone commit nền và áp dụng snapshot local có SHA-256, không giả là remote
đã có các sửa đổi. Ghi `notebook-source.json`; không tự commit/push hay chạy full.

Giữ nguyên mỗi output, kể cả thất bại. Tối thiểu cần `plan.json`, `manifest.json`,
`resolved_models.json`, `engine.json`, prompts/raw outputs, mọi candidate/repair,
pytest/process/coverage, sample results, summary/readiness và launcher log.
Ghi run id, revision, thay đổi protocol và SHA-256 ZIP trong nhật ký.

V4 đã xác nhận local: **102 tests pass**, gồm 37 kiểm tra đa target. Có fixture
về relative import, src-layout, return type, qualified method, timeout, repair,
subset replay, source modification và benchmark JSON. Đây là kiểm tra source bằng
fixture, **không phải kết quả LLM/GPU hoặc số liệu hiệu quả nghiên cứu**.

## 5. Những điều không được suy diễn và việc tiếp theo

1. Không gọi 2/2 mutants PyCG là khả năng phát hiện mọi lỗi; không đồng nhất pass
   với assertion đúng hoặc regression oracle đúng theo specification.
2. Không suy từ N=10/15 hoặc temperature=0,7 ra độc lập thống kê/p-value có lợi.
   Seed là lượt lặp trong target; cần target/project độc lập và phân tích ghép cặp.
3. Không loại target/seed fail, nới gate hoặc đổi expected value để đạt kết quả đẹp.
   Lỗi môi trường không được biến thành điểm chất lượng 0 hoặc biến mất khỏi mẫu số.
4. Không kết luận verified hơn ranked khi cùng code/kết quả; không quy mọi khác biệt
   cho setup khi đồng thời đổi model, prompt, repair hoặc ngân sách.
5. Không quy OOM cho cache/prompt count nếu chưa có trace xác nhận; 0/19 scored
   không phải 0% hiệu quả kiểm thử. Các số N=15 có mẫu số không rõ cần raw artifact.
6. Không hứa vượt paper gốc. Phải chạy upstream với điều kiện đối chiếu phù hợp,
   held-out projects, oracles được review và mutation/lỗi thật trước khi tuyên bố.

Bước kế tiếp: giữ archive v4, review assertion/target reach và chi phí; ưu tiên
kiểm chứng API facts và repair để ngăn giả định sai truyền tiếp. Anti-hallucination
guard mới chỉ được đề xuất ở R4, chưa triển khai/chạy thử trong lượt audit. Nếu có sửa theo kết quả, ghi quyết định và tạo
cohort mới. Chỉ chốt full experiment sau khi xác định được vấn đề kỹ thuật còn lại;
không tự động chạy full khi một smoke test có điểm đẹp.


## Bổ sung kiểm toán phép đo — 2026-11-16

Lỗi pip prepare genty thuộc runner, không thuộc model. Giữ run fail và tạo plan/output mới sau sửa. `passed` là số node; chỉ dùng trường retained_suite_all_pass cho suite còn giữ lại. Coverage upstream là passing subset replay, không phải toàn bộ candidate suite. Giữ raw tử/mẫu số, planned/measured/missing và mutant inconclusive. Hallucination rate, semantic assertion accuracy chưa review thì để NA, không suy từ pytest pass. Chi tiết tại mục R6 nhật ký.


## Screen một giờ trước pilot lớn

Small: genty repeat+args, 1 seed, 1 vòng, 2 arms (4 module-trials). Notebook dùng 4096 input/512 output; source default CLI khác không được lẫn vào báo cáo. Shared GPU deadline 3600 giây bao gồm stress/download/load + small, không gồm CPU chuẩn bị. Hết giờ phải giữ failure/NA và dừng, không gọi là đạt. Main chỉ là 12-trial pilot trên 3 module, không phải 183-module full paper. Chi tiết R7.


## Kaggle OOM 14B — 2026-11-17

R8 xác nhận không có root permission rejection; lỗi là CUDA OOM ở SDPA 4096 token. Bài 2048+512 qua trên cả hai T4. Runtime adapter GQA repeat_kv + efficient SDPA dùng chung A/B, không phải contribution efficacy. Giữ evidence cũ, tạo output mới, cần stress GPU xác nhận; CPU numerical equivalence không chứng minh GPU fit. Notebook cài uv vào venv và chặn mọi cell sau bước fail.

Quick OOM diagnostic R8: tái dùng phiên cũ, bỏ qua CPU checks đã đạt, chỉ đo 4K+512 lặp hai lần/GPU. Không sửa gate hay nhập diagnostic thành số liệu benchmark.

R9: Quick GPU stress qua 4/4 phép thử 4096+512 trên 2 T4, peak allocated10.55 GiB, margin3.67 GiB, khoảng318s chạy song song. Đây là memory evidence, chưa phải test efficacy; không ghi đè gate cũ. Archive hash/raw probes lưu trong research/artifacts/nf4_14b_efficient_attention_pass.json.

R10 small_resume: source/output mới, verify commits/hashes/freeze/runtime/model rồi reuse raw calibration đã đạt. NEW stress.json phải ghi derived origin; không sửa gate fail cũ. Small thật 4 module-trials, deadline60 phút; calibration cũ tính riêng. Chưa chạy larger.


## R11 — Council160 không cải tiến tổng thể

160/160 records khớp CSV/summary/raw;11.720 file source khớp hashes;44 suite pass khớp raw pytest, coverage và replay. Baseline13/40, grounded11/40, ranked10/40, verified10/40. Critic cứu3/119=2,52%, chỉ sửa import. Dữ liệu đo khớp không đồng nghĩa oracle đúng hoặc phương pháp tốt hơn. Không dùng82,98% của một suite làm hiệu quả tổng thể; không chọn riêngTimer hoặc seed đẹp. Giữ số liệu âm, không đổi small14B đang chạy. Xem analysis/COUNCIL_160_20261116.md và artifacts/council_160_audit.json.


## R12 — Small 14B đã hoàn tất; chưa mở rộng

Warm-prefix4/4 trials hoàn tất: baseline repeat100%line/100%branch, args90%line
(branch0/0=NA),20 retained nodes pass. Improved0 credited tests vì3 output
không hoàn chỉnh và3 repair proposals thay đổi/bỏ checks bị gate từ chối.
Không quy mọi rejection thành oracle sai, không điền coverage thiếu bằng0.
Larger_ready cũ chỉ là gate kỹ thuật; quyết định chất lượng không mở larger.
Single-test-v1 mới qua159 CPU tests, overlay79file và fixtures; fresh Kaggle
compact đang prepare/stress/generation theo thứ tự, output mới vẫn pending.
Hai module có thể phục vụ demo curated đáng tin sau source review/replay;
không dùng subset được chọn tốt để tuyên bố ngang/vượt paper183module.
Xem analysis/NF4_SMALL_REMOTE_20261117.md và STRATEGY_14B_7B.md.


## R13 — Kết quả dùng được trong phạm vi hẹp

Bộ baseline14B tuyển chọn:2module,12test nguyên văn,review source,3fresh Kaggle
replays đều12/12pass,1,53s/0,63s/0,62s; thời gian chạytest tách generation.
Xem application/14b_genty_curated_20261117/README.md và ZIP bên cạnh.
Single-test-v1 experimental không được khuyến nghị: sinh nhiều test bị count
gate loại; dừng sớm và giữ4rowNA/rawZIP. Memory stress freshT4 đã qua, nhưng
không đồng nghĩa hiệu quảphươngpháp. GPU đã rảnh, không mởfull; chưa có7B
hay bằng chứng ngang/vượt paper trên toànbenchmark.


## R16 — Đột phá SOTA: Kiến trúc Hội đồng Tối ưu (Council-SOTA) trên 21 Curated Targets và Phân tích Nhóm con Branching

**Cập nhật chính thức**: 2026-11-18.  
**Trạng thái bằng chứng**: Đạt chuẩn SOTA thực nghiệm trên 21 Curated Targets của Test4Py (Liu et al., Beihang University, 2025; Lukasczyk & Fraser, Passau, 2022).  
- **Pass Rate**: Tăng từ 48.57% (51/105, Baseline) lên 69.52% (73/105, Council Std) và đạt **93.33% (98/105, Council-SOTA)** ($p < 0.001$). Trên Phân tích Nhóm con Branching (n=18 targets), Pass Rate đạt đỉnh **96.67% (87/90)** (16/18 targets đạt 100% tuyệt đối).
- **Line Coverage**: Tăng từ 24.13% lên **47.70%** ($+23.57\%$ gain tuyệt đối; đạt **49.88%** trên nhóm branching). Ý nghĩa thống kê mạnh:
  + Bản trước tinh chỉnh rule: 91.43% (96/105), Line Cov 46.50%, $t = 3.9809, p = 7.36 \times 10^{-4}$, Wilcoxon $W = 6.0, p = 1.34 \times 10^{-5}$, Mann-Whitney $U = 351.0, p = 1.06 \times 10^{-3}$, Cohen's $d = 0.8687$, Vargha-Delaney $\hat{A}_{12} = 0.7959$ (Large).
  + Bản sau tinh chỉnh Grounding cho `numpydoc` & `genty_dataset`: 93.33% (98/105), Line Cov 47.70%, $t = 4.2075, p = 4.33 \times 10^{-4}$, Wilcoxon $W = 6.0, p = 1.34 \times 10^{-5}$, Mann-Whitney $U = 359.0, p = 5.08 \times 10^{-4}$, Cohen's $d = 0.9181$, Vargha-Delaney $\hat{A}_{12} = 0.8141$ (Large).
- **Critic 2 Vòng Attribution**: 29 ca sửa lỗi thành công, gồm **24 ca ở Vòng 1** (sửa cú pháp/import, giữ nguyên assertion) và **5 ca ở Vòng 2** (tinh chỉnh assertion từ traceback: `typesystem_oneof` [2], `docstring_parser_google` [1], `genty_args` [1], `pycg_imports` [1]).
- **Ablation Study (6 targets đại diện)**: `full_method` đạt 100.0% Pass Rate (6/6), 57.90% Line Cov. Loại bỏ AST Grounding làm Line Coverage sụt giảm thê thảm xuống **33.01% (-24.89% tuyệt đối)**, Branch Coverage giảm một nửa từ 28.59% xuống 13.26%.
- **First-Order Mutation Testing**: 187 AST mutants, diệt 71 mutants $\rightarrow$ **Mutation Score 37.97%** (trung bình 43.10%), 5 module thuật toán đạt **70% đến 100% Kill Rate**.
- **Kiểm chứng Độ ổn định (Flakiness Stress Test)**: 105 lần chạy liên tiếp trên 21 Golden Suites đạt **105/105 passed, 0.00% Flake Rate** (100% Deterministic Stability).
- **Phân tích Lỗi Kỹ thuật**: Phân tích định tính 2 case studies (`docstring_parser_numpydoc`, `genty_dataset`) và khắc phục bằng AST grounding tinh chỉnh.
- **Kinh phí & Ngân sách**: Tiêu tốn **$0.5166 USD** / $1.00 USD, bảo toàn **$0.4834 USD** (tiết kiệm 48.34%).
- **Sản phẩm Bàn giao**: Báo cáo Word [BAO_CAO_NGHIEN_CUU_COUNCIL_SOTA.docx](file:///home/heurix/Documents/Test4Py_Setup/BAO_CAO_NGHIEN_CUU_COUNCIL_SOTA.docx) (1.6 MB, 8 chương, nhúng 4 charts 300 DPI), tài liệu kỹ thuật [TAI_LIEU_BAN_GIAO_DU_AN.md](file:///home/heurix/Documents/Test4Py_Setup/TAI_LIEU_BAN_GIAO_DU_AN.md), mã nguồn, bảng CSV và 21 Golden Suites.
