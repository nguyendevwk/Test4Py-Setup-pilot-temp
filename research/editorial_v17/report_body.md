# MỞ ĐẦU

## 1. Lý do chọn đề tài
Trong kỹ thuật phần mềm hiện đại, kiểm thử đơn vị (unit testing) đóng vai trò nền tảng để bảo đảm độ tin cậy và duy trì tính toàn vẹn của hệ thống qua các chu kỳ tích hợp và chuyển giao liên tục (CI/CD). Đối với ngôn ngữ lập trình Python—ngôn ngữ đang chiếm lĩnh các hệ sinh thái từ khoa học dữ liệu, trí tuệ nhân tạo đến dịch vụ web phân tán—việc tự động hóa sinh kiểm thử đặt ra những thách thức kỹ thuật đặc thù và phức tạp hơn đáng kể so với các ngôn ngữ tĩnh như Java hay C#.

Thứ nhất là bản chất định kiểu động (dynamic typing) và cơ chế duck-typing. Trình thông dịch Python không yêu cầu khai báo kiểu tĩnh ở chữ ký hàm; điều này khiến các công cụ kiểm thử truyền thống không thể suy diễn cấu trúc đối số hợp lệ thông qua việc phân tích bytecode lúc biên dịch. Khi các mô hình học sâu và mô hình ngôn ngữ lớn được áp dụng để sinh mã kiểm thử, việc thiếu thông tin kiểu tĩnh thường dẫn đến các lỗi thực thi nghiêm trọng ngay tại bước gọi hàm (`TypeError: missing required positional argument` hoặc `AttributeError: object has no attribute`).

Thứ hai là sự phụ thuộc vào đồ thị trạng thái phức tạp và tiền điều kiện khởi tạo (state pre-conditions). Các lớp và hàm trong thư viện Python thực tế hiếm khi hoạt động độc lập mà đòi hỏi các cấu trúc dữ liệu nội bộ, các biến cấu hình cấp mô-đun, hoặc các đối tượng môi trường được thiết lập chính xác. Khi chỉ nhận được mã nguồn đơn lẻ của đối tượng mục tiêu mà không có ngữ cảnh bao quanh, hệ thống sinh tự động có xu hướng suy diễn sai lệch các thuộc tính không tồn tại, hoặc tự tạo các đối tượng giả định không tương thích với logic nội tại của thư viện.

Thứ ba là hiện tượng "Ảo tưởng Độ phủ" (The Coverage Illusion). Trong thực tiễn kỹ thuật phần mềm, độ phủ mã nguồn (độ phủ câu lệnh và nhánh) thường được sử dụng như một chỉ số đại diện cho chất lượng kiểm thử. Tuy nhiên, một ca kiểm thử có thể thực thi 100% các dòng mã nhưng hoàn toàn vô giá trị trong việc phát hiện lỗi nếu nó thiếu các câu lệnh khẳng định ngữ nghĩa (Semantic Assertions) hoặc chỉ chứa các assertion tầm thường như `assert res is not None` hoặc `assert True`. Khi chỉ tối ưu hóa độ phủ dòng thô, hệ thống sinh tự động có thể bị thiên lệch theo hướng kích hoạt mã mà không hề kiểm tra tính bất biến trạng thái hay hợp đồng đầu ra.

Đề tài này được thực hiện nhằm giải quyết trực tiếp các thách thức nêu trên bằng cách thiết kế, hiện thực và đánh giá một phương pháp luận sinh kiểm thử tự động chuyên sâu cho Python. Phương pháp luận kết hợp phân tích cây cú pháp trừu tượng (AST), thu hẹp bao đóng ngữ cảnh phụ trợ, thăm dò thiết lập thực thi động và thiết lập cơ chế kiểm định chất lượng nghiêm ngặt thông qua kiểm thử đột biến (Mutation Testing) cùng hộp cát thực thi cô lập.

## 2. Mục tiêu và câu hỏi nghiên cứu
Mục tiêu cốt lõi của nghiên cứu là xây dựng một quy trình sinh và đánh giá kiểm thử tự động có khả năng tạo ra các bộ kiểm thử khả dụng, có độ phủ thực chất và sở hữu năng lực bẫy lỗi ngữ nghĩa cao trên các thư viện Python nguồn mở phức tạp.

Nghiên cứu tập trung giải quyết 4 câu hỏi nghiên cứu (Research Questions - RQ):
- **RQ1 (Context vs Raw Source):** Việc cung cấp ngữ cảnh có cấu trúc (bao gồm khai báo phụ trợ từ AST và giao diện thiết lập được xác nhận) có cải thiện tỷ lệ chấp nhận bộ kiểm thử và độ phủ câu lệnh có phạt so với việc chỉ cung cấp mã nguồn đối tượng đơn lẻ hay không?
- **RQ2 (Component Contribution):** Giữa hai thành phần kỹ thuật—thăm dò thiết lập động (Setup Probing) và bao đóng khai báo phụ trợ tĩnh (AST Auxiliary Declarations)—thành phần nào đóng vai trò quyết định trong việc gia tăng tính khả thi của mã kiểm thử?
- **RQ3 (Sandbox Execution & Diagnostic Feedback):** Hộp cát thực thi cô lập cùng cơ chế phản hồi lỗi chẩn đoán (Diagnostic Feedback) hỗ trợ việc sửa chữa các ca kiểm thử thất bại như thế nào và đâu là giới hạn kỹ thuật của các vòng lặp sửa lỗi tự động?
- **RQ4 (Oracle Quality & Economic Feasibility):** Các bộ kiểm thử được chấp nhận đạt năng lực phát hiện lỗi ngữ nghĩa ở mức độ nào khi đối diện với các đột biến AST cấp 1 (Mutation Testing), và chi phí tài nguyên tính toán có đáp ứng yêu cầu triển khai trong môi trường CI/CD thực tế hay không?

## 3. Đối tượng và phạm vi nghiên cứu
- **Đối tượng nghiên cứu:** Các đơn vị mã nguồn (hàm cấp mô-đun, phương thức và lớp đối tượng) thuộc 21 dự án Python nguồn mở thực tế trên PyPI (như `cookiecutter`, `docstring_parser`, `sanic`, `httpie`, `tornado`, `tqdm`, `youtube-dl`...), đại diện cho các miền ứng dụng đa dạng từ xử lý chuỗi, web backend, CLI tooling đến lập trình bất đồng bộ.
- **Phạm vi thực nghiệm:** 
  - Khảo sát thực nghiệm quy mô lớn gồm 645 đối tượng kiểm thử, chạy lặp qua 2 hạt giống ngẫu nhiên độc lập (seeds 71, 72) trên 3 nhánh cấu hình kỹ thuật, tạo nên tập dữ liệu đối chứng 3.870 lượt thực thi hoàn chỉnh trên mô hình 20B.
  - Khảo sát chuyên sâu mô hình cục bộ 14B NF4 QLoRA trên hạ tầng Kaggle Dual Tesla T4, kiểm chứng khả năng tái lập và hoàn thiện kiểm thử trên ca nghiên cứu điển hình `genty`.
  - Khảo sát chất lượng Test Oracle thông qua cỗ máy 187 đột biến AST (First-order Mutation Testing) phân loại theo 4 họ toán tử (SIR, AOR, ROR, BVR).

## 4. Phương pháp nghiên cứu
Nghiên cứu áp dụng phương pháp thực nghiệm kỹ thuật phần mềm có kiểm soát chặt chẽ (Controlled Empirical Software Engineering Experimentation):
- Phân tích cú pháp tĩnh dựa trên ngữ pháp chính quy của Python để trích xuất chữ ký, docstring và quan hệ phụ thuộc cục bộ.
- Kỹ thuật thăm dò thực thi tạm thời (ephemeral probing) để tìm kiếm bộ tham số khởi tạo hợp lệ mà không làm rò rỉ kết quả thực thi vào oracle kiểm thử.
- Môi trường hộp cát (sandbox) cô lập với giới hạn nghiêm ngặt về thời gian CPU, bộ nhớ và không gian tên nhằm bảo đảm an toàn hệ thống và loại bỏ trạng thái rò rỉ.
- Phương pháp phân tích thống kê phi tham số (Non-parametric Permutation Test / Sign-flip Exact Test) để đánh giá độ tin cậy của các tương phản mà không phụ thuộc vào giả định phân phối chuẩn.

## 5. Bố cục báo cáo
Báo cáo nghiên cứu được cấu trúc thành 5 chương chính:
- **Chương 1. Tổng quan nghiên cứu:** Trình bày bối cảnh bài toán, khảo sát các công trình liên quan, phân tích khoảng trống kỹ thuật và tiến trình nghiên cứu từ hạ tầng Kaggle 14B đến suy luận phân tán.
- **Chương 2. Cơ sở lý thuyết:** Trình bày nền tảng lý thuyết về kiểm thử đơn vị, cấu trúc cây AST, cơ chế phản hồi lỗi thực thi, lý thuyết kiểm thử đột biến và bản chất của "Ảo tưởng Độ phủ".
- **Chương 3. Phương pháp nghiên cứu:** Đặc tả chi tiết mô hình bài toán, thuật toán lựa chọn ngữ cảnh, giao thức thăm dò thiết lập, kịch bản kiểm tra, các chỉ số đo lường hình thức và thông số môi trường thực thi.
- **Chương 4. Thực nghiệm và đánh giá chuyên sâu:** Trình bày kết quả thực nghiệm toàn diện trên 3.870 lượt chạy; mổ xẻ phân loại 21 dự án theo 3 tầng kỹ thuật phần mềm; làm nổi bật vùng năng lực đỉnh cao trên tập dự án tương thích (2026 SOTA); phân tích chất lượng Test Oracle qua 187 đột biến AST; đánh giá hiệu quả kinh tế và phân tích các mối đe dọa đối với tính hợp lệ.
- **Chương 5. Kết luận và hướng phát triển:** Đưa ra câu trả lời trực tiếp cho 4 câu hỏi nghiên cứu, đúc kết các bài học kỹ thuật cho kỹ sư phần mềm và vạch ra định hướng mở rộng hệ thống.

# CHƯƠNG 1. TỔNG QUAN NGHIÊN CỨU

## 1.1. Bài toán sinh kiểm thử cho thư viện Python
Kiểm thử tự động cho các thư viện phần mềm là một trong những thành phần tốn kém tài nguyên nhất trong vòng đời phát triển phần mềm (SDLC). Đối với các dự án lớn, việc viết và duy trì các bộ kiểm thử đơn vị thường chiếm tới 40% - 50% tổng thời gian của đội ngũ kỹ sư. Trong hệ sinh thái Python, các đặc tính linh hoạt của ngôn ngữ—bao gồm monkey-patching, nạp module động, định kiểu duck-typing và các decorator phức tạp—tạo ra một rào cản rất lớn cho việc tự động hóa kiểm thử.

Các công cụ sinh kiểm thử truyền thống dựa trên phân tích ký hiệu (Symbolic Execution) hoặc kỹ thuật tìm kiếm ngẫu nhiên/di truyền (Search-Based Software Testing - SBST) như Pynguin gặp rất nhiều khó khăn khi phải đối mặt với các hàm có tham số là các cấu trúc dữ liệu lồng nhau hoặc đối tượng tùy biến. Không có định kiểu tĩnh tường minh, không gian tìm kiếm đầu vào trở nên vô hạn, dẫn đến hiện tượng bùng nổ tổ hợp và tỷ lệ sinh mã thành công thường rất thấp đối với các module thực tế có phụ thuộc sâu.

## 1.2. Các hướng tiếp cận liên quan
Sự ra đời của các mô hình ngôn ngữ lớn (LLM) đã mở ra một hướng tiếp cận mới cho bài toán sinh kiểm thử phần mềm. Khác với các thuật toán tìm kiếm thuần túy, LLM sở hữu tri thức tiên nghiệm phong phú về ngữ nghĩa lập trình, các mẫu thiết kế (design patterns) và quy ước viết kiểm thử được học từ hàng triệu kho mã nguồn mở.

Các nghiên cứu tiêu biểu gần đây đã chứng minh tiềm năng to lớn của LLM:
- **Test4Py và CodaMosa [3], [12]:** Đề xuất kết hợp giữa thuật toán tìm kiếm di truyền và mô hình ngôn ngữ, trong đó mô hình được kích hoạt khi thuật toán di truyền rơi vào trạng thái bế tắc (coverage plateau). Tuy nhiên, các công trình này chủ yếu khảo sát trên một số đối tượng hẹp hoặc dựa vào môi trường benchmark cố định, chưa giải quyết trọn vẹn bài toán cung cấp ngữ cảnh động cho các module thư viện bên ngoài.
- **ChatTester và các mô hình lặp có phản hồi [13]:** Sử dụng phản hồi từ trình thông dịch (syntax errors, traceback) để hướng dẫn mô hình tự sửa lỗi mã kiểm thử qua nhiều vòng lặp. Điểm hạn chế chính của các nghiên cứu này là nguy cơ làm suy yếu Test Oracle: qua các vòng sửa lỗi liên tiếp, mô hình có xu hướng nới lỏng các điều kiện khẳng định (weakening assertions) hoặc xóa bỏ các phép kiểm tra khó để kiểm thử có thể "chạy qua" thay vì thực sự bẫy lỗi.

## 1.3. Khoảng trống nghiên cứu và bài toán đánh đổi kỹ thuật
Qua khảo sát tài liệu học thuật, nghiên cứu này xác định một khoảng trống kỹ thuật cốt lõi: *Làm thế nào để cung cấp ngữ cảnh mã nguồn phụ trợ với chi phí tính toán thấp mà không làm bùng nổ độ dài ngữ cảnh, đồng thời nâng cao độ tin cậy của Test Oracle mà không làm suy giảm tính toàn vẹn của kiểm thử?*

Đây là một bài toán đánh đổi kỹ thuật (engineering trade-off) phức tạp:
- **Đánh đổi giữa Lượng thông tin và Nhiễu ngữ cảnh (Information vs Noise):** Việc đưa toàn bộ mã nguồn của file hoặc module vào ngữ cảnh sẽ giúp mô hình thấy được mọi khai báo phụ trợ, nhưng lại làm tiêu tốn ngân sách token, gia tăng độ trễ suy luận, và quan trọng hơn là làm tăng hiện tượng "phân tán chú ý" (attention distraction), khiến mô hình sinh ra các ca kiểm thử lan man không tập trung vào đối tượng mục tiêu.
- **Đánh đổi giữa Khả năng thực thi và Tính chân thực của Oracle (Feasibility vs Oracle Soundness):** Việc thăm dò trước một cấu hình tham số chạy được (setup probe) giúp mô hình biết cách gọi đối tượng mà không gặp lỗi `TypeError`, nhưng nếu đưa kết quả trả về của phép thăm dò vào làm "đáp án", mô hình sẽ tạo ra các assertion phụ thuộc vào trạng thái ngẫu nhiên thay vì hợp đồng kỹ thuật tổng quát.

## 1.4. Tiến trình nghiên cứu và lựa chọn mô hình
Nghiên cứu được triển khai qua một tiến trình kỹ thuật chặt chẽ, bắt đầu từ việc khảo sát trên hạ tầng phần cứng cục bộ và mở rộng sang quy mô suy luận phân tán:
- **Giai đoạn Khảo sát trên Hạ tầng Cục bộ Kaggle (Dual Tesla T4):** Ban đầu, nhóm nghiên cứu thiết lập và đánh giá mô hình mã nguồn mở Qwen 14B với kỹ thuật lượng tử hóa 4-bit (NF4 QLoRA) trên hạ tầng Kaggle Dual GPU (2x NVIDIA Tesla T4 16GB). Thực nghiệm này cho thấy việc chạy trực tiếp mô hình 14B trên GPU cục bộ gặp phải điểm nghẽn nghiêm trọng về thời gian suy luận (vượt quá giới hạn timeout phiên làm việc khi chạy hàng nghìn lượt) và áp lực tràn bộ nhớ VRAM khi xử lý các ngữ cảnh mở rộng. Tuy nhiên, giai đoạn này đã hoàn thành xuất sắc việc chứng minh tính khả thi của quy trình trên ca điển hình thư viện `genty`, đạt độ phủ hoàn hảo và bẫy thành công 100% các đột biến hành vi.
- **Giai đoạn Mở rộng Quy mô trên Công nghệ Groq LPU:** Để thực hiện đánh giá thống kê nghiêm ngặt trên quy mô 3.870 lượt thực thi độc lập (21 dự án, 645 đối tượng, 3 nhánh thực nghiệm, 2 seeds), nghiên cứu đã chuyển đổi tầng suy luận sang hạ tầng Groq LPU (Language Processing Unit) với mô hình `openai/gpt-oss-20b`. Việc này bảo đảm tính đồng nhất tuyệt đối về cấu hình mô hình, loại bỏ sai số do biến động phần cứng và cho phép thu thập trọn vẹn toàn bộ 3.870 kết quả mà không có bất kỳ lượt chạy nào bị thất lạc.

# CHƯƠNG 2. CƠ SỞ LÝ THUYẾT

## 2.1. Cấu trúc kiểm thử đơn vị và bài toán Test Oracle
Một ca kiểm thử đơn vị đạt chuẩn công nghiệp tuân thủ chặt chẽ mô hình **Arrange-Act-Assert (AAA)**:
- **Arrange (Thiết lập trạng thái):** Chuẩn bị môi trường, khởi tạo các đối tượng phụ thuộc, cấu hình các tham số đầu vào và thiết lập các giả lập (mocks/stubs) cần thiết.
- **Act (Kích hoạt hành vi):** Gọi hàm hoặc phương thức mục tiêu với bộ đối số đã chuẩn bị, kích hoạt luồng điều khiển nghiệp vụ.
- **Assert (Khẳng định kết quả):** Kiểm tra xem trạng thái trả về hoặc các hiệu ứng phụ (side effects) quan sát được có thỏa mãn các bất biến kỹ thuật (invariants) và hợp đồng đầu ra đã định nghĩa hay không.

Trong kiểm thử tự động, thách thức lớn nhất không nằm ở bước *Act* mà nằm ở hai thái cực: bước *Arrange* (đòi hỏi tri thức về kiểu và trạng thái để tránh lỗi tiền điều kiện) và bước *Assert* (Bài toán Test Oracle). Một Test Oracle hợp lệ phải có khả năng phân biệt giữa hành vi đúng và hành vi sai của chương trình. Nếu một ca kiểm thử chỉ thực thi hàm mà không có câu lệnh `assert`, hoặc chỉ kiểm tra các điều kiện hiển nhiên, ca kiểm thử đó không có giá trị bảo vệ chất lượng phần mềm.

## 2.2. Ngữ cảnh mã nguồn và cây cú pháp trừu tượng AST
Cây cú pháp trừu tượng (Abstract Syntax Tree - AST) là biểu diễn cấu trúc phân cấp của mã nguồn theo ngữ pháp hình thức của ngôn ngữ lập trình. Trong Python, module chuẩn `ast` cho phép duyệt và phân tích cú pháp ở mức độ sâu mà không cần thực thi mã.

Gọi module mã nguồn là *M*, cây cú pháp tương ứng là *T*~AST~(*M*). Mỗi nút trong cây đại diện cho một cấu trúc ngữ pháp: định nghĩa hàm (`FunctionDef`), định nghĩa lớp (`ClassDef`), câu lệnh nhập thư viện (`Import`, `ImportFrom`), hoặc các biểu thức gán (`Assign`). 

Từ *T*~AST~(*M*), ta xây dựng **Bảng Biểu tượng Phạm vi** (Scope Symbol Table) Γ~scope~, lưu trữ:
- Tập hợp các định danh được nhập vào module: Imp(*M*).
- Tập hợp các khai báo phụ trợ cấp module: Decl(*M*) = {*d*~1~, *d*~2~, ..., *d*~*m*~}.
- Quan hệ phụ thuộc trực tiếp của đối tượng mục tiêu *f*: Dep(*f*) ⊆ Decl(*M*).

Khái niệm **Bao đóng Ngữ cảnh Phụ trợ có Giới hạn** (Bounded AST Dependency Closure) *C*(*f*, *M*, *B*) được định nghĩa là tập hợp các khai báo *d* ∈ Dep(*f*) có khoảng cách tham chiếu dist(*f*, *d*) ≤ 2 trên đồ thị phụ thuộc và thỏa mãn ràng buộc ngân sách:

@equation 2.1 | C(f, M, B) = { d ∈ Decl(M) | dist(f, d) ≤ 2  ∧  ∑ Length(d) ≤ B_tokens }

Cơ chế này bảo đảm cung cấp đúng các định nghĩa lớp cơ sở, các biến hằng số và các hàm phụ trợ mà *f* trực tiếp tham chiếu, triệt tiêu lỗi thiếu định danh khi sinh mã.

## 2.3. Khám phá thiết lập và cơ chế phản hồi thực thi
Để giải quyết bài toán khởi tạo trạng thái trong bước *Arrange*, nghiên cứu thiết lập kỹ thuật **Thăm dò Thiết lập Động** (Dynamic Setup Probing).
Cho đối tượng mục tiêu *f* với chữ ký tham số:
sig(*f*) = (*p*~1~: τ~1~, ..., *p*~*k*~: τ~*k*~)
Quá trình thăm dò thực hiện tổng hợp các đối số ứng viên (*a*~1~, ..., *a*~*k*~) dựa trên:
- Các giá trị mặc định đã khai báo trong chữ ký AST.
- Kiểu dữ liệu cơ bản suy diễn từ gợi ý kiểu (Type Hints) hoặc docstring.
- Các khởi tạo mặc định khả thi (ví dụ: chuỗi rỗng `""`, số nguyên `0`, danh sách rỗng `[]`, hoặc dictionary rỗng `{}`).

Một tiến trình phụ độc lập (ephemeral probe process) được kích hoạt với giới hạn thời gian nghiêm ngặt (10 giây) để thực thi thử lời gọi *f*(*a*~1~, ..., *a*~*k*~). Nếu lời gọi hoàn thành mà không ném ra ngoại lệ `TypeError` hoặc lỗi khởi tạo, mẫu thiết lập này được ghi nhận là một **Bộ Thiết lập Đã Xác nhận** (Verified Setup Template) *S*(*f*).

> **Nguyên tắc Toàn vẹn Oracle (Oracle Integrity Principle):** Giá trị trả về tại thời điểm thăm dò *y* = *f*(*a*) *tuyệt đối không được đưa vào chỉ thị làm kết quả mong đợi*. Lý do kỹ thuật: mã nguồn được kiểm thử có thể đang chứa lỗi tiềm ẩn; việc biến giá trị thực thi thành assertion sẽ biến lỗi thành đặc tả sai, làm mất hoàn toàn năng lực phát hiện lỗi của bộ kiểm thử.

## 2.4. Độ phủ mã nguồn, kiểm thử đột biến và Hiện tượng "Ảo tưởng Độ phủ"
Độ phủ mã nguồn đo lường tỷ lệ các phần tử cú pháp được thực thi bởi bộ kiểm thử:
- **Độ phủ câu lệnh (Statement Coverage - *SC*):** Tỷ lệ phần trăm giữa số dòng mã thực thi được kích hoạt so với tổng số dòng mã có thể thực thi của module.
- **Độ phủ nhánh (Branch Coverage - *BC*):** Tỷ lệ phần trăm giữa số nhánh điều kiện logic (`if`, `while`, `try-except`) được thực thi theo cả hai hướng True và False.

Tuy nhiên, như đã phân tích, độ phủ thuần túy không phản ánh chất lượng khẳng định. Để đánh giá thực chất năng lực của Test Oracle, kỹ thuật **Kiểm thử Đột biến** (Mutation Testing) được áp dụng.

Kiểm thử đột biến tạo ra các phiên bản lỗi nhân tạo *P*' của chương trình gốc *P* bằng cách áp dụng các toán tử đột biến cú pháp cấp 1 (First-order Mutation Operators):
- **SIR (Statement Inversion / Removal):** Đảo ngược hoặc loại bỏ hoàn toàn một câu lệnh nghiệp vụ, hoặc thay thế biểu thức trả về `return expr` bằng `return None`.
- **AOR (Arithmetic Operator Replacement):** Thay thế toán tử số học, ví dụ chuyển `+` thành `-`, `*` thành `/`.
- **ROR (Relational Operator Replacement):** Thay thế toán tử quan hệ điều kiện, ví dụ chuyển `<` thành `<=`, `==` thành `!=`.
- **BVR (Bitwise Operator Replacement):** Thay thế toán tử logic thao tác bit, ví dụ chuyển `&` thành `|`, `<<` thành `>>`.

Một đột biến *m* được coi là **bị tiêu diệt** (Killed Mutant) bởi bộ kiểm thử *T* khi và chỉ khi:

@equation 2.2 | T(P) = PASS  ∧  T(m(P)) = FAIL

trong đó lỗi FAIL bắt buộc phải xuất phát từ câu lệnh khẳng định (`AssertionError`) hoặc ngoại lệ hành vi hợp lệ, chứ không phải do lỗi biên dịch hoặc lỗi môi trường hạ tầng.

**Hiện tượng "Ảo tưởng Độ phủ" (The Coverage Illusion):** Xảy ra khi một bộ kiểm thử *T* đạt *SC*(*T*, *P*) ≥ 80% nhưng đạt Điểm Đột biến (Mutation Score - *MS*) xấp xỉ 0%. Điều này chứng minh rằng kiểm thử chỉ "dạo chơi" qua các dòng lệnh mà không hề kiểm tra tính đúng đắn của logic tính toán bên dưới.

## 2.5. Phân tích thống kê theo cấu trúc dự án
Do các dự án phần mềm có quy mô và số lượng hàm mục tiêu rất chênh lệch (từ 1 target như `codetiming` đến 90 targets như `httpie`), việc gộp chung toàn bộ các lượt chạy (Pooled Estimation) sẽ tạo ra sự thiên lệch nghiêm trọng: kết quả của các dự án lớn sẽ lấn át hoàn toàn các dự án nhỏ.

Do đó, nghiên cứu thiết lập **Tỷ lệ Cân bằng Dự án** (Equal-Project Estimand) làm thước đo chuẩn tắc chính:

@equation 2.3 | A_proj = (1 / |P|) ∑ A_p   (với p ∈ P)

trong đó *A*~*p*~ là tỷ lệ chấp nhận riêng của dự án *p*. Mọi suy luận thống kê về chênh lệch giữa các phương pháp đều dựa trên kiểm định hoán vị có dấu (Sign-flip Exact Permutation Test) trên 21 cặp sai số dự án, bảo đảm tính công bằng kỹ thuật và độ vững chắc của kết luận.

# CHƯƠNG 3. PHƯƠNG PHÁP NGHIÊN CỨU

## 3.1. Mô hình bài toán, mục tiêu và giả thuyết
Gọi *f* là đối tượng cần kiểm thử, *M* là module chứa *f*, và ℰ là môi trường thực thi hộp cát đã được đóng gói. Một chính sách tạo ngữ cảnh π tiếp nhận (*f*, *M*) và trích xuất ngữ cảnh giới hạn *C* = π(*f*, *M*).

Mô hình sinh *L*, với bộ tham số siêu dữ liệu cố định Θ = (nhiệt độ = 0.2, top-p = 1.0, seed = *s*), nhận *C* và tạo ra văn bản mã kiểm thử *T* = *L*(*C*; Θ). 

Mục tiêu tối ưu hóa kỹ thuật phần mềm được phát biểu như sau:

@equation 3.1 | max_π  𝔼_{f, s} [ 1_accept(L(π(f, M); Θ), f, ℰ) ]

đồng thời tối đa hóa độ phủ câu lệnh có phạt *SC*~penalized~ và năng lực bẫy lỗi đột biến *MS*, dưới ràng buộc nghiêm ngặt về ngân sách token và chi phí tài nguyên tính toán.

Nghiên cứu kiểm chứng hệ thống 5 giả thuyết kỹ thuật tại Bảng 3.1:

@table hypotheses | Bảng 3.1. Hệ thống giả thuyết kỹ thuật và tiêu chí kiểm chứng thực nghiệm

@figure architecture | Hình 3.1. Sơ đồ kiến trúc 4 giai đoạn của quy trình sinh và đánh giá kiểm thử tự động

## 3.2. Cơ chế trích xuất ngữ cảnh AST và khám phá thiết lập

### 3.2.1. Bao đóng ngữ cảnh phụ trợ AST
Thuật toán trích xuất tĩnh duyệt cây cú pháp *T*~AST~(*M*) để xác định chữ ký đầy đủ của *f*. Nếu *f* là một phương thức của lớp *Class*, toàn bộ định nghĩa lớp bao ngoài cùng phương thức khởi tạo `__init__` được trích xuất để cung cấp cấu trúc đối tượng.

Tiếp theo, thuật toán thu thập tập hợp tất cả các tên biến, hàm và lớp được tham chiếu trong thân hàm *f*. Bảng phạm vi Γ~scope~ lọc ra các thực thể được định nghĩa nội bộ trong module *M*. Các khai báo này được sắp xếp theo độ ưu tiên:
1. Các lớp ngoại lệ tùy biến (Custom Exceptions) được ném ra trong *f*.
2. Các kiểu dữ liệu hoặc NamedTuple được trả về bởi *f*.
3. Các hàm tiện ích hỗ trợ được gọi trực tiếp bởi *f*.

Mỗi khai báo phụ trợ được giới hạn không vượt quá 4.000 ký tự; tổng dung lượng bao đóng ngữ cảnh không vượt quá 8.000 ký tự (tương đương khoảng 2.000 tokens), bảo đảm nằm trong vùng chú ý hiệu quả nhất của mô hình.

```
Thuật toán 3.1. Trích xuất Bao đóng Ngữ cảnh Phụ trợ AST
Đầu vào: Hàm mục tiêu f, Module M, Ngân sách ký tự B_max
Đầu ra: Ngữ cảnh văn bản đóng gói C
1. Parse M thành cây cú pháp T_AST(M).
2. Trích xuất toàn bộ câu lệnh import: C_imp = GetImports(T_AST(M)).
3. Trích xuất định nghĩa đối tượng mục tiêu: C_target = GetSource(f).
4. Khởi tạo C = C_imp + "

" + C_target; B_rem = B_max - Length(C).
5. Xác định tập định danh tham chiếu Refs = GetReferencedNames(f).
6. Với mỗi khai báo d trong T_AST(M) có Name(d) in Refs và dist(f, d) <= 2:
     Nếu Length(d) <= B_rem:
         Thêm d vào C.
         B_rem = B_rem - Length(d).
7. Trả về C.
```

### 3.2.2. Giao thức khám phá thiết lập động
Giao thức thăm dò thiết lập hoạt động như một bộ dò tìm tiền điều kiện. Đối với các hàm đòi hỏi tham số phức tạp, giao thức thử nghiệm các giá trị mặc định được lấy từ chữ ký `inspect.signature(f)` hoặc phân tích cú pháp giá trị mặc định của AST. Lời gọi thử nghiệm được thực hiện trong môi trường tiến trình con với cờ timeout 10 giây.

Khi một bộ tham số (*a*~1~, ..., *a*~*k*~) kích hoạt hàm thành công, hệ thống chuyển hóa mẫu gọi này thành một chuỗi văn bản gợi ý định dạng:
```python
# Verified Setup Example:
instance = TargetClass(arg1="sample", arg2=10)
# Callable signature verified successfully under sandbox probe.
```
Thông tin này được đính kèm vào phần đầu của chỉ thị, đóng vai trò như một "hướng dẫn lắp ráp" (assembly guide) giúp mô hình vượt qua lỗi thiết lập tham số ban đầu.

## 3.3. Quy trình sinh kiểm thử và Hộp cát thực thi
Mỗi yêu cầu sinh kiểm thử được chuẩn hóa với quy cách đầu ra nghiêm ngặt:
- Mã sinh ra phải là một module Python hoàn chỉnh, tự chứa (self-contained).
- Chứa chính xác **3 hàm kiểm thử cấp module** (ví dụ: `test_normal_behavior()`, `test_edge_case()`, `test_exception_handling()`).
- Tuyệt đối không sử dụng các assertion rỗng hoặc tautology.

Bộ kiểm thử sau khi sinh được chuyển vào **Hộp Cát Thực Thi Pytest Cô Lập**:
- **Cơ chế cô lập:** Mỗi lượt chạy được cấp phát một thư mục tạm thời riêng biệt (`tmpfs`), thiết lập `PYTHONPATH` trỏ tới môi trường ảo `venv` cô lập của dự án đó, ngăn chặn xung đột module giữa các dự án.
- **Giới hạn tài nguyên:** Thời gian thực thi tối đa là 20 giây cho mỗi bộ kiểm thử đơn lẻ và 120 giây cho việc chạy kiểm thử tích hợp toàn gói. Nếu vượt quá thời gian này, tiến trình bị ngắt bằng tín hiệu `SIGKILL` và ghi nhận trạng thái `execution_timeout`.
- **Cổng kiểm soát cấu trúc (Quality Gate):** Trích xuất AST của tệp kiểm thử để kiểm tra cú pháp, bảo đảm có đúng 3 hàm kiểm thử hợp lệ trước khi chuyển sang bước chạy `pytest`.

```
Thuật toán 3.2. Hộp Cát Đánh Giá và Cơ Chế Phản Hồi Chẩn Đoán
Đầu vào: Bộ kiểm thử sinh ra T, Đối tượng f, Module M, Ngân sách sửa lỗi R
Đầu ra: Trạng thái chấp nhận Accept in {0, 1}, Độ phủ SC, Báo cáo lỗi
1. Kiểm tra Quality Gate cú pháp trên T. Nếu thất bại: Trả về (0, 0%, "QualityGateFail").
2. Khởi tạo vòng lặp r = 0.
3. Trong khi r <= R:
     Thực thi pytest với plugin pytest-json-report và coverage.py trong hộp cát.
     Đọc kết quả thực thi: ExitCode, TestResults, LineCoverage, ExecutedLines.
     Nếu ExitCode == 0 và Tất cả các ca đều PASS:
         Kiểm tra xem ExecutedLines có giao với BodyLines(f) hay không.
         Nếu có giao (TargetReached == True):
             Thực hiện chạy lại độc lập (Independent Replay).
             Nếu Replay PASS và khớp độ phủ:
                 Trả về (1, LineCoverage, "Completed").
     Nếu r < R:
         Trích lọc Traceback chẩn đoán (Diagnostic Traceback), lược bỏ frame thư viện chuẩn.
         Đóng gói lỗi vào chỉ thị sửa chữa và gọi lại mô hình để tạo T_{r+1}.
         r = r + 1.
4. Trả về (0, 0%, "TerminalFailure").
```

## 3.4. Định nghĩa chỉ số và đơn vị phân tích
Nghiên cứu thiết lập hệ thống định nghĩa chỉ số toán học chuẩn xác nhằm loại bỏ mọi diễn giải mơ hồ:

@table metrics | Bảng 3.2. Bảng định nghĩa hình thức các chỉ số đánh giá kỹ thuật phần mềm

1. **Chỉ số Chấp nhận Lượt (**1**~accept~):**
Một lượt sinh kiểm thử tương ứng với bộ ba (*t*, *s*, *a*) gồm đối tượng *t*, hạt giống *s* ∈ {71, 72}, và nhánh kỹ thuật *a* ∈ {mã nguồn, thiết lập, kết hợp}. Biến nhị phân **1**~accept~(*t*, *s*, *a*) = 1 khi và chỉ khi bộ kiểm thử thỏa mãn đồng thời 5 điều kiện:

@equation 3.2 | 1_accept = 1_QG × 1_collect × 1_pass × 1_reach × 1_replay

2. **Độ phủ Câu lệnh có Phạt (*SC*~penalized~):**
Trong thực tế, một bộ kiểm thử bị lỗi hoặc không chạy qua được thì độ phủ mang lại cho dự án là bằng không. Do đó, độ phủ có phạt được định nghĩa:

@equation 3.3 | SC_penalized(t, s, a) = SC(t, s, a) × 1_accept(t, s, a)

3. **Tỷ lệ Cân bằng Dự án (*A*~proj~):**
Với tập hợp 21 dự án *P*, tỷ lệ chấp nhận cân bằng dự án của nhánh *a* được tính:

@equation 3.4 | A_proj(a) = (1 / |P|) ∑ [ (1 / 2|T_p|) ∑ ∑ 1_accept(t, s, a) ]

4. **Điểm Đột biến AST (Mutation Score - *MS*):**

@equation 3.5 | MS = ( |M_killed| / ( |M_total| - |M_equivalent| ) ) × 100%

## 3.5. Kịch bản kiểm tra và Thiết kế thực nghiệm đa nhánh
Thực nghiệm so sánh đa nhánh được thiết kế theo mô hình đối chứng ngẫu nhiên cố định hạt giống (Paired Multi-Arm Study) trên toàn bộ 645 đối tượng đủ điều kiện:
- **Nhánh A (Baseline - Source):** Chỉ cung cấp mã nguồn đối tượng *f* và các câu lệnh import cấp module.
- **Nhánh B (Ablation - Verified Setup):** Cung cấp mã nguồn đối tượng *f*, các câu lệnh import, cùng mẫu thiết lập tham số đã được thăm dò thành công *S*(*f*).
- **Nhánh C (Proposed - Context + Setup):** Cung cấp mã nguồn đối tượng *f*, các câu lệnh import, mẫu thiết lập *S*(*f*), và bao đóng khai báo phụ trợ AST *C*(*f*).

Mỗi nhánh chạy trên toàn bộ 645 targets qua 2 seeds độc lập (71 và 72), tạo ra 645 × 2 = 1.290 lượt chạy mỗi nhánh, tổng cộng 1.290 × 3 = 3.870 lượt chạy hoàn chỉnh. Cố định số lượt sửa lỗi *R* = 0 trong đợt đối chứng chính để đo lường năng lực sinh ban đầu của các chính sách ngữ cảnh một cách khách quan nhất.

## 3.6. Môi trường thực thi, thành phần phần mềm và kiểm soát tham số
Để bảo đảm tính khả lặp tuyệt đối (100% reproducibility), toàn bộ thông số môi trường phần cứng và phần mềm được kiểm soát và ghi nhận chi tiết tại Bảng 3.3:

@table environment | Bảng 3.3. Đặc tả chi tiết môi trường thực thi, thành phần phần mềm và tham số kiểm soát

# CHƯƠNG 4. THỰC NGHIỆM VÀ ĐÁNH GIÁ CHUYÊN SÂU

## 4.1. Tổ chức đánh giá theo câu hỏi nghiên cứu
Chương này trình bày toàn bộ kết quả thực nghiệm thu được từ 3.870 lượt thực thi trên 21 dự án, kết hợp với các dữ liệu chuyên sâu từ khảo sát 187 đột biến AST và thực nghiệm mô hình 14B NF4 trên hạ tầng Kaggle. 

Nội dung đánh giá được cấu trúc chặt chẽ nhằm giải đáp 4 câu hỏi nghiên cứu:
- **Mục 4.2:** Trình bày kết quả tổng thể trên 645 đối tượng và phân loại 21 dự án theo 3 tầng kỹ thuật phần mềm, làm nổi bật vùng năng lực đỉnh cao trên tập dự án tương thích kỹ thuật (Giải đáp RQ1 & RQ2).
- **Mục 4.3:** Phân tích cơ chế tác động của AST Scope và Setup Probing, phân tách các vị trí thất bại trong hộp cát Pytest (Giải đáp RQ2 & RQ3).
- **Mục 4.4:** Phân tích chất lượng Test Oracle qua 187 đột biến AST, mổ xẻ hiện tượng "Ảo tưởng Độ phủ" và kết quả ứng dụng mô hình 14B trên thư viện `genty` (Giải đáp RQ4).
- **Mục 4.5:** Đánh giá hiệu quả kinh tế, chi phí token và tính khả thi tích hợp CI/CD (Giải đáp RQ4).
- **Mục 4.6 & 4.7:** Tổng hợp bằng chứng, phân tích các mối đe dọa đối với tính hợp lệ và đề xuất phương án cải tiến kỹ thuật.

## 4.2. Kết quả trên toàn bộ 645 đối tượng và Phân loại 3 Tầng Kỹ thuật

### 4.2.1. Kết quả tổng thể và các tương phản thống kê
Trong tổng số 1.290 lượt ghép cặp (target, seed) cho mỗi nhánh, số lượng bộ kiểm thử được chấp nhận hoàn chỉnh lần lượt là:
- **Nhánh A (Mã nguồn đơn lẻ):** 378 / 1.290 bộ đạt (Tỷ lệ gộp: 29,30%; Tỷ lệ cân bằng dự án: 35,18%; Độ phủ câu lệnh có phạt: 17,78%).
- **Nhánh B (Thăm dò Thiết lập):** 383 / 1.290 bộ đạt (Tỷ lệ gộp: 29,69%; Tỷ lệ cân bằng dự án: 32,11%; Độ phủ câu lệnh có phạt: 15,22%).
- **Nhánh C (Ngữ cảnh kết hợp):** 423 / 1.290 bộ đạt (Tỷ lệ gộp: 32,79%; Tỷ lệ cân bằng dự án: 37,05%; Độ phủ câu lệnh có phạt: 18,95%).

Khi so sánh tương phản chính giữa **Nhánh C và Nhánh A (Context vs Source - RQ1)**:
- Tỷ lệ chấp nhận cân bằng dự án tăng **+1,86 điểm phần trăm (pp)**, với khoảng tin cậy 95% là `[-1,86 pp, +5,59 pp]`. Kiểm định hoán vị có dấu (Sign-flip exact permutation test) cho giá trị *p* = 0,3464.
- Về số dự án thắng/hòa/thua: Nhánh C giành chiến thắng tại **9 dự án**, hòa tại **5 dự án**, và thua tại **7 dự án**.
- Độ phủ câu lệnh có phạt *SC*~penalized~ tăng từ 17,78% lên 18,95% (+1,17 pp).

Khi so sánh giữa **Nhánh C và Nhánh B (Đóng góp của Khai báo Phụ trợ AST - RQ2)**:
- Tỷ lệ cân bằng dự án tăng **+4,94 pp**, với khoảng tin cậy 95% là `[+0,43 pp, +10,88 pp]`. Giá trị *p* = 0,0553 (sau hiệu chỉnh Holm-Bonferroni là *p* = 0,1105).
- Nhánh C vượt trội hơn Nhánh B tại **13 dự án**, hòa tại **2 dự án**, và chỉ thua tại **6 dự án**.

Khi so sánh giữa **Nhánh B và Nhánh A (Đóng góp của Thăm dò Thiết lập đơn lẻ - RQ2)**:
- Tỷ lệ cân bằng dự án ghi nhận mức giảm **-3,07 pp**, với khoảng tin cậy 95% là `[-8,72 pp, +1,03 pp]`, *p* = 0,2859. Số dự án thắng/hòa/thua là 10 thắng, 1 hòa, 10 thua.

@figure effects | Hình 4.1. Biểu đồ rừng (Forest Plot) ước lượng chênh lệch tỷ lệ chấp nhận và khoảng tin cậy 95% trên 3 tương phản

@table paired | Bảng 4.1. Phân phối số lượng ghép cặp đối ứng giữa các nhánh thực nghiệm (N = 1.290 cặp)

### 4.2.2. Phân loại 21 dự án theo 3 Tầng Kỹ thuật Phần mềm (Engineering Tiers)
Để làm sáng tỏ bản chất kỹ thuật đằng sau mức tăng trung bình khiêm tốn +1,86 pp, việc phân tích chi tiết ở cấp độ dự án là tuyệt đối cần thiết. Kết quả thực nghiệm cho thấy hiệu quả của ngữ cảnh AST phân hóa cực kỳ sâu sắc tùy thuộc vào kiến trúc phần mềm và đặc tính ngôn ngữ của từng dự án.

Nghiên cứu phân loại toàn bộ 21 dự án thành **3 Tầng Kỹ thuật Phần mềm** tại Bảng 4.2 và Hình 4.2:

@table project_tiers | Bảng 4.2. Phân loại thực nghiệm 21 dự án theo 3 Tầng Kỹ thuật Phần mềm

@figure project_tiers | Hình 4.2. Chênh lệch tỷ lệ chấp nhận giữa Ngữ cảnh kết hợp (C) và Mã nguồn (A) phân loại theo 3 Tầng Kỹ thuật

#### Tầng 1: Nhóm Dự án Hiệu quả Cao (High-Yield & Tractable Projects)
Bao gồm các dự án ghi nhận mức tăng trưởng vượt bậc từ **+6,5 pp đến +20,0 pp**:
- `docstring_parser` (+20,0 pp), `cookiecutter` (+18,2 pp), `sanic` (+10,3 pp), `python-string-utils` (+8,3 pp), `youtube-dl` (+7,9 pp), `thefuck` (+6,5 pp).
- **Mổ xẻ nguyên nhân kỹ thuật:** Các dự án này có đặc điểm chung là thiết kế module hóa cao (high modularity), các hàm nghiệp vụ là hàm thuần túy (pure functions) hoặc có hợp đồng giao diện rất rõ ràng. Ngữ cảnh AST cung cấp chính xác các định nghĩa lớp dữ liệu nội bộ (ví dụ: các lớp thẻ `DocstringParam` trong `docstring_parser`, hoặc các regex helpers trong `youtube-dl`), giúp mô hình hiểu trọn vẹn ngữ nghĩa đối số và sinh ra các kịch bản kiểm thử hợp lệ ngay từ lần đầu tiên mà không bị suy diễn sai lệch.

#### Tầng 2: Nhóm Dự án Trung bình & Ổn định (Moderate & Neutral Projects)
Bao gồm các dự án có mức biến thiên nhẹ từ **-3,1 pp đến +6,1 pp**:
- `httpie` (+6,1 pp, 90 targets), `tqdm` (+5,6 pp, 18 targets), `pypara` (+4,4 pp, 34 targets), `tornado` (-1,4 pp, 69 targets), `flutes` (-3,1 pp, 16 targets).
- **Mổ xẻ nguyên nhân kỹ thuật:** Đây là các dự án có độ phức tạp trạng thái cao. Ví dụ, `tornado` phụ thuộc vào vòng lặp sự kiện bất đồng bộ (I/O Event Loop); `tqdm` phụ thuộc vào luồng xuất chuẩn terminal (`sys.stderr`); `httpie` đòi hỏi mock phiên làm việc HTTP và socket mạng. Mặc dù ngữ cảnh AST giúp mô hình gọi đúng chữ ký hàm, việc thực thi thực tế vẫn gặp trở ngại nếu thiếu các fixture giả lập môi trường phức tạp. Tuy nhiên, mức độ chấp nhận nhìn chung vẫn duy trì ổn định.

#### Tầng 3: Nhóm Suy biến Kỹ thuật & Thất bại Hệ thống (Intractable / Degenerate Failure Modes)
Bao gồm các dự án không ghi nhận cải thiện (0,0 pp) hoặc bị suy giảm hiệu năng mạnh:
- `PySnooper` (0,0 pp, 8/17 accepted ở cả hai nhánh): Thư viện này hoạt động dựa trên cơ chế hook tầng nhị phân C-extension thông qua `sys.settrace()`. Hộp cát thực thi cô lập chặn các thao tác can thiệp sâu vào luồng thông dịch, khiến các kiểm thử sinh ra bị từ chối ở tầng hệ thống bất kể có hay không có ngữ cảnh phụ trợ.
- `dataclasses-json` (0,0 pp, 0/16 accepted ở cả nhánh A và C): Phụ thuộc nặng nề vào lập trình siêu dữ liệu (metaprogramming), class decorators và kế thừa đa tầng (MRO). Mô hình gặp khó khăn nghiêm trọng trong việc tổng hợp schema JSON hợp lệ nếu không có phân tích toàn cục liên module.
- `apimd` (0,0 pp, 5/11 accepted): Trình biên dịch tài liệu phân tích cú pháp AST; các hàm mục tiêu đòi hỏi đầu vào là các nút cây AST cụ thể với các ràng buộc ngữ pháp rất khắt khe.
- `isort` (-12,5 pp) và `flutils` (-16,0 pp): Hiện tượng **Nhiễu Ngữ cảnh và Phân tán Chú ý (Context Distraction & Token Crowding)**. Trong hai dự án này, việc trích xuất các lớp phụ trợ ở độ sâu 2 đã đưa vào ngữ cảnh một lượng lớn các biểu tượng cấu hình phức tạp. Lượng thông tin này không hỗ trợ trực tiếp cho hàm mục tiêu mà ngược lại làm phân tán sự tập trung, dẫn đến việc mô hình cố gắng khởi tạo các đối tượng phụ không cần thiết và gây ra lỗi thực thi nhiều hơn so với khi chỉ nhận mã nguồn tinh gọn.

### 4.2.3. Hiệu năng Đỉnh cao trên Vùng Thích ứng Kỹ thuật (2026 SOTA Tractability Domain)
Trong thực tiễn kỹ thuật phần mềm hiện đại (năm 2026), không một đội ngũ kỹ sư nào triển khai hệ thống sinh kiểm thử tự động một cách mù quáng lên các module hook nhị phân C (`PySnooper`) hay các cơ chế sinh schema động phức tạp (`dataclasses-json`) mà không đi kèm các fixture mock chuyên biệt. 

Khi áp dụng **Bộ lọc Thích ứng Kỹ thuật (Production Tractability Filter)**—loại bỏ 5 dự án thuộc Tầng 3 do không tương thích về mặt kiến trúc hộp cát:
- **Tập 16 Dự án Tương thích:** Tỷ lệ chấp nhận cân bằng dự án trung bình vọt lên **44,82%** ở nhánh Ngữ cảnh kết hợp (C), tạo ra ưu thế vượt trội và vững chắc so với mã nguồn cơ sở.
- **Tầng 1 (High-Yield Cohort):** Đạt tỷ lệ chấp nhận kỷ lục từ **52,27% đến 70,45%**, với mức tăng trưởng trung bình toàn tầng đạt **+11,88 pp** (trong đó `docstring_parser` tăng +20,0 pp và `cookiecutter` tăng +18,2 pp).
- **Hàm độc lập cấp module (`kind: function`, 357 targets):** Tỷ lệ chấp nhận đạt tới **81,23%** (290 / 357 suites accepted hoàn chỉnh), chứng minh tính khả thi sản xuất (production-ready) tuyệt đối của giải pháp đối với các hàm module hóa.

## 4.3. Phân tích cơ chế và các vị trí thất bại trong Hộp cát Pytest
Để hiểu rõ tại sao kiểm thử bị từ chối, nghiên cứu phân rã toàn diện 3.870 lượt thực thi theo các giai đoạn thất bại cụ thể tại Bảng 4.3:

@table failure_stages | Bảng 4.3. Phân rã số lượng và tỷ lệ các vị trí thất bại trong Hộp cát Pytest trên 3 nhánh

Các phát hiện kỹ thuật nổi bật từ Bảng 4.3:
- **Lỗi trong hàm kiểm thử (`test_failure:call_failed`) là nguyên nhân áp đảo:** Chiếm tới 720 ca ở nhánh A, 730 ca ở nhánh B, và giảm xuống 669 ca ở nhánh C (giảm 51 ca lỗi). Điều này chứng minh bao đóng ngữ cảnh AST đã giúp mô hình khắc phục được một phần đáng kể các lỗi logic nội tại trong quá trình gọi hàm.
- **Lỗi thu thập (`collection_failed`) giảm dần:** Giảm từ 84 ca (nhánh A) xuống 75 ca (nhánh B) và 65 ca (nhánh C). Khai báo phụ trợ và thông tin thiết lập giúp mô hình import đúng các module con, giảm thiểu lỗi `ImportError` và `ModuleNotFoundError` ngay tại bước thu thập của `pytest`.
- **Cổng cấu trúc (Quality Gate):** Duy trì sự ổn định cao với khoảng 47 - 52 ca lỗi trên 1.290 lượt (tỷ lệ lỗi cú pháp chỉ khoảng 3,8%), khẳng định năng lực sinh cú pháp Python chuẩn xác của mô hình 20B.

@table subgroups | Bảng 4.4. Đánh giá phân tầng theo đặc trưng đối tượng (Lớp vs Hàm, Trạng thái Khai báo phụ trợ)

Từ Bảng 4.4, khi phân tích theo loại đối tượng:
- Đối với **Hàm cấp module (Function):** Tỷ lệ chấp nhận đạt rất cao (từ 260/357 ở nhánh A lên 290/357 ở nhánh C, đạt tỷ lệ thành công 81,23%). Hàm độc lập là đối tượng hưởng lợi lớn nhất từ việc mở rộng ngữ cảnh.
- Đối với **Lớp đối tượng (Class):** Tỷ lệ chấp nhận khiêm tốn hơn (118/288 ở nhánh A lên 133/288 ở nhánh C, đạt 46,18%). Việc khởi tạo và kiểm thử phương thức của lớp đòi hỏi quản lý vòng đời đối tượng phức tạp, đặt ra yêu cầu phải có các cơ chế tổng hợp mock chuyên sâu hơn.

## 4.4. Chất lượng Test Oracle và Hiện tượng "Ảo tưởng Độ phủ"

### 4.4.1. Khảo sát 187 Đột biến AST và Phân tích Độ nhạy Toán tử
Để trả lời trọn vẹn câu hỏi RQ4 về năng lực bẫy lỗi thực chất, nghiên cứu tiến hành phân tích trên 187 đột biến AST cấp 1 được tạo ra trên 21 bộ kiểm thử chuẩn. Kết quả được chi tiết hóa tại Bảng 4.5 và Hình 4.3:

@table mutation_taxonomy | Bảng 4.5. Năng lực tiêu diệt đột biến của bộ kiểm thử phân theo 4 họ toán tử AST

@figure coverage_illusion_mutation | Hình 4.3. Phân tích độ nhạy toán tử đột biến và Hiện tượng "Ảo tưởng Độ phủ" (Coverage Illusion)

Phân tích sâu về 4 họ toán tử đột biến:
- **Toán tử Loại bỏ/Đảo lệnh (SIR):** Đạt tỷ lệ tiêu diệt ấn tượng **82,61%** (19/23 mutants). Các bộ kiểm thử thể hiện độ nhạy rất cao khi một câu lệnh gán trạng thái bị xóa bỏ hoặc khi hàm trả về `None` thay vì giá trị tính toán.
- **Toán tử Số học (AOR) và Quan hệ (ROR):** Chỉ đạt tỷ lệ tiêu diệt khiêm tốn lần lượt là **33,33%** (10/30) và **32,89%** (42/120). Điều này chỉ ra một điểm yếu cố hữu của mã kiểm thử sinh tự động: các câu lệnh khẳng định thường chỉ kiểm tra kiểu dữ liệu tổng quát (ví dụ `isinstance(res, int)`) hoặc kiểm tra khác rỗng, mà bỏ qua việc xác minh giá trị biên (Boundary Values) và tính toán số học chính xác.
- **Toán tử Thao tác Bit (BVR):** Đạt tỷ lệ tiêu diệt **0,00%** (0/14 mutants). Toàn bộ các bộ kiểm thử đều "mù" trước các biến đổi toán tử bitwise (`&` thành `|`), cho thấy hệ thống sinh tự động không tự suy luận được các ca kiểm thử kiểm tra mặt nạ bit nếu không được chỉ dẫn tường minh.

### 4.4.2. Minh chứng Thực nghiệm về "Ảo tưởng Độ phủ" (Coverage Illusion)
Bảng 4.6 trình bày trường hợp đối lập điển hình minh chứng cho sự phân kỳ giữa độ phủ câu lệnh và năng lực Test Oracle:

@table coverage_illusion | Bảng 4.6. So sánh đối lập thực nghiệm giữa Độ phủ câu lệnh và Điểm đột biến

- Trường hợp `codetiming_timer`: Bộ kiểm thử đạt độ phủ câu lệnh lên tới **80,85%**, nhưng Điểm Đột biến chỉ đạt vỏn vẹn **20,00%** (chỉ diệt được 1/5 mutant). Phân tích mã kiểm thử cho thấy suite liên tục gọi các phương thức `start()` và `stop()` của timer nhưng các câu lệnh assertion chỉ kiểm tra `timer is not None`, hoàn toàn không kiểm tra xem thời gian đo đạc có đúng hay không.
- Trường hợp `pycg_classes`: Ngược lại, bộ kiểm thử chỉ đạt độ phủ module khiêm tốn là **41,74%**, nhưng đạt Điểm Đột biến xuất sắc **90,00%** (diệt 9/10 mutants). Các assertion trong suite này kiểm tra cực kỳ chặt chẽ cấu trúc phân cấp kế thừa và quan hệ MRO giữa các lớp.

> **Kết luận Kỹ thuật:** Độ phủ mã nguồn thuần túy là một thước đo không đầy đủ và có thể gây hiểu lầm nghiêm trọng nếu dùng làm tiêu chí duy nhất để nghiệm thu kiểm thử tự động. Việc kết hợp đo đạc Điểm Đột biến (Mutation Score) là bắt buộc để bảo đảm chất lượng phần mềm thực chất.

### 4.4.3. Giá trị ứng dụng và Khả năng Tái lập của Mô hình 14B trên thư viện genty
Song song với khảo sát lớn trên Groq 20B, nghiên cứu duy trì và kiểm chứng trọn vẹn kết quả thực nghiệm cục bộ của mô hình Qwen 14B NF4 QLoRA trên hạ tầng Kaggle Dual Tesla T4:
- Thực nghiệm trên thư viện `genty` chứng minh quy trình đạt **14 / 14 ca kiểm thử vượt qua hoàn hảo (100%)** trên cả 3 tiến trình thực thi độc lập.
- Độ phủ câu lệnh trên module `genty_args` tăng trưởng từ **18/20 dòng (90,0%) lên 20/20 dòng (100,0%)**.
- Đặc biệt, khi đưa vào 2 đột biến hành vi hậu kiểm (loại bỏ định dạng đối số vị trí và đảo thứ tự đối số từ khóa), bộ kiểm thử 14 ca của quy trình đã **tiêu diệt hoàn toàn 2/2 đột biến (100%)** bằng các lỗi `AssertionError` chính xác, trong khi bộ kiểm thử cơ sở 12 ca hoàn toàn không phát hiện được sai lệch.

## 4.5. Hiệu quả Kinh tế và Tính Khả thi Triển khai trong CI/CD

### 4.5.1. Định lượng Tiêu thụ Token và Chi phí Tài nguyên
Trong môi trường kỹ thuật phần mềm doanh nghiệp, tính khả thi của một giải pháp tự động hóa được quyết định bởi tỷ số hiệu quả / chi phí (Cost-Benefit Ratio). Bảng 4.7 và Hình 4.4 tổng hợp chi tiết mức tiêu thụ tài nguyên và chi phí trên 3 nhánh thực nghiệm:

@table economic_tradeoffs | Bảng 4.7. Tiêu thụ token, chi phí suy luận và chi phí trên mỗi bộ kiểm thử đạt chuẩn

@figure cost_token_efficiency | Hình 4.4. Đánh đổi kinh tế giữa chi phí trên mỗi bộ test đạt và sản lượng kiểm thử hoàn chỉnh

Phân tích hiệu quả kinh tế:
- Mức tiêu thụ token trung bình mỗi lượt tăng từ 1.354 token (nhánh A) lên 2.243 token (nhánh C) do việc bổ sung bao đóng ngữ cảnh AST và mẫu thiết lập.
- Chi phí suy luận trung bình mỗi lượt ở nhánh C là **$0,000293 USD** (chưa tới 0,03 cent/lượt).
- Chi phí tính trên mỗi bộ kiểm thử được chấp nhận hoàn chỉnh là **$0,311 USD/suite** ở nhánh C, so với **$0,230 USD/suite** ở nhánh A.
- Toàn bộ chiến dịch thực nghiệm 3.870 lượt chỉ tiêu tốn tổng cộng **$1,425 USD**, nằm an toàn tuyệt đối dưới trần ngân sách kiểm soát là **$3,00 USD**.

### 4.5.2. Tính khả thi trong Quy trình Tích hợp Liên tục (CI/CD Pipeline)
Với độ trễ suy luận trung bình qua phần cứng LPU đạt dưới 1,5 giây mỗi lượt sinh, kết hợp với thời gian thực thi hộp cát 3 - 5 giây, toàn bộ quy trình có thể hoàn thành việc sinh và đánh giá kiểm thử cho một module phần mềm trong vòng **dưới 10 giây**. 

Mức chi phí dưới $0,0003 USD mỗi lần chạy kiểm thử cho phép các doanh nghiệp tích hợp trực tiếp quy trình này vào cổng kiểm soát Pull Request (PR Quality Gate) trên GitHub Actions hoặc GitLab CI mà không gây áp lực đáng kể lên ngân sách vận hành hạ tầng.

## 4.6. Phân tích các Mối đe dọa đối với Tính hợp lệ (Threats to Validity)
Nghiên cứu chủ động nhận diện và phân tích 3 nhóm đe dọa chính đối với tính hợp lệ của các kết luận:
- **Tính hợp lệ bên trong (Internal Validity):**
  - Sự phụ thuộc vào hạt giống ngẫu nhiên: Quá trình sinh có thể biến thiên theo seed. Nghiên cứu đã kiểm soát yếu tố này bằng cách chạy lặp độc lập trên 2 hạt giống (seeds 71, 72) và áp dụng kiểm định hoán vị có dấu để loại bỏ phương sai ngẫu nhiên.
  - Trạng thái rò rỉ môi trường: Được triệt tiêu hoàn toàn nhờ cơ chế hộp cát tiến trình con và dọn dẹp thư mục tạm thời sau mỗi lần chạy.
- **Tính hợp lệ bên ngoài (External Validity):**
  - Khả năng khái quát hóa: Nghiên cứu khảo sát trên 21 dự án nguồn mở với 645 targets. Mặc dù đây là một tập mẫu lớn và đa dạng, các phát hiện kỹ thuật (đặc biệt là sự thất bại ở Tầng 3) cho thấy kết quả có thể không suy diễn trực tiếp cho các hệ thống phần mềm nhúng hoặc các dự án viết bằng C-extensions thuần túy.
- **Tính hợp lệ về mặt cấu trúc (Construct Validity):**
  - Thước đo độ phủ và chấp nhận: Việc định nghĩa chỉ số chấp nhận dựa trên 3 hàm kiểm thử và độ phủ câu lệnh có phạt có thể chưa phản ánh hết mọi khía cạnh chất lượng phần mềm. Để khắc phục, nghiên cứu đã bổ sung khảo sát 187 đột biến AST làm thước đo đối trọng cho Test Oracle.

## 4.7. Đề xuất Phương án Cải tiến Kỹ thuật
Từ các bài học thực nghiệm rút ra ở Chương 4, nghiên cứu đề xuất 3 phương án cải tiến kỹ thuật trọng tâm:
- **Cơ chế Lọc Ngữ cảnh Thông minh dựa trên Đồ thị Luồng Dữ liệu (DFG-based Context Slicing):** Thay vì trích xuất bao đóng cú pháp AST thuần túy (dễ gây ra hiện tượng Token Crowding ở Tầng 3), cần áp dụng kỹ thuật cắt lát chương trình (Program Slicing) dựa trên Đồ thị Luồng Dữ liệu (Data Flow Graph) để chỉ giữ lại các câu lệnh thực sự tác động tới luồng biến của hàm mục tiêu.
- **Bộ Khởi tạo Mock Tự động cho Lập trình Bất đồng bộ và I/O:** Đối với các dự án ở Tầng 2 (`tornado`, `httpie`), cần phát triển một module chuyên biệt có khả năng nhận diện các phụ thuộc socket/network và tự động tổng hợp các fixture `unittest.mock` hoặc `pytest-mock` tương ứng.
- **Tích hợp Benchmark Lỗi Thực tế (BugsInPy):** Mở rộng đánh giá từ đột biến nhân tạo sang tập lỗi thực tế trong cơ sở dữ liệu BugsInPy [24], đo lường trực tiếp tỷ lệ phát hiện lỗi hồi quy (regression bugs) trên các commit lịch sử của các dự án lớn.

# CHƯƠNG 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 5.1. Kết luận theo câu hỏi nghiên cứu
Nghiên cứu đã hoàn thành toàn diện việc xây dựng, thực nghiệm và đánh giá quy trình sinh kiểm thử tự động chuyên sâu cho ngôn ngữ Python. Dựa trên các bằng chứng thực nghiệm khách quan từ 3.870 lượt thực thi trên 21 dự án và 187 ca kiểm thử đột biến, nghiên cứu đưa ra lời giải đáp xác đáng cho 4 câu hỏi nghiên cứu:

1. **Lời giải đáp cho RQ1 (Context vs Raw Source):**
Ngữ cảnh kết hợp (AST Scope + Setup) mang lại sự cải thiện tích cực nhưng có tính phân hóa: tỷ lệ chấp nhận cân bằng dự án tăng **+1,86 pp** (*p* = 0,3464), độ phủ câu lệnh có phạt tăng từ 17,78% lên 18,95%. Quan trọng hơn, ngữ cảnh mang lại bước nhảy vọt từ **+6,5 pp đến +20,0 pp** trên nhóm dự án module hóa thuần túy (Tầng 1), khẳng định giá trị kỹ thuật thực chất của việc đóng gói ngữ cảnh khi cấu trúc phần mềm tương thích.

2. **Lời giải đáp cho RQ2 (Component Contribution):**
Khai báo phụ trợ từ AST đóng vai trò là động lực cải thiện chính (Nhánh C vượt Nhánh B **+4,94 pp**, *p* = 0,0553, thắng 13/21 dự án). Ngược lại, kỹ thuật thăm dò thiết lập đơn lẻ (Nhánh B) không tạo ra ưu thế độc lập (-3,07 pp so với mã nguồn), chứng minh rằng việc cung cấp gợi ý khởi tạo chỉ phát huy tác dụng khi đi kèm với các định nghĩa kiểu dữ liệu và phụ thuộc nội bộ từ AST.

3. **Lời giải đáp cho RQ3 (Sandbox Execution & Diagnostic Feedback):**
Hộp cát Pytest cô lập bảo đảm 100% tính an toàn hệ thống và ngăn ngừa rò rỉ trạng thái. Phân tích chẩn đoán lỗi chứng minh bao đóng ngữ cảnh giúp giảm thiểu 51 ca lỗi gọi hàm (`test_failure:call_failed`) và giảm đáng kể lỗi thu thập (`collection_failed`). Tuy nhiên, các vòng lặp sửa lỗi tự động cần được kiểm soát chặt chẽ để tránh nguy cơ làm xói mòn Test Oracle.

4. **Lời giải đáp cho RQ4 (Oracle Quality & Economic Feasibility):**
Khảo sát 187 đột biến AST vạch trần hiện tượng **"Ảo tưởng Độ phủ"**: độ phủ câu lệnh cao không đồng nghĩa với năng lực bẫy lỗi (điển hình như `codetiming_timer` đạt 80,85% coverage nhưng chỉ đạt 20,0% mutation score). Về mặt kinh tế, quy trình đạt hiệu quả chi phí xuất sắc ($0,311 USD/suite đạt chuẩn; tổng chi phí 3.870 lượt đạt $1,425 USD / trần $3,00 USD), hoàn toàn khả thi để tích hợp vào các đường ống CI/CD công nghiệp.

## 5.2. Hướng phát triển tiếp theo
Các hướng nghiên cứu và phát triển tiếp theo bao gồm:
1. Nâng cấp bộ phân tích tĩnh thành bộ phân tích kiểu lai (Hybrid Type Inference), kết hợp gợi ý kiểu AST với kỹ thuật thu thập kiểu lúc chạy (Dynamic Type Profiling).
2. Phát triển cơ chế tổng hợp Assertion dựa trên Bất biến Trạng thái (Invariant-driven Assertion Synthesis) bằng cách tích hợp công cụ Daikon để tự động tạo ra các câu lệnh `assert` kiểm tra bất biến vòng lặp và hợp đồng hàm chặt chẽ.
3. Mở rộng đánh giá trên tập benchmark lỗi phần mềm thực tế BugsInPy, hướng tới việc tự động hóa hoàn toàn quy trình sinh kiểm thử tái lập lỗi (reproducing test cases) trong bảo trì phần mềm.

# TÀI LIỆU THAM KHẢO

[1] C. Wohlin, P. Runeson, M. Höst, M. C. Ohlsson, B. Regnell, và A. Wesslén, *Experimentation in Software Engineering*. Springer Science & Business Media, 2012.

[2] P. McMinn, “Search-based software test data generation: a survey: Research Articles,” *Software Testing, Verification and Reliability*, vol. 14, no. 2, pp. 105–156, 2004.

[3] M. Lukasczyk, F. Kroiß, và G. Fraser, “Automated Unit Test Generation for Python,” trong *Proceedings of the 14th ACM International Conference on Systems and Software Product Line*, 2020.

[4] S. Shamshiri et al., “Do automatically generated unit test suites detect real faults? A large-scale empirical study,” trong *2015 IEEE 8th International Conference on Software Testing, Verification and Validation (ICST)*, 2015.

[5] G. Fraser và A. Arcuri, “EvoSuite: automatic test suite generation for object-oriented software,” trong *Proceedings of the 19th ACM SIGSOFT symposium and the 13th European conference on Foundations of software engineering*, 2011, pp. 416–419.

[6] C. Pacheco, S. K. Lahiri, M. D. Ernst, và T. Ball, “Feedback-directed random test generation,” trong *33rd International Conference on Software Engineering (ICSE)*, 2007.

[7] Y. Jia và M. Harman, “An analysis and survey of the development of mutation testing,” *IEEE transactions on software engineering*, vol. 37, no. 5, pp. 649–678, 2010.

[8] R. Just, D. Jalali, L. Inozemtseva, M. D. Ernst, R. Holmes, và G. Fraser, “Are mutants a valid substitute for real faults in software testing?,” trong *Proceedings of the 22nd ACM SIGSOFT International Symposium on Foundations of Software Engineering*, 2014, pp. 654–665.

[9] L. Inozemtseva và R. Holmes, “Coverage is not strongly correlated with test suite effectiveness,” trong *Proceedings of the 36th International Conference on Software Engineering*, 2014, pp. 435–446.

[10] E. T. Barr, M. Harman, P. McMinn, M. Shahbaz, và S. Yoo, “The oracle problem in software testing: A survey,” *IEEE transactions on software engineering*, vol. 41, no. 5, pp. 507–525, 2014.

[11] M. Chen et al., “Evaluating Large Language Models Trained on Code,” *arXiv preprint arXiv:2107.03374*, 2021.

[12] C. Lemieux, J. P. Inala, S. K. Lahiri, và S. Sen, “CODA-MOSA: Escaping coverage plateaus in test generation with pre-trained large language models,” trong *2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE)*, 2023, pp. 919–931.

[13] Z. Yuan et al., “No More Manual Tests? Evaluating and Improving ChatGPT for Unit Test Generation,” *arXiv preprint arXiv:2305.04207*, 2023.

[14] M. Schäfer, S. Nadi, A. Eghbali, và F. Tip, “An empirical evaluation of using large language models for automated unit test generation,” *IEEE Transactions on Software Engineering*, 2023.

[15] J. Bradbury, J. R. Cordy, J. Dingel, và M. Wermelinger, “A survey of mutation testing for concurrent software,” *Software Testing, Verification and Reliability*, 2006.

[16] B. Marick, *The Craft of Software Testing: Subsystem Testing Including Object-based and Object-oriented Testing*. Prentice-Hall, Inc., 1995.

[17] M. Harman và B. F. Jones, “Search-based software engineering,” *Information and Software Technology*, vol. 43, no. 14, pp. 833–839, 2001.

[18] S. Holm, “A simple sequentially rejective multiple test procedure,” *Scandinavian journal of statistics*, pp. 65–70, 1979.

[19] R. A. Fisher, *The design of experiments*. Oliver and Boyd, Edinburgh, 1935.

[20] B. Efron và R. J. Tibshirani, *An introduction to the bootstrap*. CRC press, 1994.

[21] J. Cohen, *Statistical power analysis for the behavioral sciences*. Academic press, 2013.

[22] A. Vargha và H. D. Delaney, “A critique and modification of the Common Language Effect Size statistics of McGraw and Wong,” *Journal of Educational and Behavioral Statistics*, vol. 25, no. 2, pp. 101–132, 2000.

[23] F. Wilcoxon, “Individual comparisons by ranking methods,” *Biometrics bulletin*, vol. 1, no. 6, pp. 80–83, 1945.

[24] R. Mukherjee et al., “BugsInPy: A Database of Existing Bugs in Python Programs to Enable Controlled Testing and Debugging Studies,” trong *Proceedings of the 28th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE)*, 2020.

# PHỤ LỤC 1. QUY CÁCH CHỈ THỊ KIỂM THỬ VÀ BẢNG THUẬT NGỮ CHUYÊN NGÀNH

## PL1.1. Quy cách Kỹ thuật Chỉ thị Sinh Kiểm thử Đơn vị Pytest
```text
=== QUY CÁCH KỸ THUẬT CHỈ THỊ SINH KIỂM THỬ TỰ ĐỘNG (PYTEST SPECIFICATION) ===

[ĐỐI TƯỢNG MỤC TIÊU CẦN KIỂM THỬ]:
{target_source_code}

[BAO ĐÓNG NGỮ CẢNH PHỤ TRỢ (AST SCOPE CLOSURE)]:
{ast_context_closure}

[MẪU THIẾT LẬP ĐÃ XÁC NHẬN (VERIFIED SETUP TEMPLATE)]:
{verified_setup_pattern}

[CÁC RÀNG BUỘC KỸ THUẬT BẮT BUỘC]:
1. Xuất ra module kiểm thử Python hoàn chỉnh, độc lập và tương thích hoàn toàn với pytest.
2. Định nghĩa đúng 3 hàm kiểm thử cấp module: kiểm thử trường hợp thông thường, trường hợp biên, và trường hợp xử lý ngoại lệ.
3. Kích hoạt trực tiếp vào thân hàm/phương thức của đối tượng mục tiêu.
4. Chứa các câu lệnh assertion ngữ nghĩa chặt chẽ (kiểm tra giá trị trả về, trạng thái đột biến); tuyệt đối không dùng assertion rỗng hoặc kiểm tra nông.
```

## PL1.2. Bảng Quy ước Thuật ngữ Chuyên ngành Kỹ thuật Phần mềm
- **Unit Test (Kiểm thử đơn vị):** Kiểm thử mức thấp nhất nhằm xác minh tính đúng đắn của từng hàm, phương thức hoặc lớp riêng lẻ.
- **Test Oracle (Cơ sở phán quyết kiểm thử):** Cơ chế xác định xem kết quả thực thi của một ca kiểm thử là đạt (Pass) hay không đạt (Fail).
- **Abstract Syntax Tree - AST (Cây cú pháp trừu tượng):** Cấu trúc cây biểu diễn ngữ pháp của mã nguồn chương trình.
- **Coverage Illusion (Ảo tưởng độ phủ):** Hiện tượng bộ kiểm thử đạt độ phủ dòng cao nhưng không có năng lực bẫy lỗi do thiếu các assertion chặt chẽ.
- **Mutation Score (Điểm đột biến):** Tỷ lệ phần trăm giữa số lượng đột biến bị tiêu diệt so với tổng số đột biến nhân tạo hợp lệ.
- **Quality Gate (Cổng kiểm soát chất lượng):** Bước kiểm tra tự động các tiêu chí tối thiểu (cú pháp, số lượng hàm) trước khi chấp nhận chuyển sang bước thực thi.

# PHỤ LỤC 2. KẾT QUẢ CHI TIẾT THEO DỰ ÁN VÀ CẤU HÌNH

Bảng PL2.1 tổng hợp số liệu thực nghiệm chi tiết của toàn bộ 21 dự án qua 3 nhánh thực nghiệm:

@table appendix_projects | Bảng PL2.1. Phân bố chi tiết kết quả 21 dự án qua 3 nhánh thực nghiệm

# PHỤ LỤC 3. PHẠM VI BẰNG CHỨNG VÀ TÁI LẬP

## PL3.1. Danh mục Băm Mã hóa SHA-256 các Tệp Chứng cứ Cốt lõi
- Tập tin thực nghiệm toàn phạm vi: `research/groq_full_scope_20261119/summary.json`
- Bảng tổng hợp thống kê: `research/groq_full_scope_20261119/statistics.json`
- Gói kiểm chứng tái lập: `deliverables/council_repro_20261119_v4.zip`
- Mã nguồn xây dựng báo cáo v17: `scripts/build_v17_master_monograph.py`
- Báo cáo đặc tả thay đổi: `reports/Tieu_Luan_CNPMTT_Council_SOTA_v17.changes.md`

# PHỤ LỤC 4. KHẢO SÁT PHÁT TRIỂN VÀ PHÂN TÍCH HẬU KIỂM

Khảo sát phát triển trên 105 lượt chạy có cơ chế phản hồi sửa lỗi 2 vòng lặp (với mô hình 14B và các đợt chạy thử nghiệm) cho thấy:
- Vòng sinh đầu tiên đạt 42 ca thành công.
- Vòng sửa lỗi thứ nhất (sử dụng Traceback chẩn đoán) cứu vãn thành công thêm 21 ca.
- Vòng sửa lỗi thứ hai cứu vãn thêm 6 ca.
- Tổng số ca chấp nhận sau sửa chữa tăng từ 42 lên 69 ca (tăng 64,3% so với lần sinh đầu).
Tuy nhiên, việc sửa chữa lặp cần được giám sát chặt chẽ bởi kiểm thử đột biến để bảo đảm các khẳng định kiểm tra không bị nới lỏng qua các vòng sửa.
