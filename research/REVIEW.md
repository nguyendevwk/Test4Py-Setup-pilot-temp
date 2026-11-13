# Đánh giá nghiên cứu: từ suy luận kiểu sang setup có kiểm chứng

Ngày đánh giá: 2026-11-14. Phạm vi: source hiện tại, paper arXiv v2, log Kaggle người dùng cung cấp; chưa có kết quả sinh test cuối của bốn arm.

## Kết luận có thể bảo vệ ở thời điểm này

Đây là **pilot cơ chế có tiềm năng**, chưa phải bằng chứng rằng phương pháp mới vượt Test4Py trên benchmark. Đóng góp ứng viên là tìm một chuỗi thao tác sản phẩm làm đối tượng thỏa tiền điều kiện trạng thái, kiểm chứng chuỗi trước khi đưa vào prompt và định lượng lợi ích so với cùng chuỗi ứng viên không được kiểm chứng. Thay model, hỗ trợ Kaggle, hai GPU và dashboard là đóng góp triển khai, không tự chứng minh đóng góp thuật toán.

Theo log Kaggle: smoke check và validation PyCG thật đã pass; hai worker đã nạp model trên GPU 0/1. Validation dùng oracle nội bộ. Nó kiểm tra hạ tầng và bộ chấm, **không phải mutation score của test do model sinh**. Lượt sinh test chưa có báo cáo cuối, nên mọi chênh lệch chất lượng hiện là **NA**.

## Mốc tham chiếu từ bài gốc

Nguồn: [Test4Py arXiv v2](https://arxiv.org/html/2503.14000v2), §§2–4.

| Published setting | Paper | Pilot hiện tại |
|---|---|---|
| Evaluation units | 183 modules | 1 function, 2 scenarios |
| Default generator / rounds | GPT-4o / 3 | Qwen 1.5B / CLI, thường 1 |
| Line / branch coverage | 83.0% / 70.8% | NA |
| CoverUp reference LC / BC | 77.4% / 65.3% | Không chạy CoverUp |
| Mutation Test4Py / NoGraph | 0.843 / 0.787 | 2 mutant minh họa; kết quả generated tests: NA |

`get_custom_loader` đã là ví dụ động cơ của bài gốc; constructor/type context cũng đã có. Vì vậy, gọi đây là ví dụ chưa từng được nghiên cứu hoặc tuyên bố mới ở việc thêm thông tin constructor là không đúng.

Từ số trung bình công bố, tôi tính: chênh lệch LC với CoverUp là **5.6 điểm phần trăm**, tương đối khoảng **7.24%**; BC là **5.5 điểm phần trăm**, tương đối khoảng **8.42%**. Không nhầm phần trăm tương đối với điểm phần trăm. Không đặt số của pilot lên cùng biểu đồ như một phép tái lập trực tiếp: khác model, số vòng, đơn vị đánh giá và mutant pool.

## Đóng góp nên phát biểu thế nào

Đề xuất tên làm việc: **Execution-Verified Setup Context for Stateful Python Test Generation**. Tên này chỉ mô tả hướng nghiên cứu, chưa khẳng định hiệu quả.

Mô hình hóa đối tượng sau constructor là trạng thái `s0`; `π = [a1,…,ak]` là chuỗi lời gọi API sản phẩm; `S` là tình huống đầu vào. Bộ kiểm chứng `V(s0,π,f,S)` kiểm tra tiền điều kiện đã khai báo và việc gọi đúng entry point không phát sinh lỗi. Prompt nhận code của `π`, không nhận output quan sát, assertion oracle hay test có sẵn.

Trong code hiện tại, `V` chỉ chứng minh một witness thực thi trong fixture đã chọn. Nó không chứng minh mọi đầu vào hợp lệ, tính tối thiểu toàn cục hay tính đúng ngữ nghĩa của assertion. Chỉ dùng từ “verified” trong phạm vi đó.

Ba đóng góp có thể phát triển thành luận điểm độc lập:

1. **Cơ chế**: trích hành động và ràng buộc trạng thái từ mã sản phẩm, sinh ứng viên và xác thực trước generation.
2. **Bằng chứng nhân quả**: giữ model/pipeline cố định, đối chứng extraction/caller, chỉ ra lỗi nào giảm vì trạng thái đối tượng được chuẩn bị đúng.
3. **Ứng dụng**: giảm công sửa fixture và tạo regression tests phát hiện lỗi thực với ngân sách máy cục bộ chấp nhận được.

## Audit code: các điểm reviewer sẽ hỏi

| Điểm | Bằng chứng trong source | Hệ quả / việc cần làm |
|---|---|---|
| Chuỗi setup chưa tổng quát | `pilot/setup.py`: allowlist 2 method; render đối số literal riêng cho PyCG | Gọi đúng là adapter miền. Cần suy ra action/argument/dependency từ source nếu muốn đóng góp thuật toán tổng quát. |
| Extracted còn yếu | Candidate đầu là constructor-only, cả hai tình huống | Đo verified–extracted hiện có nhưng không lấy đó làm toàn bộ bằng chứng. Cần thêm structural ranking mạnh, không probe. |
| Caller có thể dài/lặp | Snippet được định danh bằng file + từng dòng call | Cùng function có thể lặp khi chứa nhiều call. Audit token và dedup theo function/span trước benchmark xác nhận, không sửa ngầm lượt đang chạy. |
| Ví dụ nghiên cứu bị chọn thuận lợi | Một target đã biết cần source node | Đây là case study có chủ đích, không đại diện tập Python stateful. Phải có held-out targets và negative controls khi mở rộng. |
| Kiểm chứng có quy tắc thủ công | `pilot/probe.py`: current module, source node, destination old path | Công khai toàn bộ quy tắc; tách phần suy ra tự động khỏi kiến thức của người viết adapter. |
| Pass cuối bị chọn lọc | Upstream repair/decline giữ test pass và có thể cắt assertion | Không dùng tỷ lệ pass của suite cuối làm first-pass rate. Audit assertion còn lại và fault detection. |
| Taxonomy lỗi chỉ heuristic | `classify()` dựa tên exception | AttributeError/TypeError có thể do kiểu, state hoặc lỗi code. Không gọi số event đó là setup-failure rate có ground truth. |
| Mutation pool rất nhỏ | Hai AST operator cố định trong loader | Chỉ có 0, 0.5, 1.0; không chứng minh năng lực phát hiện lỗi rộng. Giữ pool chung, bổ sung pool đa dạng và lỗi thực sau pilot. |
| Scope coverage dễ nhầm | Report có module và nested-function coverage | Báo factory/returned-loader và target+nested riêng, không lấy module coverage thay target. |
| GPU/timing có nhiễu | `--jobs 2`, CPU/IO/cache dùng chung | Throughput hệ thống tách khỏi thời gian thuật toán. Đo đối chứng timing jobs=1 nếu muốn claim speedup. |
| Greedy không tạo mẫu ngẫu nhiên mới | `do_sample=False`, seed mặc định 42 | Chạy lại cùng target chủ yếu đo môi trường. Không coi 30 lượt giống nhau là 30 function độc lập. |
| Lọc test cần audit | Bộ lọc hiện theo đường dẫn/tên phổ biến | Lưu danh mục file thực sự truy xuất, kiểm tra naming lạ và nguồn test trước khi khẳng định không có retrieval leakage. Không thể suy ra không có pretraining contamination. |

Không thay các quyết định phương pháp giữa chừng sau khi nhìn kết quả. Mọi thay đổi ranking, prompt, budget hoặc mutant pool phải là phiên bản protocol mới.

## Đối chứng và câu hỏi nghiên cứu

| Contrast | Câu hỏi trả lời | Giới hạn |
|---|---|---|
| verified − extracted | Giá trị của lựa chọn có chạy kiểm chứng từ cùng candidate pool/order | Top constructor-only là control yếu; độ dài ngữ cảnh khác. |
| verified − caller | Setup đã chuẩn hóa/kiểm chứng hơn việc đưa mã caller thô ở đâu? | Context length/ranking là các cơ chế khác nhau, cần báo token. |
| verified − baseline | Lợi ích end-to-end của toàn bộ extension | Không tách riêng extraction và verification. |
| caller − baseline | Chỉ bổ sung caller đã đủ chưa? | Caller đã có tín hiệu ngầm ở upstream summarization. |
| extracted − baseline | Chỉ thêm witness chưa kiểm chứng giúp gì? | Cần ghi cả trường hợp gây hại. |
| extracted = verified | Khi hai mode chọn cùng code thì có khác chất lượng không? | Không loại khỏi kết quả; đây là trường hợp verification có thể chỉ thêm chi phí. |

RQ1: Trong các test đã dùng đúng class, setup có kiểm chứng có giảm lỗi trạng thái trước repair không?

RQ2: Có tăng coverage đúng scope và phát hiện lỗi, hay chỉ làm test pass bằng assertion yếu?

RQ3: Chi phí phân tích/probe có bù lại chi phí repair và số token giảm được không?

RQ4: Hiệu quả thay đổi theo độ dài setup, phụ thuộc tham số, constructor phức tạp và model size thế nào?

RQ5: Kết quả có chuyển sang target/project chưa dùng để thiết kế adapter và quy trình CI thực tế không?

## Thông số phải khóa và ghi lại

Ghim source tool, Test4Py, target repo; model/tokenizer/embedding revision; Python, package lock và Kaggle image; GPU model, CUDA/Torch, precision; do_sample/temperature/seed; token cap mỗi call, context cap nếu có; số vòng; repair/decline policy; source scope/retrieval index; candidate grammar/order, search budget/timeout; scenario text; scoring command, mutant source/hash và timeout; jobs, CPU thread, cache cold/warm; thứ tự/GPU assignment; inclusion/exclusion và stopping rule.

Các biến đã được source ghi lại phần lớn nằm trong `experiment.json`, `environment.json`, report/log. Kaggle image version, type-state labels, lần đầu test pass, target reach từng test, assertion preservation và human effort **chưa được đo đầy đủ**. Xem `METRICS.csv`; ô thiếu không tự điền bằng 0.

## Bộ chỉ số và cách trình bày

Chỉ số cơ chế ưu tiên: đúng class nhưng thiếu state; tỷ lệ setup hợp lệ theo tình huống; rank của ứng viên được chọn; probes/budget; kết quả hai mode chọn cùng setup; reach returned loader. Chỉ số chất lượng: first-pass trước repair, pass cuối, branch/line coverage target+nested, mutation/real-bug detection, flaky replay và assertion còn lại. Chỉ số chi phí: token input/output, số call theo phase, thời gian từng stage, wall time, peak VRAM và telemetry GPU. Không quy token self-hosted thành USD hoặc utilization thành năng lượng nếu không có phép đo thích hợp.

Bảng T1 mô tả target + tiêu chí chọn; T2 cấu hình/pinning; T3 đối chứng bốn mode với tất cả lượt lỗi; T4 paired differences và mẫu số; T5 hiệu quả/cost; T6 từng mutant và lý do inconclusive; T7 threats/negative cases. Các biểu đồ nên gồm paired dots, cost–quality scatter và stage-time decomposition không đếm chồng `setup_total` với AST/probe. GPU traces là đồ thị vận hành, không phải bằng chứng chất lượng test.

`analyze.py` xuất CSV và đồ thị SVG/PDF/PNG từ artifact thật. Không plot số paper cùng pilot thành “before/after”. Không nối đường qua điểm dữ liệu thiếu; không tự đặt số 0 cho failed environment, confidence interval giả hoặc mean gộp nhiều cohort không tương thích.

## Suy luận thống kê

Pilot hiện tại dùng báo cáo mô tả và hiệu số ghép cặp. Không tính p-value hoặc CI suy rộng từ một function; hai scenario và hai mutant cũng không phải bốn project độc lập. Lượt chạy/hàm/test/mutant không được đánh tráo thành cùng đơn vị mẫu.

Giai đoạn xác nhận tương lai: khóa primary contrast/outcome trước; lấy mẫu functions theo strata stateful và negative controls từ nhiều project; giữ cùng target/seed/model/budget trong block; luân phiên GPU/thứ tự để giảm nhiễu. Dùng paired effect (điểm phần trăm hoặc risk difference), CI theo cluster project và báo toàn phân phối. Power/sample size dựa trên độ biến thiên, tương quan nội project và mức cải thiện có ý nghĩa thực tế, không theo quy tắc “30 seeds”. Có thể dùng paired randomization hoặc bootstrap cluster khi giả định/số cluster phù hợp; nêu điều kiện áp dụng, không dùng test thống kê để cứu thiết kế một target.

Primary outcome và ngưỡng lợi ích thực tế phải do protocol xác định trước; không đặt sau khi thấy verified thắng. Secondary contrasts cần điều chỉnh multiplicity, chẳng hạn Holm. Báo effect size + độ bất định, không chỉ dấu sao p-value. Thiếu dữ liệu có tính thông tin phải báo theo lý do, kèm sensitivity analysis; không chỉ giữ các run đẹp. Cases no-generated-tests là outcome chất lượng riêng; infrastructure error là loại lỗi khác.

Một CI hẹp quanh trung bình nhiều lần chạy cùng greedy target chỉ nói về lặp lại môi trường đó, không chứng minh generalization. Một benchmark mới cần cỡ mẫu độc lập thật; việc mở rộng này chưa được chạy trong source pilot.

## Điều kiện để bảo vệ đóng góp mạnh

- Vượt một control extraction/ranking có năng lực, không chỉ constructor-only.
- Lợi ích còn khi giữ cùng model và cân bằng budget; báo riêng same-selected và negative cases.
- Witness được suy ra qua nhiều API/state patterns, có held-out project, không thêm rule sau khi nhìn test set.
- Giảm lỗi state đã được audit nguyên nhân; tăng fault detection chứ không chỉ coverage/pass.
- Cải thiện đủ lớn và ổn định so với chi phí; kết quả có độ bất định phù hợp, không xuất phát từ một trường hợp thuận lợi.
- Artifact, dữ liệu nguồn, scoring và protocol đủ để người khác tái lập.

Đây là tiêu chí nghiên cứu đề xuất, không phải cam kết “đóng góp cao” hoặc bảo đảm chấp nhận ở venue nào.

## Ứng dụng thực tế cần thử

| Miền ứng dụng đề xuất | Ví dụ state cần chuẩn bị | Kết quả thực tế phải đo |
|---|---|---|
| SDK/client nội bộ | configure → authenticate → invoke | lỗi setup giảm; phút sửa fixture; không phụ thuộc dịch vụ live trong CI |
| Đồ thị/analysis tooling | add source node → add edge | regression phát hiện sai quan hệ/path; thời gian review test |
| Database layer | mở connection/transaction → thao tác | resource cleanup, isolation và flaky replay |
| ML estimator/pipeline | fit → transform/predict | trạng thái fitted, oracle phù hợp và tránh fixture “pass nhưng vô nghĩa” |

Đây là hướng đánh giá tương lai, không phải các miền đã được benchmark. Case study CI có thể đưa test/fixture gợi ý vào review của lập trình viên; ghi acceptance, sửa tay, thời gian đến test hợp lệ, flaky failures và bug được xác nhận. Muốn claim giảm human effort cần đo thực sự, không lấy số token làm proxy duy nhất.

## Vị trí so với công trình liên quan

[ChatUniTest](https://arxiv.org/abs/2305.04764) đã có adaptive context và generation–validation–repair. [CoverUp](https://arxiv.org/abs/2403.16218) dùng coverage-guided generation; [Pynguin](https://arxiv.org/abs/2202.05218) là nền tảng test generation Python. Vì vậy “có thực thi để kiểm tra test” không đủ mới. Điểm phân biệt cần kiểm chứng là **kiểm chứng input-state witness trước generation**, còn pipeline type inference/repair giữ nguyên.

Một [preprint năm 2026 về model mới](https://arxiv.org/abs/2601.09695) cũng đặt vấn đề framework có thể mất lợi thế khi dùng baseline LLM mạnh hơn. Đây là lý do cần kiểm soát model và đối chứng tốt, không phải bằng chứng trực tiếp cho pilot này. Phần related work ở đây là khảo sát định hướng, chưa phải systematic literature review hoặc chứng minh “đầu tiên”.

Thiết kế báo cáo tham khảo [ACM SIGSOFT Empirical Standards](https://www2.sigsoft.org/EmpiricalStandards/docs/standards): câu hỏi rõ, phép đo phù hợp, công khai giả định/giới hạn và kết luận dựa vào evidence. Phần phương pháp thống kê ở trên là đề xuất áp dụng cho dự án, không phải chứng nhận tuân thủ từ ACM.
