# CHUYÊN KHẢO NGHIÊN CỨU KHOA HỌC: SINH VÀ SỬA LỖI BỘ KIỂM THỬ ĐƠN VỊ TỰ ĐỘNG BẰNG KIẾN TRÚC HỘI ĐỒNG TỐI ƯU SOTA (COUNCIL-SOTA) TRÊN HỆ QUY CHIẾU TEST4PY BENCHMARK

*Closed-Loop Multi-Turn Adaptive Critic Repair with Abstract Syntax Tree Symbol-Table Grounding and Mutation-Hardened Verification for Modern Python Ecosystems*

---

## PHẦN ĐẦU (FRONT MATTER)

### TÓM TẮT NGHIÊN CỨU (ABSTRACT)

Tự động hóa quá trình sinh bộ kiểm thử đơn vị (Automated Unit Test Generation) thông qua các Mô hình Ngôn ngữ Lớn (LLMs) và Mô hình Ngôn ngữ Tinh gọn (SLMs) đang mở ra bước ngoặt mang tính cách mạng trong kỹ nghệ phần mềm và xác minh chương trình. Tuy nhiên, khi triển khai trên các hệ sinh thái mã nguồn Python thực tế thuộc hệ quy chiếu chuẩn mực **Test4Py Benchmark**, các mô hình kích thước nhỏ và vừa (~14B–20B tham số) đối mặt với ba "tử huyệt" kỹ thuật mang tính hệ thống: (1) **Ảo giác đường dẫn nhập khẩu (Submodule Import Hallucinations)** do suy đoán sai cấu trúc gói nội bộ; (2) **Thổi phồng thuộc tính ngoại lệ và suy biến tiên tri kiểm thử (Oracle Degradation / Hollow Assertions)** với các khẳng định rỗng (`assert True`) hoặc truy cập thuộc tính không tồn tại trong mô hình dữ liệu động; và (3) **Cái bẫy ngắt mạch sửa lỗi đơn vòng (Single-Turn Truncation Trap)**, trong đó bộ phản biện truyền thống chỉ giải quyết được lỗi cú pháp ban đầu nhưng làm nảy sinh các sai khác assertion vi mô ở chu kỳ kế tiếp mà không có cơ chế hồi tiếp thích ứng để khắc phục.

Công trình này đề xuất và hiện thực hóa **Council-SOTA**—một kiến trúc hội đồng đa tác nhân khép kín (Closed-Loop Multi-Agent Architecture) kết hợp giữa biểu diễn hình thức của cây cú pháp trừu tượng và cơ chế lập luận hồi tiếp đa vòng. Council-SOTA tích hợp ba giải pháp kỹ thuật cốt lõi: (1) **Neo Định Danh Cú Pháp AST Tĩnh (AST Symbol-Table Export Grounding)** cho phép trích xuất bảng định danh xuất khẩu và ghim cứng ràng buộc chữ ký với chi phí tính toán $\approx 0$ token và thời gian xử lý $< 50\text{ ms}$; (2) **Quy trình Sửa lỗi Thích ứng Hai vòng (Two-Round Multi-Turn Adaptive Critic Repair)** tiếp nhận đầy đủ phản hồi lỗi thực thi (Traceback) và vi sai assertion từ `pytest` để tự động hiệu chỉnh mã nguồn kiểm thử; và (3) **Cỗ máy Thẩm định Ngữ nghĩa bằng Đột biến Cấp 1 (First-Order AST Mutation Testing Engine)** nhằm định lượng chính xác năng lực phát hiện lỗi logic thực tế, loại trừ hoàn toàn các bộ test đạt độ phủ hình thức nhưng vô giá trị về mặt ngữ nghĩa.

Nghiên cứu tiến hành đánh giá thực nghiệm toàn diện trên **21 Curated Benchmark Targets** đại diện cho 7 thư viện nguồn mở phức tạp thuộc Test4Py thông qua $N=5$ hạt giống ngẫu nhiên độc lập (tổng cộng 315 lượt thực nghiệm so sánh đối đầu). Kết quả thực nghiệm khẳng định Council-SOTA vượt trội áp đảo các phương pháp tiền nhiệm: tỷ lệ vượt qua bộ test (Pass Rate) đạt **91,43%** (tăng lên **93,33%** sau tinh chỉnh quy tắc ngữ nghĩa), cao gần gấp đôi so với Zero-Shot Baseline (**48,57%**) và vượt xa Standard Council (**69,52%**). Độ phủ dòng mã đạt **46,50%** (tăng ròng $+22,37\%$ tuyệt đối so với Baseline, $p = 7,35 \times 10^{-4}$, hệ số kích thước tác động Cohen's $d = 0,8687$; kiểm định Wilcoxon $W = 6,0, p = 1,34 \times 10^{-5}$). Vòng phản biện thứ hai cứu vãn thành công 5 ca lỗi assertion hiểm hóc, đưa các module thất bại triệt để lên tỷ lệ hoàn hảo 100%. Đánh giá trên 187 đột biến nhân tạo ghi nhận điểm đột biến trung bình đạt **37,97%** (đạt tới **43,10%** trên các module thuật toán cốt lõi và tối đa 100% trên các bộ điều khiển luồng phức tạp). Toàn bộ chiến dịch thực thi chỉ tiêu tốn trung bình **$0,0013\text{ USD/suite}** với độ trễ suy luận dao động từ 5,8 đến 6,6 giây, chứng minh tính khả thi kinh tế vượt trội và độ sẵn sàng tích hợp hoàn hảo vào các đường ống tích hợp liên tục (CI/CD) hiện đại.

---

### EXTENDED ABSTRACT

Automated unit test synthesis using Large Language Models (LLMs) and Small Language Models (SLMs) represents a transformative frontier in software engineering and automated program repair. However, state-of-the-art generative language models operating in zero-shot or classical prompt-response paradigms encounter fundamental algorithmic barriers when deployed on production Python repositories exhibiting duck typing, dynamic late-binding, and stateful receiver graph architectures, such as those cataloged in the rigorous **Test4Py Benchmark** ecosystem. Specifically, empirical investigations reveal three systemic failure modes: (1) **Submodule Import Path Hallucination**, wherein generative agents infer intuitive but non-existent modular hierarchy (e.g., attempting `from typesystem.exceptions import ValidationError` instead of binding to `typesystem.base`); (2) **Exception Attribute Speculation and Hollow Test Synthesis**, characterized by models asserting non-existent internal attributes or generating vacuous tautological invariants (`assert True`); and (3) **The Single-Turn Repair Truncation Trap**, in which monolithic generator-critic architectures exhaust their repair budget on initial syntactic or import adjustments, only to fail on subtle secondary runtime assertion discrepancies without subsequent recovery avenues.

To surmount these intrinsic bottlenecks, this monograph presents **Council-SOTA**, an open-source, closed-loop multi-agent verification framework engineered specifically for dynamic languages. Council-SOTA synergizes three primary theoretical and engineering contributions:
1. **Deterministic AST Symbol-Table Export Grounding**: A static, pre-generation AST analyzer that extracts canonical exported symbols, explicit module bindings, and decorator calling protocols directly from package namespaces. This mechanism completely bypasses the computationally prohibitive cold-start latency ($> 40\text{ minutes}$) and VRAM out-of-memory risks inherent to multi-hop Call-Graph RAG pipelines, operating deterministically within $< 50\text{ ms}$ on CPU with zero token overhead.
2. **Two-Round Multi-Turn Adaptive Critic Repair Loop**: A specialized feedback control loop that dynamically ingests standard `pytest` failure diagnostic tracebacks, standard error streams, and assertion difference matrices. While Round 1 effectively resolves syntax, import, and argument-binding exceptions (accounting for 24 empirical recoveries), Round 2 specifically isolates and repairs semantic assertion regressions (achieving 5 crucial recoveries in previously deadlocked targets), safeguarded by an automated AST gatekeeper preventing assertion pruning.
3. **First-Order Semantic Mutation Testing Engine**: A rigorous downstream validation apparatus synthesizing 187 first-order syntactic mutants across four distinct operator classes (Relational Operator Replacement, Arithmetic Operator Replacement, Boolean Value Replacement, and Statement Inversion/Return Modification) to quantitatively adjudicate test oracle adequacy and discriminate between authentic bug-detecting suites and hollow coverage artifacts.

We conducted an extensive, stratified empirical evaluation across **21 Curated Benchmark Targets** selected from 7 core Test4Py repositories (`typesystem`, `docstring_parser`, `PyCG`, `genty`, `python-string-utils`, `codetiming`, and `superstring.py`). Under a rigorous $N=5$ multi-seed statistical design ($S \in \{42, 43, 44, 45, 46\}$, encompassing 315 comparative trials) powered by `openai/gpt-oss-20b` over Groq hardware, Council-SOTA achieves a **91.43% test suite pass rate** (advancing to **93.33%** following semantic attribute refinement), nearly doubling the Zero-Shot Baseline (**48.57%**) and substantially eclipsing the Standard Single-Turn Council (**69.52%**). Council-SOTA attains a mean statement line coverage of **46.50%** (an absolute gain of $+22.37\%$ over baseline; paired $t = 3.9810, p = 7.35 \times 10^{-4}$; Wilcoxon signed-rank $W = 6.0, p = 1.34 \times 10^{-5}$; Cohen's $d = 0.8687$; Vargha-Delaney $\hat{A}_{12} = 0.7985$). Across 187 AST mutants, the generated test suites achieve an aggregate mutant kill rate of **37.97%** (reaching **43.10%** on core algorithmic suites and up to 100% on complex control-flow targets). Stress testing across 105 consecutive executions demonstrates a **0.00% flaky test rate**. With an average execution latency of 6.2 seconds and an ultra-low operational inference cost of **$0.0013 USD per verified test suite**, Council-SOTA establishes a new Pareto-optimal frontier for industrial CI/CD integration.

---

### DANH MỤC TỪ VIẾT TẮT (LIST OF ABBREVIATIONS)

| Ký hiệu | Thuật ngữ Tiếng Anh | Nghĩa Tiếng Việt |
| :--- | :--- | :--- |
| **AST** | Abstract Syntax Tree | Cây cú pháp trừu tượng |
| **RAG** | Retrieval-Augmented Generation | Kỹ thuật sinh tăng cường bằng truy xuất |
| **NF4** | NormalFloat 4-bit Quantization | Định dạng lượng tử hóa số học 4-bit chuẩn hóa |
| **SLM** | Small Language Model | Mô hình ngôn ngữ kích thước tinh gọn (nhỏ và vừa) |
| **LLM** | Large Language Model | Mô hình ngôn ngữ lớn |
| **CoT** | Chain-of-Thought Prompting | Kỹ thuật thúc đẩy mô hình tư duy theo chuỗi lập luận |
| **SC** | Statement / Line Coverage | Độ phủ câu lệnh (độ phủ dòng mã thực thi) |
| **BC** | Branch Coverage | Độ phủ nhánh rẽ logic |
| **MS** | Mutation Score | Điểm đột biến (tỷ lệ đột biến bị tiêu diệt) |
| **MUT** | Method / Module Under Test | Phương thức hoặc module đang được kiểm thử |
| **ROR** | Relational Operator Replacement | Toán tử đột biến thay thế phép toán quan hệ |
| **AOR** | Arithmetic Operator Replacement | Toán tử đột biến thay thế phép toán số học |
| **BVR** | Boolean Value Replacement | Toán tử đột biến thay thế giá trị luận lý Boolean |
| **CRP** | Constant Replacement Operator | Toán tử đột biến thay thế giá trị hằng số |
| **SIR** | Statement Inversion and Return Mutation | Toán tử đột biến đảo ngược lệnh và sửa giá trị trả về |
| **CB** | Circuit Breaker (Financial Engine) | Cơ chế ngắt mạch bảo vệ an toàn tài chính |
| **CI/CD**| Continuous Integration / Continuous Deployment | Quy trình Tích hợp liên tục và Triển khai liên tục |
| **SBST**| Search-Based Software Testing | Kiểm thử phần mềm dựa trên kỹ thuật tìm kiếm |
| **API** | Application Programming Interface | Giao diện lập trình ứng dụng |
| **SOTA**| State-Of-The-Art | Đỉnh cao công nghệ / Trạng thái phát triển tối tân |

---

# CHƯƠNG MỞ ĐẦU (INTRODUCTION)

### 1.1 Bối cảnh & Lý do chọn đề tài

Trong vòng đời phát triển phần mềm (Software Development Life Cycle - SDLC), bảo đảm chất lượng và ngăn ngừa lỗi hồi quy (regression defects) là yêu cầu sống còn. Kiểm thử đơn vị (Unit Testing) đóng vai trò là tuyến phòng thủ cơ sở quan trọng nhất, cho phép cô lập và xác thực tính đúng đắn ngữ nghĩa của từng đơn vị chức năng độc lập. Mặc dù sở hữu tầm quan trọng không thể tranh cãi, việc thiết kế thủ công các bộ kiểm thử chất lượng cao là một hoạt động tiêu tốn nguồn lực nghiêm trọng, thường chiếm từ 40% đến 60% tổng chi phí nhân sự và thời gian phát triển của dự án [1], [2].

Đối với hệ sinh thái ngôn ngữ **Python**—ngôn ngữ đóng vai trò trụ cột trong kỷ nguyên trí tuệ nhân tạo, tính toán khoa học, phân tích dữ liệu lớn và kiến trúc vi dịch vụ đám mây—bài toán kiểm thử tự động vấp phải những rào cản nội tại bắt nguồn từ các đặc tính ngữ nghĩa động:
1. **Định kiểu vịt (Duck Typing) và Liên kết muộn (Dynamic Late-Binding)**: Ngôn ngữ Python không có bước kiểm tra kiểu tĩnh (Static Type Checking) bắt buộc tại thời điểm biên dịch. Các xung đột kiểu, việc truyền tham số sai lệch, hoặc hành vi truy cập vào các phương thức/thuộc tính không tồn tại đều không bị cảnh báo sớm mà chỉ phát tác dưới dạng ngoại lệ nghiêm trọng (`TypeError`, `AttributeError`) khi mã nguồn được nạp hoặc thực thi trong không gian bộ nhớ thời gian chạy (runtime).
2. **Khởi tạo đối tượng nhận có trạng thái phức tạp (Stateful Receiver Graph Construction)**: Các module thư viện thực tế hiếm khi tồn tại dưới dạng các hàm thuần túy độc lập (Pure Functions). Thay vào đó, chúng phụ thuộc chặt chẽ vào đồ thị đối tượng có trạng thái (Receiver Objects), đòi hỏi các chuỗi thiết lập đa bước (Multi-step Setup Sequences) chính xác để thỏa mãn các bất biến trạng thái (State Invariants) trước khi phương thức mục tiêu (Method Under Test - MUT) có thể được kích hoạt hợp lệ.
3. **Sự trỗi dậy của LLMs và Nghịch lý Mô hình Tinh gọn (SLMs)**: Sự bùng nổ của các mô hình ngôn ngữ lớn (LLMs) như GPT-4 hay Claude-3.5 đã chứng minh năng lực vượt bậc trong việc đọc hiểu mã nguồn và sinh các kịch bản kiểm thử mang tính ngữ nghĩa phong phú. Tuy nhiên, việc vận hành các mô hình thương mại khổng lồ này đòi hỏi chi phí tài chính đắt đỏ, phụ thuộc vào hạ tầng đóng của bên thứ ba, và đối mặt với độ trễ suy luận lớn, khiến chúng trở nên phi thực tế khi triển khai trong các đường ống tích hợp liên tục (CI/CD) quy mô công nghiệp. Điều này dẫn đến sự dịch chuyển tất yếu hướng tới việc làm chủ các **Mô hình Ngôn ngữ Tinh gọn (SLMs)** trong dải kích thước từ 7B đến 20B tham số (như `Qwen2.5-Coder-14B` hoặc `openai/gpt-oss-20b`).

Tuy nhiên, khi trực tiếp áp dụng kỹ thuật thúc đẩy trực tiếp (Zero-Shot Prompting) trên các SLMs đối với các thư viện Python nguồn mở phức tạp (tiêu biểu như các mục tiêu trong hệ quy chiếu **Test4Py Benchmark** [1]), nghiên cứu ghi nhận một loạt điểm yếu chí tử mang tính quy luật:
- **Ảo giác đường dẫn nhập khẩu (Submodule Import Hallucinations)**: SLMs thường suy đoán cấu trúc gói dựa trên ngữ nghĩa tự nhiên của tên lớp thay vì sơ đồ xuất khẩu thực tế. Điển hình, khi sinh test cho lớp `ValidationError` thuộc gói `typesystem`, mô hình liên tục phát sinh lệnh `from typesystem.exceptions import ValidationError`, trong khi trên thực tế module `typesystem.exceptions` hoàn toàn không tồn tại (symbol này được xuất khẩu từ `typesystem.base`). Lỗi này khiến bài kiểm thử sụp đổ ngay tại pha thu thập (Pytest Collection Failure).
- **Thổi phồng thuộc tính ngoại lệ và bài kiểm thử rỗng (Oracle Problem & Hollow Tests)**: Khi kiểm tra các ngoại lệ nghiệp vụ, mô hình tự suy đoán các thuộc tính kiểm tra nội bộ (chẳng hạn gán ghép thuộc tính giả định `excinfo.value.code` cho `ValidationError` thay vì gọi hàm API chuẩn `messages()`). Nghiêm trọng hơn, để thỏa mãn chỉ số độ phủ dòng (Line Coverage), mô hình có xu hướng sinh ra các bộ kiểm thử "rỗng" (Hollow Tests)—kích hoạt dòng lệnh nhưng chỉ sử dụng các assertion tầm thường (`assert True` hoặc `assert result is not None`), tạo ra sự ảo tưởng về chất lượng kiểm thử trong khi năng lực phát hiện lỗi logic bằng không [3].
- **Cái bẫy ngắt mạch sửa lỗi đơn vòng (Single-Turn Truncation Trap)**: Các kiến trúc Coder-Critic truyền thống chỉ cấp phép tối đa một chu kỳ sửa lỗi. Trong thực tế, khi nhận traceback lỗi import, Critic vòng 1 sửa thành công đường dẫn nhưng mã mới thường phát sinh một sai khác assertion nhỏ ở pha chạy. Do cạn kiệt ngân sách vòng lặp, toàn bộ bài test bị hủy bỏ, dẫn đến lãng phí tài nguyên suy luận.
- **Nghẽn cổ chai tính toán của Call-Graph RAG**: Các nỗ lực giải quyết vấn đề ngữ cảnh bằng cách xây dựng đồ thị gọi hàm (Call-Graph) đa tầng và dùng LLM tóm tắt docstrings (như khảo sát trong giai đoạn nghiên cứu R8–R15 trên hạ tầng Kaggle 2x Tesla T4) đã gây ra hiện tượng nghẽn cổ chai nghiêm trọng: thời gian chuẩn bị context tiêu tốn tới **43,8 phút (2.627 giây)** qua 95 lệnh gọi LLM chỉ để chuẩn bị dữ liệu cho 2 module, đồng thời liên tục kích hoạt tràn bộ nhớ VRAM (CUDA OOM).

Từ bối cảnh thực tiễn trên, việc phát triển một kiến trúc hội đồng tinh gọn, có khả năng neo định danh cú pháp xác định (Deterministic AST Grounding), kết hợp cơ chế phản biện hồi tiếp thích ứng đa vòng và thẩm định nghiêm ngặt bằng kiểm thử đột biến là đòi hỏi cấp bách cả về mặt khoa học lẫn ứng dụng công nghiệp.

---

### 1.2 Bốn Câu hỏi Nghiên cứu Cụ thể (Research Questions)

Nhằm thiết lập một hệ thống kiểm chứng khoa học chặt chẽ, luận án xác định và tập trung giải quyết 4 câu hỏi nghiên cứu cốt lõi:

* **RQ1 (Tác động của Neo Định Danh Cú Pháp AST - AST Symbol Grounding)**:  
  *Việc tích hợp cơ chế Neo Định Danh Cú Pháp AST tĩnh (AST Symbol-Table Export Grounding) vào giai đoạn tiền tạo sinh prompt có loại bỏ được hiện tượng ảo giác đường dẫn nhập khẩu (Import Hallucinations) và cải thiện có ý nghĩa thống kê tỷ lệ vượt qua bộ test (Pass Rate) cũng như độ phủ dòng mã (Statement Coverage) so với phương thức Zero-Shot Baseline và Council Cổ điển hay không?*  
  Mục tiêu toán học là kiểm định giả thuyết vô hiệu:
  $$\mathcal{H}_0^{(1)}: \mu_{\text{Cov}}(\text{Council-SOTA}) \le \mu_{\text{Cov}}(\text{Baseline})$$
  đối nghịch với giả thuyết:
  $$\mathcal{H}_1^{(1)}: \mu_{\text{Cov}}(\text{Council-SOTA}) > \mu_{\text{Cov}}(\text{Baseline})$$
  với mức ý nghĩa thống kê $\alpha = 0,05$.

* **RQ2 (Hiệu quả Hồi tiếp Đa vòng của Two-Round Adaptive Critic)**:  
  *Cơ chế phản biện hồi tiếp thích ứng hai vòng (Two-Round Multi-Turn Adaptive Critic Repair Loop) tiếp nhận thông tin vi sai assertion và traceback từ `pytest` đóng góp định lượng như thế nào vào khả năng cứu vãn các bộ kiểm thử bị suy biến ở vòng 1, và tỷ lệ phục hồi thành công ($\Delta P_{R2}$) đạt được là bao nhiêu trên các mục tiêu có cấu trúc ngoại lệ phức tạp?*

* **RQ3 (Mối quan hệ giữa Code Coverage và Mutation Score / Test Oracle Quality)**:  
  *Có hay không mối tương quan tuyến tính chặt chẽ giữa độ phủ mã nguồn cấu trúc (Line/Branch Coverage) và điểm số kiểm thử đột biến (Mutation Score)? Cơ chế tiền lọc và cổng kiểm soát chất lượng cú pháp (Quality Gatekeeper) loại trừ hiện tượng khẳng định rỗng (Hollow Assertions) và bảo toàn tính toàn vẹn ngữ nghĩa của Test Oracle như thế nào?*

* **RQ4 (Tính khả thi Kinh tế và Độ trễ Pareto trong CI/CD)**:  
  *Kiến trúc Council-SOTA có thỏa mãn đường biên Pareto tối ưu giữa chi phí token suy luận ($C_{\text{token}}$), độ trễ thực thi ($T_{\text{latency}}$) và độ ổn định chống kiểm thử chập chờn (Flakiness Rate $\approx 0\%$) để có thể ứng dụng thực tế trong các đường ống CI/CD doanh nghiệp dưới trần ngân sách khắt khe hay không?*

---

### 1.3 Đối tượng và Phạm vi Nghiên cứu

Nghiên cứu tập trung vào bài toán tự động sinh và sửa chữa các bộ kiểm thử đơn vị cấp module/hàm cho ngôn ngữ Python. Đối tượng khảo nghiệm thực nghiệm được chuẩn hóa trên **21 Curated Benchmark Targets** thuộc 7 kho mã nguồn lõi của hệ quy chiếu **Test4Py Benchmark** [1] (Bảng 0.1).

*Bảng 0.1: Danh mục 21 Curated Benchmark Targets phân tầng thuộc hệ sinh thái Test4Py.*

| STT | Target Identifier | Repository / Dự án | Module mục tiêu (MUT) | Đặc tính kỹ thuật & Thách thức ngữ nghĩa |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `superstring` | `superstring.py` | `superstring.py` | Xử lý chuỗi C-extension, logic ép kiểu chặt chẽ |
| 2 | `codetiming_timer` | `codetiming` | `codetiming._timer.Timer` | Đo lường hiệu năng thời gian thực, ngữ cảnh ContextManager |
| 3 | `docstring_parser_docstring` | `docstring_parser` | `docstring_parser.common` | Cấu trúc dữ liệu AST Docstring, phân tách chuỗi mô tả |
| 4 | `docstring_parser_parse` | `docstring_parser` | `docstring_parser.parser` | Máy phân tích cú pháp đa chuẩn docstring (ReST, Google) |
| 5 | `docstring_parser_google` | `docstring_parser` | `docstring_parser.google` | Bộ phân tích ngữ pháp đặc tả kiểu Google-style phức hợp |
| 6 | `docstring_parser_numpydoc` | `docstring_parser` | `docstring_parser.numpydoc` | Cấu trúc docstring NumPy, mô hình thuộc tính đặc thù |
| 7 | `genty_args` | `genty` | `genty.genty_args` | Đóng gói tham số kiểm thử tham số hóa (Parameterized Tests) |
| 8 | `genty_dataset` | `genty` | `genty.genty_dataset` | Decorator giải nén tập dữ liệu kiểm thử ma trận đa chiều |
| 9 | `genty_repeat` | `genty` | `genty.genty_repeat` | Vòng lặp kiểm thử lặp lại có điều kiện kiểm soát trạng thái |
| 10 | `pycg_callgraph` | `PyCG` | `pycg.machinery.callgraph` | Cấu trúc dữ liệu đồ thị gọi hàm tĩnh đa nút liên kết |
| 11 | `pycg_classes` | `PyCG` | `pycg.machinery.classes` | Bảng quản lý định danh phân cấp hướng đối tượng nội bộ |
| 12 | `pycg_imports` | `PyCG` | `pycg.machinery.imports` | Cơ chế giải quyết phụ thuộc import động trong phân tích mã |
| 13 | `pycg_scopes` | `PyCG` | `pycg.machinery.scopes` | Cây phạm vi biến (Lexical Scope) và bảng ký hiệu lồng nhau |
| 14 | `string_utils_is_email` | `python-string-utils` | `string_utils.validation` | Biểu thức chính quy (Regex) xác thực email chuẩn RFC |
| 15 | `string_utils_slugify` | `python-string-utils` | `string_utils.manipulation` | Chuẩn hóa chuỗi ký tự unicode, logic không phân nhánh |
| 16 | `typesystem_choice` | `typesystem` | `typesystem.fields` | Ràng buộc trường dữ liệu lựa chọn tập giá trị hữu hạn |
| 17 | `typesystem_oneof` | `typesystem` | `typesystem.composites` | Kiểm tra tính hợp lệ đa hình của các schema liên hợp phức tạp |
| 18 | `typesystem_schema` | `typesystem` | `typesystem.schemas` | Lớp cơ sở định nghĩa cấu trúc đối tượng và quan hệ lồng ghép |
| 19 | `typesystem_string` | `typesystem` | `typesystem.fields` | Xác thực chuỗi, kiểm tra độ dài min/max, biểu thức chính quy |
| 20 | `typesystem_validation_error` | `typesystem` | `typesystem.base` | Đối tượng ngoại lệ phân cấp quản lý cấu trúc tin nhắn lỗi |
| 21 | `woa_whale_opt` | `woa` | `woa.algorithm` | Giải thuật tối ưu hóa đàn cá voi, tính toán số học ma trận |

*Phạm vi nghiên cứu*:
- Đánh giá trên mô hình ngôn ngữ `openai/gpt-oss-20b` chạy thông qua hạ tầng Groq LPU với giao thức chuẩn hóa `test4py-curated-sota-v1`.
- Không sử dụng các phương pháp can thiệp thủ công (No Handcrafted Expected Values); mọi kịch bản đều được sinh và sửa đổi tự động 100%.

---

### 1.4 Phương pháp luận Nghiên cứu

Công trình áp dụng phương pháp luận nghiên cứu định lượng thực nghiệm (Empirical Quantitative Methodology) chuẩn mực theo các nguyên tắc của Kỹ nghệ Phần mềm Thực nghiệm (Empirical Software Engineering):
1. **Thiết kế Đối chứng Ba Trục (Three-Arm Factorial Design)**:
   - *Trục 1 (Zero-Shot Baseline)*: Sinh mã trực tiếp dựa trên mã nguồn MUT và mô tả docstring, không có tri thức bảng ký hiệu AST và không có vòng sửa lỗi.
   - *Trục 2 (Standard Council)*: Cấu trúc Coder-Critic truyền thống với 1 chu kỳ phản biện hồi tiếp duy nhất dựa trên traceback thô.
   - *Trục 3 (Council-SOTA)*: Tích hợp trọn vẹn AST Symbol Grounding, Two-Round Adaptive Critic và Preflight Normalizer.
2. **Quy trình Kiểm chứng Đa Hạt giống Ngẫu nhiên (Multi-Seed Statistical Replication)**:
   Để loại trừ yếu tố thiên lệch do tính ngẫu nhiên của mô hình tạo sinh, toàn bộ 21 targets được chạy lặp lại độc lập qua $N=5$ hạt giống ngẫu nhiên ($S \in \{42, 43, 44, 45, 46\}$), tạo thành $21 \times 3 \times 5 = 315$ lượt chạy thực nghiệm độc lập.
3. **Phân tích Thống kê Suy luận Chặt chẽ (Inferential Statistical Testing)**:
   - Kiểm định tham số cặp: Paired Student's $t$-test.
   - Kiểm định phi tham số cho phân phối không chuẩn: Wilcoxon Signed-Rank Test và Mann-Whitney $U$ Test.
   - Đo lường kích thước tác động thực tế: Chuẩn hóa Cohen's $d$ và thước đo phi tham số Vargha-Delaney $\hat{A}_{12}$.
4. **Kiểm thử Đột biến Cấp 1 (First-Order Mutation Testing Framework)**:
   Xây dựng bộ công cụ tiêm lỗi tự động trực tiếp trên cây AST của mã nguồn mục tiêu với 187 mutants thuộc 5 toán tử đột biến: Relational Operator Replacement (ROR), Arithmetic Operator Replacement (AOR), Boolean Value Replacement (BVR), Constant Replacement (CRP), và Statement Inversion / Return Mutation (SIR). Một đột biến được coi là bị tiêu diệt (Killed) khi và chỉ khi bộ kiểm thử tự sinh trả về mã lỗi thực thi (`exit_code != 0`).

---

### 1.5 Đóng góp Khoa học và Kỹ thuật Chính

Luận án mang lại ba đóng góp cốt lõi cho lĩnh vực tự động hóa kiểm thử phần mềm:
1. **Đề xuất Kiến trúc Council-SOTA Khép kín**: Thiết lập mô hình cộng tác đa tác nhân thông minh với cơ chế phản hồi hai vòng thích ứng, chứng minh trên thực nghiệm khả năng giải quyết triệt để "cái bẫy ngắt mạch đơn vòng", nâng tỷ lệ vượt qua bài test từ 48,57% lên 91,43% (và đạt 93,33% sau tinh chỉnh).
2. **Cơ chế Neo Định Danh Cú Pháp AST Tĩnh (AST Symbol-Table Export Grounding)**: Phát triển giải pháp trích xuất bảng ký hiệu xuất khẩu với chi phí tính toán 0 token, loại bỏ hoàn toàn các lỗi ảo giác cấu trúc thư viện con, giải quyết triệt để bài toán nghẽn cổ chai thời gian khởi động (giảm từ 43,8 phút xuống $< 50\text{ ms}$) và loại trừ rủi ro tràn bộ nhớ VRAM so với kỹ thuật Call-Graph RAG truyền thống.
3. **Hệ thống Đánh giá Thực nghiệm Toàn diện và Dữ liệu Mở**: Cung cấp một tập chuẩn 21 Curated Benchmark Targets trên Test4Py kèm theo 187 ca đột biến AST cấp 1, bộ kiểm chứng độ ổn định công nghiệp (Flakiness Stress Verification đạt 0,00% flake rate trên 105 lần chạy liên tiếp), và bộ 21 Golden Test Suites chuẩn mực được công khai hóa hoàn toàn phục vụ cộng đồng nghiên cứu tái lập.

---

### 1.6 Bố cục Tài liệu

Chuyên khảo được cấu trúc thành các chương chuyên sâu:
- **Chương Mở Đầu & Chương 1**: Thiết lập bối cảnh, 4 câu hỏi nghiên cứu, phân tích lịch sử SBST và các công trình SOTA dựa trên LLM, làm rõ khoảng trống tri thức.
- **Chương 2**: Cơ sở lý thuyết, phân tích hệ sinh thái Test4Py, giới hạn phần cứng Kaggle T4 và lý thuyết kiểm thử đột biến.
- **Chương 3**: Thiết kế chi tiết kiến trúc Council-SOTA, các giải thuật AST Symbol Grounding, Two-Round Adaptive Critic, và Safe Semantic Normalizer.
- **Chương 4**: Phương pháp luận thực nghiệm, thiết kế phân tầng 21 targets, quy trình tạo đột biến và các chỉ số thống kê suy luận.
- **Chương 5**: Phân tích kết quả thực nghiệm chi tiết cho RQ1–RQ4, nghiên cứu bóc tách thành phần (Ablation Study), và phân tích nhóm con.
- **Chương 6**: Phân tích định tính lỗi thực tế (Qualitative RCA), kỹ thuật tinh chỉnh grounding và báo cáo thực nghiệm chống kiểm thử chập chờn (Flakiness Stress Test).
- **Chương 7**: Phân tích kinh tế học phần mềm ($0,0013 USD/suite) và khả năng ứng dụng CI/CD.
- **Chương 8**: Thảo luận về các mối đe dọa giá trị (Threats to Validity).
- **Chương 9**: Kết luận khoa học và vạch ra 3 lộ trình nghiên cứu tương lai (Symbolic Execution, RLHF/PPO với hàm thưởng đột biến, Swarm Multi-Agent).

---

# CHƯƠNG 1: TỔNG QUAN NGHIÊN CỨU & CÔNG TRÌNH LIÊN QUAN

### 1.1 Các Hướng Sinh Test Tự Động Truyền Thống (Search-Based Software Testing - SBST)

Ý tưởng tự động hóa quy trình sinh kiểm thử đơn vị đã được cộng đồng Kỹ nghệ Phần mềm nghiên cứu sâu rộng trong hơn hai thập kỷ qua. Trường phái thống trị trong giai đoạn này là **Kiểm thử Phần mềm Dựa trên Tìm kiếm (Search-Based Software Testing - SBST)** [4], [5]. SBST mô hình hóa bài toán sinh ca kiểm thử dưới dạng một bài toán tối ưu hóa trong không gian trạng thái đầu vào, sử dụng các thuật toán tiến hóa (Evolutionary Algorithms) hoặc giải thuật di truyền (Genetic Algorithms - GA) nhằm cực đại hóa độ phủ cấu trúc chương trình (Structural Code Coverage)—chủ yếu là độ phủ câu lệnh (Statement Coverage) và độ phủ nhánh (Branch Coverage).

Công cụ tiêu biểu và thành công nhất của trường phái SBST trong thế giới Java là **EvoSuite** (Fraser & Arcuri, 2011) [4]. EvoSuite sử dụng thuật toán tìm kiếm quần thể toàn diện để sinh các chuỗi lời gọi phương thức nhằm đạt tới các nhánh rẽ khó. Tuy nhiên, khi chuyển giao các nguyên lý của SBST sang hệ sinh thái Python, công cụ tiên phong **Pynguin** (Lukasczyk & Fraser, 2022) [5] đã bộc lộ những giới hạn căn bản:
1. **Rào cản khởi tạo đồ thị đối tượng (Object Generation Plateaus)**: Do Python thiếu thông tin kiểu tĩnh, Pynguin phải dựa vào cơ chế phỏng đoán ngẫu nhiên hoặc phân tích kiểu suy diễn (Type Inference) vốn rất dễ sai lệch. Khi gặp các phương thức yêu cầu đối tượng nhận (Receiver Objects) có trạng thái lồng ghép sâu, không gian tìm kiếm bị bùng nổ tổ hợp, khiến thuật toán di truyền rơi vào trạng thái bế tắc (Plateau) và không thể tìm ra chuỗi tham số hợp lệ.
2. **Sự vắng bóng của Oracle ngữ nghĩa (The Semantic Oracle Problem)**: Bản chất của SBST là một bộ tạo sinh mù ngữ nghĩa (Semantically Blind Generator). Để tạo ra các mệnh đề khẳng định (Assertions), SBST thường thực thi mã và ghi nhận giá trị đầu ra tại thời điểm đó để làm "khẳng định hồi quy" (Regression Assertions). Nếu mã nguồn đang tồn tại lỗi tiềm ẩn, SBST sẽ bất tử hóa chính lỗi sai đó thành một khẳng định chuẩn, hoàn toàn mất khả năng phân biệt giữa hành vi mong đợi của nhà thiết kế và khiếm khuyết trong cài đặt.

---

### 1.2 Sinh Test Bằng LLM và Hệ Quy Chiếu Test4Py Benchmark

Sự xuất hiện của các Mô hình Ngôn ngữ Lớn (LLMs) được huấn luyện trên kho tàng mã nguồn mở khổng lồ đã tạo ra bước nhảy vọt về khả năng hiểu ngữ cảnh. LLMs không chỉ hiểu cú pháp mà còn nắm bắt được quy ước đặt tên, ngữ nghĩa của API và ý đồ kiểm thử ẩn sau các docstrings.

Một dấu mốc khoa học quan trọng gần đây là công trình khảo sát quy mô lớn của **Liu và cộng sự (Beihang University, 2025 - arXiv:2503.14000v2)** [1]. Nhóm nghiên cứu đã xây dựng hệ quy chiếu **Test4Py Benchmark** bao gồm hàng trăm module trích xuất từ các thư viện Python thực tế nhằm đánh giá toàn diện năng lực của LLMs so với SBST (Pynguin). Công trình của Liu et al. đã rút ra những kết luận then chốt:
- Các mô hình tạo sinh LLM vượt trội hoàn toàn Pynguin về khả năng sinh cú pháp tự nhiên và hiểu các cấu trúc dữ liệu phức tạp.
- Tuy nhiên, khi áp dụng cơ chế Zero-Shot hoặc Few-Shot thông thường, LLMs đối mặt với tỷ lệ thất bại thực thi rất cao (> 50% trong nhiều thư viện phức tạp). Các nguyên nhân hàng đầu khiến bài test không thể thực thi được bao gồm: lỗi nạp module (`ModuleNotFoundError`), lỗi sai lệch chữ ký hàm (`TypeError`), và lỗi truy cập thuộc tính ảo giác (`AttributeError`).
- Điều này chứng minh rằng: **Năng lực ngôn ngữ thuần túy của LLMs không đủ để bảo đảm tính khả thi thực thi nếu thiếu đi các cơ chế neo ngữ cảnh hình thức và vòng lặp phản hồi sửa lỗi từ môi trường runtime thực tế.**

---

### 1.3 Khoảng Trống Tri Thức (Research Gaps)

Tổng hợp các công trình nghiên cứu hiện đại chỉ ra ba khoảng trống tri thức lớn đang cản trở việc ứng dụng thực tế của LLMs/SLMs trong kiểm thử phần mềm tự động:

#### Khoảng trống 1: Bài toán Tiên tri Kiểm thử và Hiện tượng "Hollow Assertions"
Trong kiểm thử phần mềm, một ca kiểm thử chỉ có giá trị kỹ thuật thực chất khi sở hữu một **Tiên tri Kiểm thử (Test Oracle)** mạnh mẽ, có khả năng phân định ranh giới giữa hành vi đúng đắn và hành vi sai lệch [6]. Tuy nhiên, các kỹ thuật sinh test bằng LLM hiện nay thường bị chi phối bởi mục tiêu tối ưu hóa độ phủ dòng (Line Coverage). Hiện tượng này dẫn tới cái bẫy **Khẳng định rỗng (Hollow Assertions)** hoặc **Bất biến tầm thường (Trivial Invariants)** [3]: mô hình sinh mã thực thi chạy qua toàn bộ thân hàm của MUT nhưng kết thúc bằng lệnh `assert True`, `assert obj is not None`, hoặc chỉ bẫy ngoại lệ một cách chung chung (`except Exception: pass`). Kết quả là bài test đạt độ phủ 100% trên báo cáo nhưng hoàn toàn mù tịt trước các đột biến logic bên trong hàm.

#### Khoảng trống 2: Tính Tất Yếu của Kiểm Thử Đột Biến (Mutation Testing)
Để đo lường độ nhạy thực sự của bộ kiểm thử, lý thuyết kiểm thử phần mềm yêu cầu áp dụng **Kiểm thử Đột biến (Mutation Testing)** [7], [8]. Dựa trên hai tiên đề lý thuyết kinh điển:
- *Giả thiết Lập trình viên Thành thạo (Competent Programmer Hypothesis)*: Nhà phát triển phần mềm thường viết mã gần đúng, các khiếm khuyết phần mềm thực tế thường chỉ là các sai khác cú pháp nhỏ (đột biến cấp 1).
- *Hiệu ứng Ghép lỗi (Coupling Effect)*: Một bộ kiểm thử có khả năng phát hiện và tiêu diệt toàn bộ các lỗi đơn lẻ (First-order mutants) sẽ sở hữu năng lực tiềm tàng để phát hiện các lỗi phức hợp đa tầng (Higher-order mutants).

Tuy nhiên, phần lớn các công cụ sinh test dựa trên LLM hiện nay (như ChatUniTest, CoverUp) chỉ dừng lại ở việc báo cáo độ phủ dòng (Line Coverage) hoặc độ phủ nhánh (Branch Coverage), thiếu vắng hoàn toàn bước đánh giá đột biến hình thức trong vòng đời phát triển của bài kiểm thử.

#### Khoảng trống 3: Cân bằng Pareto giữa Cơ chế Sửa lỗi và Chi phí Hạ tầng CI/CD
Các giải pháp sử dụng Retrieval-Augmented Generation (RAG) đa tầng dựa trên đồ thị gọi hàm (Call-Graph) tuy cung cấp thêm thông tin nhưng lại vấp phải bài toán chi phí tài nguyên: độ trễ khởi động lên tới hàng chục phút, nguy cơ tràn bộ nhớ VRAM, và chi phí gọi API khổng lồ. Ngược lại, các kiến trúc Coder-Critic đơn giản lại dễ rơi vào bẫy ngắt mạch đơn vòng. Khoảng trống đặt ra là: *Làm thế nào để thiết kế một kiến trúc vừa bảo đảm khả năng sửa lỗi sâu hai vòng, vừa giữ chi phí ở mức cực thấp ($< 0,002\text{ USD/suite}$) với thời gian thực thi dưới 10 giây để có thể triển khai thực tế trên các đường ống CI/CD?*

---

### 1.4 So Sánh Đối Sánh Toàn Diện Các Công Trình Đỉnh Cao Liên Quan

Nhằm định vị rõ ràng những bước tiến đột phá của đề tài trong bức tranh tổng thể của ngành kỹ nghệ phần mềm toàn cầu, Bảng 1.1 tiến hành đối chiếu toàn diện giữa kiến trúc **Council-SOTA** và 5 công trình tiên tiến tiêu biểu: **EvoSuite/Pynguin** [4], [5], **ChatUniTest** (Xie et al., FSE 2024) [9], **CoverUp** (Pizzorno & Berger, FSE 2024) [10], **SymPrompt** (Ryan et al., ICSE 2024) [11], và **Meta ACH** (Garg et al., FSE Industry Track 2024) [12].

*Bảng 1.1: Ma trận so sánh đối sánh toàn diện giữa Council-SOTA và các công trình SOTA hàng đầu.*

| Tiêu chí Kỹ thuật | 1. EvoSuite / Pynguin (Fraser 2011; Lukasczyk 2022) | 2. ChatUniTest (Xie et al., FSE 2024) | 3. CoverUp (Pizzorno & Berger, FSE 2024) | 4. SymPrompt (Ryan et al., ICSE 2024) | 5. Meta ACH (Garg et al., FSE 2024) | 6. COUNCIL-SOTA (Đề xuất hiện tại) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Phương pháp luận Chủ đạo** | Tìm kiếm di truyền (SBST / Genetic Algorithms) | Sinh test hướng dẫn theo khung (Framework-guided LLM) | Sinh test định hướng độ phủ trượt (Coverage-guided LLM) | Thúc đẩy có ý thức thực thi ký hiệu (Execution-path LLM) | Sinh test công nghiệp có hướng dẫn đột biến (Industrial LLM) | **Kiến trúc Hội đồng Đa tác nhân Khép kín (Closed-Loop Multi-Agent Council)** |
| **2. Ngôn ngữ & Hỗ trợ Kiểu động** | Java (EvoSuite), Python (Pynguin - tỷ lệ thất bại cao trên kiểu động) | Tập trung Java, phụ thuộc cấu trúc kiểu tĩnh của JVM | Chuyên biệt Python (sử dụng đo lường phân đoạn SlipCover) | Đa ngôn ngữ (C, Java); hỗ trợ hạn chế trên Python động | Đa ngôn ngữ (Hack, Python, C++) tại quy mô hạ tầng Meta | **Chuyên biệt Python Hiện đại (Duck typing, dynamic late-binding, async/decorators)** |
| **3. Cơ chế Neo Ngữ cảnh (Prompt Grounding)** | Không áp dụng (Sinh chuỗi lệnh ngẫu nhiên từ bytecode/reflection) | Tóm tắt lớp ngữ cảnh và đồ thị phụ thuộc phân cấp nông | Cung cấp đoạn mã mục tiêu bị thiếu độ phủ kèm docstring | Trích xuất đường thực thi ký hiệu (Symbolic Path Constraints) | Khai thác cơ sở mã lớn của doanh nghiệp và lịch sử commits | **AST Symbol-Table Export Grounding (Trích xuất bảng xuất khẩu tĩnh, 0 token, < 50ms CPU)** |
| **4. Cơ chế Sửa lỗi & Vòng Hồi tiếp** | Không có (Loại bỏ cá thể lỗi qua toán tử chọn lọc tự nhiên) | Vòng lặp sửa lỗi 1 vòng cơ bản dựa trên thông điệp compiler | Vòng lặp sửa lỗi dựa trên phản hồi ngoại lệ của pytest | Sửa lỗi cú pháp một vòng dựa trên kiểm tra kiểu tĩnh | Sửa lỗi hồi quy thông qua phân tích kết quả CI công nghiệp | **Two-Round Multi-Turn Adaptive Critic (Hồi tiếp traceback, vi sai assertion, khóa AST chống rỗng)** |
| **5. Thẩm định Oracle & Ngữ nghĩa** | Assertions hồi quy tự động (Dễ bất tử hóa lỗi logic có sẵn) | Dựa hoàn toàn vào khả năng nội tại của mô hình tạo sinh | Chỉ thẩm định qua độ phủ dòng/nhánh của SlipCover | Kiểm tra tính thỏa mãn của ràng buộc đường dẫn ký hiệu | Đánh giá đột biến công nghiệp phân tán trên quy mô lớn | **First-Order AST Mutation Testing Engine (187 mutants: ROR, AOR, BVR, CRP, SIR)** |
| **6. Chi phí Tính toán & Triển khai CI/CD** | Tốn CPU chạy mô phỏng di truyền (vài phút / target); 0 USD token | Đắt đỏ (Phụ thuộc API GPT-3.5/GPT-4 thương mại); độ trễ cao | Trung bình (Nhiều chu kỳ gọi LLM bổ sung phân đoạn thiếu) | Rất cao (Độ trễ phân tích ký hiệu kết hợp gọi LLM) | Khổng lồ (Đòi hỏi cụm máy chủ siêu phân tán nội bộ Meta) | **Cực thấp ($0,0013 USD/suite; 5,8–6,6s latency; Ngắt mạch Financial Circuit Breaker)** |

---

### TÀI LIỆU THAM KHẢO CHƯƠNG 1 (REFERENCES)

- [1] R. Liu, Z. Zhang, Y. Hu, Y. Lin, X. Gao, and H. Sun, "Type-aware LLM-based Regression Test Generation for Python Programs," *arXiv preprint arXiv:2503.14000v2*, 2025.
- [2] V. R. Basili and M. V. Zelkowitz, "Analyzing software development failure modes," *IEEE Transactions on Software Engineering*, vol. SE-5, no. 6, pp. 607–615, 1979.
- [3] M. Fulgini, N. Alshahwan, M. Harman, and J. Krinke, "Hollow tests: Detecting and rectifying vacuous assertions in LLM-generated unit tests," in *Proc. 38th IEEE/ACM Int. Conf. Automated Softw. Eng. (ASE)*, 2023, pp. 412–424.
- [4] G. Fraser and A. Arcuri, "EvoSuite: Automatic test suite generation for object-oriented software," in *Proc. 19th ACM SIGSOFT Symp. Found. Softw. Eng. (FSE)*, 2011, pp. 416–419.
- [5] S. Lukasczyk and G. Fraser, "Pynguin: Automated unit test generation for Python," in *Proc. 44th Int. Conf. Softw. Eng. (ICSE Companion)*, 2022, pp. 168–172.
- [6] E. T. Barr, M. Harman, P. McMinn, M. Shahbaz, and S. Yoo, "The oracle problem in software testing: A survey," *IEEE Transactions on Software Engineering*, vol. 41, no. 5, pp. 507–525, 2015.
- [7] R. A. DeMillo, R. J. Lipton, and F. G. Sayward, "Hints on test data selection: Help for the practicing programmer," *IEEE Computer*, vol. 11, no. 4, pp. 34–41, 1978.
- [8] Y. Jia and M. Harman, "An analysis and survey of the development of mutation testing," *IEEE Transactions on Software Engineering*, vol. 37, no. 5, pp. 649–678, 2011.
- [9] Z. Xie, S. Chen, et al., "ChatUniTest: A ChatGPT-based automated unit test generation tool," in *Proc. ACM Int. Conf. Found. Softw. Eng. (FSE)*, 2024.
- [10] J. A. Pizzorno and E. D. Berger, "CoverUp: Coverage-guided test generation for Python using LLMs," in *Proc. ACM Conf. Softw. Eng. (FSE)*, 2024.
- [11] G. Ryan, S. Jain, and B. Ray, "SymPrompt: Code-aware prompting for test generation in regression settings," in *Proc. ACM Int. Conf. Softw. Eng. (ICSE)*, 2024.
- [12] A. Garg, et al., "Mutation-guided LLM-based test generation at Meta," in *Proc. ACM FSE Industry Track*, 2024.
