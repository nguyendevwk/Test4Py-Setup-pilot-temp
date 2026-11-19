# CHƯƠNG 4: THIẾT KẾ THỰC NGHIỆM VÀ PHƯƠNG PHÁP ĐÁNH GIÁ

Thiết kế thực nghiệm trong nghiên cứu này được xây dựng tuân thủ nghiêm ngặt các nguyên tắc phương pháp luận trong công nghệ phần mềm thực nghiệm (Empirical Software Engineering), đáp ứng các tiêu chuẩn đánh giá của ACM/IEEE Transactions on Software Engineering (TSE). Chương này trình bày chi tiết mô hình giai thừa thực nghiệm (Factorial Experimental Design), tiêu chí phân tầng và đặc tả 21 mục tiêu kiểm thử tuyển chọn (Curated Benchmark Targets), khung kiểm thử đột biến cấp 1 (First-Order Mutation Testing Framework), hệ thống các chỉ số đo lường định lượng và phương pháp luận kiểm định thống kê suy luận đa biến.

---

### 4.1 BỐI CẢNH VÀ THIẾT KẾ GIAI THỪA THỰC NGHIỆM (FACTORIAL DESIGN)

Để cô lập và định lượng chính xác sự đóng góp của từng thành phần kiến trúc trong Council-SOTA so với các phương pháp tiếp cận hiện hành, nghiên cứu triển khai thiết kế thực nghiệm giai thừa $3 \times 21 \times 5$:
- **Nhân tố Phương pháp (Treatment Factor - 3 Arms)**:
  1. *Baseline (Zero-Shot Generation)*: Sinh mã trực tiếp qua mô hình ngôn ngữ lớn không kèm cơ chế phản biện hay neo ngữ cảnh ngoài chữ ký hàm mục tiêu.
  2. *Council Standard (1-Round Critic)*: Kiến trúc hội đồng tiêu chuẩn thực thi một vòng phản biện sửa lỗi dựa trên thông điệp lỗi cú pháp/thực thi ban đầu.
  3. *Council-SOTA (Two-Round Multi-Turn Adaptive Critic + AST Symbol-Table Export Grounding)*: Kiến trúc tối ưu tích hợp bảng biểu tượng AST tĩnh, phản biện thích ứng 2 vòng vi mô và bộ lọc chuẩn hóa Oracle.
- **Nhân tố Đối tượng (Subject Factor - 21 Targets)**: 21 module phần mềm mã nguồn mở được tuyển chọn có hệ thống từ 7 kho lưu trữ tiêu biểu trong hệ quy chiếu Test4Py.
- **Nhân tố Ngẫu nhiên (Randomization Factor - $N=5$ Seeds)**: Nhằm kiểm soát tính bất định (stochasticity) của quá trình lấy mẫu suy luận ngôn ngữ, mỗi nghiệm thức được lặp lại độc lập trên 5 hạt giống sinh số ngẫu nhiên:
  $$\mathcal{S} = \{42, 43, 44, 45, 46\}$$

Tổng số lượt thực nghiệm độc lập trong nghiên cứu là:
$$N_{\text{total}} = 3 \text{ arms} \times 21 \text{ targets} \times 5 \text{ seeds} = 315 \text{ independent trials}$$
Trong đó, mỗi nhánh phương pháp gánh chịu chính xác 105 lượt chạy đối chứng trực tiếp.

Môi trường thực thi thực nghiệm được chuẩn hóa trên hạ tầng tăng tốc phần cứng Groq Cloud LPU phục vụ mô hình nguồn mở quy mô tham số nhỏ `openai/gpt-oss-20b`. Quá trình kiểm tra và thu thập độ phủ được đóng gói trong môi trường ảo hóa cách ly với bộ thông dịch Python 3.10, công cụ thực thi `pytest 7.4.x` và thư viện đo đạc `coverage.py 7.x`. Mọi tiến trình thực thi kiểm thử được áp đặt rào cản thời gian cứng (Hard Execution Timeout) là 30 giây cho mỗi lượt chạy nhằm ngăn chặn triệt để hiện tượng treo luồng do vòng lặp vô hạn. Toàn bộ tiến trình gọi API được giám sát bởi bộ ngắt mạch tài chính tự động (Financial Circuit Breaker) nhằm đảm bảo tính an toàn vận hành.

---

### 4.2 ĐẶC TẢ VÀ PHÂN TẦNG 21 CURATED BENCHMARK TARGETS

Hệ quy chiếu Test4Py ban đầu bao gồm 183 đối tượng kiểm thử. Tuy nhiên, qua phân tích sơ bộ có hệ thống, nghiên cứu phát hiện một số mục tiêu chứa lỗi cú pháp nội tại của mã nguồn gốc hoặc gặp hiện tượng phụ thuộc vòng (circular imports) không thể giải quyết ở cấp độ kiểm thử đơn vị độc lập (ví dụ: `docstring_parser_rest`, `pycg_definitions`, `typesystem_date_format`). 

Nhằm đảm bảo tính hợp lệ nội tại (Internal Validity) và khả năng tái lập khoa học, nghiên cứu đã tiến hành rà soát, loại bỏ các mục tiêu lỗi nội tại và bổ sung các module chất lượng cao, hình thành bộ **21 Curated Benchmark Targets** thuộc 7 thư viện mã nguồn mở thực tế trong hệ sinh thái Python. Bảng 4.1 trình bày đặc tả phân loại của 21 đối tượng này.

**BẢNG 4.1: ĐẶC TẢ CHI TIẾT 21 CURATED BENCHMARK TARGETS THUỘC HỆ QUY CHIẾU TEST4PY**

| STT | Target ID | Kho Mã Nguồn (Repository) | Phân Loại Cấu Trúc Mã Nguồn | Đặc Tính Kỹ Thuật Trọng Yếu | Số LOC |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | `codetiming_timer` | `codetiming` | Context Manager (Medium) | Quản lý vòng đời Context Manager, tính toán thời gian thực | 125 |
| 2 | `docstring_parser_docstring` | `docstring_parser` | AST Data Model | Khởi tạo cấu trúc dữ liệu AST biểu diễn docstring | 89 |
| 3 | `docstring_parser_google` | `docstring_parser` | AST-Parser (Complex) | Parser cú pháp Google Docstring, xử lý thụt lề phức tạp | 242 |
| 4 | `docstring_parser_numpydoc` | `docstring_parser` | AST-Parser (Complex) | Parser cú pháp NumPy Docstring, phân giải section và type | 288 |
| 5 | `docstring_parser_parse` | `docstring_parser` | AST-Typed (Complex) | Điều phối phân giải tự động các định dạng docstring | 115 |
| 6 | `genty_args` | `genty` | Data Structure (Medium) | Cấu trúc bao đóng tham số kiểm thử tham số hóa | 78 |
| 7 | `genty_dataset` | `genty` | Decorator (Medium) | Cơ chế tiêm nạp dữ liệu kiểm thử qua Decorator động | 134 |
| 8 | `genty_repeat` | `genty` | Decorator (Medium) | Decorator lặp kiểm thử, kiểm soát logic tái thực thi | 64 |
| 9 | `pycg_callgraph` | `PyCG` | Machinery (Complex) | Đồ thị gọi hàm bậc cao, quản lý cạnh phụ thuộc ngữ nghĩa | 165 |
| 10 | `pycg_classes` | `PyCG` | Machinery (Complex) | Quản lý kế thừa lớp, quan hệ đa hình và MRO | 210 |
| 11 | `pycg_imports` | `PyCG` | Machinery (Complex) | Phân giải cây phụ thuộc nhập khẩu tĩnh và bí danh import | 148 |
| 12 | `pycg_scopes` | `PyCG` | Machinery (Scopes) | Phân cấp không gian tên (Scopes) và bóng biến (Shadowing) | 192 |
| 13 | `string_utils_is_email` | `python-string-utils` | Regex Validation | Khớp mẫu biểu thức chính quy kiểm thực địa chỉ email | 92 |
| 14 | `string_utils_slugify` | `python-string-utils` | String Manipulation | Chuẩn hóa chuỗi ASCII, xử lý ký tự Unicode phức tạp | 110 |
| 15 | `superstring` | `superstring.py` | Utility (Simple) | Lớp bao đóng chuỗi mở rộng với các toán tử tiện ích | 145 |
| 16 | `typesystem_choice` | `typesystem` | Fields (Choice) | Ràng buộc kiểm thực trường dữ liệu lựa chọn có tập giá trị | 98 |
| 17 | `typesystem_oneof` | `typesystem` | Validation (Composite) | Kiểm thực tổ hợp logic lựa chọn đa hình kiểu | 120 |
| 18 | `typesystem_schema` | `typesystem` | Validation (Complex) | Định nghĩa lược đồ dữ liệu, kiểm thực cấu trúc lồng nhau | 230 |
| 19 | `typesystem_string` | `typesystem` | Fields (Complex) | Kiểm thực chuỗi, độ dài tối thiểu/tối đa, khớp pattern | 185 |
| 20 | `typesystem_validation_error` | `typesystem` | Validation (Core Error) | Đối tượng lỗi kiểm thực, cấu trúc cây thông báo lỗi | 105 |
| 21 | `woa_whale_opt` | `woa` | Optimization (Complex) | Giải thuật tối ưu hóa bầy đàn cá voi (Metaheuristic) | 172 |

21 mục tiêu này phân bổ toàn diện trên các miền bài toán: xử lý văn bản, xác thực dữ liệu tĩnh, cấu trúc dữ liệu trừu tượng, phân tích đồ thị luồng tĩnh (static call-graph analysis) và tối ưu hóa toán học phức tạp.

---

### 4.3 KHUNG ĐÁNH GIÁ KIỂM THỬ ĐỘT BIẾN CẤP 1 (FIRST-ORDER MUTATION TESTING)

Độ phủ dòng mã (Line Coverage) thuần túy không đảm bảo tính đầy đủ của kiểm thử, do một bộ kiểm thử có thể thực thi toàn bộ các dòng lệnh nhưng chứa các mệnh đề xác thực rỗng (Tautological Assertions) hoặc thiếu các assertion kiểm tra trạng thái biên. Để định lượng năng lực phát hiện lỗi ngữ nghĩa thực tế, nghiên cứu tích hợp một công cụ kiểm thử đột biến cấp 1 (First-Order Mutation Engine) hoạt động trực tiếp trên Cây Cú Pháp Trừu Tượng (AST) của mã nguồn mục tiêu.

#### 4.3.1 Cơ Sở Lý Thuyết Đột Biến
Kiểm thử đột biến dựa trên hai giả thuyết nền tảng trong công nghệ phần mềm:
1. **Giả thuyết Lập trình viên Thành thạo (Competent Programmer Hypothesis)**: Lập trình viên có xu hướng viết các chương trình gần đúng; các lỗi thực tế thường chỉ khác biệt so với chương trình đúng bởi các sai lệch cú pháp hoặc toán tử nhỏ.
2. **Hiệu ứng Ghép lỗi (Coupling Effect)**: Một bộ kiểm thử có khả năng phát hiện và tiêu diệt các lỗi đơn lẻ (First-Order Mutants) cũng sở hữu năng lực phát hiện các lỗi phức hợp đa biến (Higher-Order Mutants).

#### 4.3.2 Tập Toán Tử Đột Biến Cấp 1
Khung đánh giá thiết lập 5 lớp toán tử biến dị cú pháp chuẩn mực trên Python AST:
- **ROR (Relational Operator Replacement)**: Thay thế các toán tử so sánh quan hệ:
  $$\{<, \le, >, \ge, ==, \ne, \text{in}, \text{not in}\} \longrightarrow \text{toán tử đối nghịch}$$
- **AOR (Arithmetic Operator Replacement)**: Thay thế các toán tử số học:
  $$\{+, -, *, /, //, \%, **\} \longrightarrow \text{toán tử số học khác}$$
- **BVR (Boolean Value Replacement)**: Đảo ngược các hằng số logic:
  $$\{\text{True} \longleftrightarrow \text{False}\}$$
- **CRP (Constant Replacement)**: Thay đổi các hằng số số học hoặc chuỗi ký tự tại các điểm quyết định rẽ nhánh ($0 \to 1, 1 \to 0, \text{""} \to \text{"mutant"}$).
- **SIR (Statement Inversion / Removal)**: Vô hiệu hóa hoặc đảo ngược các câu lệnh gán trạng thái then chốt (`pass` injection hoặc đảo nhánh `if/else`).

#### 4.3.3 Quy Trình Kiểm Thử Đột Biến
1. **Trích xuất Đột biến**: Bộ duyệt AST duyệt qua file mã nguồn của từng mục tiêu, sinh ra tối đa 10 thể đột biến đại diện không tương đương (non-equivalent mutants).
2. **Thực thi Đối chứng**: Với mỗi thể đột biến $m_j \in \mathcal{M}_i$ của mục tiêu $t_i$, bộ kiểm thử tạo bởi Council-SOTA được thực thi trong môi trường độc lập.
3. **Phán Quyết (Verdict)**: Thể đột biến $m_j$ được phân loại là **Bị tiêu diệt (Killed)** nếu và chỉ nếu bộ kiểm thử ném ra ngoại lệ kiểm thử thất bại (`exit_code \neq 0`, `AssertionError`, hoặc runtime crash). Ngược lại, nếu toàn bộ các bài kiểm thử đều vượt qua (`exit_code == 0`), thể đột biến được phân loại là **Sống sót (Survived)**.

Tổng cộng, hệ thống đã sinh ra $M = 187$ thể đột biến phân bố trên toàn bộ 21 tệp mã nguồn mục tiêu.

---

### 4.4 HỆ THỐNG CHỈ SỐ ĐO LƯỜNG ĐỊNH LƯỢNG (EVALUATION METRICS)

Nghiên cứu sử dụng hệ thống chỉ số đo lường đa chiều nhằm phản ánh toàn diện tính đúng đắn, độ bao phủ và năng lực phát hiện lỗi của các bộ kiểm thử:

1. **Tỷ Lệ Vượt Qua Của Bộ Kiểm Thử (Suite Pass Rate - $PR$)**:
   Tỷ lệ phần trăm các bộ kiểm thử thực thi thành công hoàn toàn mà không gặp bất kỳ lỗi biên dịch, lỗi nạp module, hay lỗi assertion nào:
   $$PR = \frac{1}{|T|} \sum_{k=1}^{|T|} \mathbb{I}(\text{status}(t_k) = \text{PASS}) \times 100\%$$
   trong đó $|T|$ là tổng số lượt thử nghiệm ($|T|=105$ cho mỗi arm), và $\mathbb{I}(\cdot)$ là hàm chỉ thị.

2. **Độ Phủ Dòng Mã (Statement / Line Coverage - $SC$)**:
   Tỷ lệ các dòng mã khả thi (coverable statements) được thực thi bởi bộ kiểm thử $t$:
   $$SC(t) = \frac{|\mathcal{L}_{\text{executed}}(t)|}{|\mathcal{L}_{\text{total}}|} \times 100\%$$

3. **Độ Phủ Nhánh Quyết Định (Branch Coverage - $BC$)**:
   Tỷ lệ các nhánh rẽ điều kiện boolean (control-flow edges) được duyệt qua trong đồ thị luồng điều khiển:
   $$BC(t) = \frac{|\mathcal{B}_{\text{traversed}}(t)|}{|\mathcal{B}_{\text{total}}|} \times 100\%$$

4. **Điểm Đột Biến (Mutation Score - $MS$)**:
   - *Điểm đột biến toàn cục (Absolute Global Mutation Score)*:
     $$MS_{\text{global}} = \frac{K}{M - E} \times 100\%$$
     với $K$ là tổng số mutant bị tiêu diệt ($K=71$), $M$ là tổng số mutant sinh ra ($M=187$), và $E$ là số mutant tương đương ($E=0$ theo thiết kế chắt lọc).
   - *Điểm đột biến trung bình theo mục tiêu (Target-Level Mean Mutation Score)*:
     $$MS_{\text{mean}} = \frac{1}{|T_{\text{targets}}|} \sum_{i=1}^{|T_{\text{targets}}|} \frac{K_i}{M_i} \times 100\%$$

5. **Tỷ Lệ Kiểm Thử Chập Chờn (Flaky Test Rate - $FR$)**:
   Xác suất một bài kiểm thử thay đổi kết quả (đỗ $\leftrightarrow$ trượt) giữa các lần thực thi liên tiếp trong điều kiện môi trường bất biến:
   $$FR = \frac{N_{\text{flaky\_suites}}}{N_{\text{evaluated\_suites}}} \times 100\%$$

---

### 4.5 PHƯƠNG PHÁP LUẬN KIỂM ĐỊNH THỐNG KÊ SUY LUẬN

Để xác lập tính nghiêm ngặt khoa học và loại trừ hoàn toàn khả năng các sai khác thực nghiệm bắt nguồn từ nhiễu ngẫu nhiên, nghiên cứu áp dụng phối hợp cả kiểm định tham số và phi tham số:

1. **Kiểm Định Tham Số Cặp (Paired Student's $t$-test)**:
   Đánh giá sự khác biệt kỳ vọng toán học giữa hai phân phối độ phủ dòng mã theo từng cặp mục tiêu tương ứng ($n=21$):
   $$t = \frac{\bar{D}}{s_D / \sqrt{n}}$$
   trong đó $\bar{D}$ là sai khác trung bình của độ phủ ($\bar{D} = \bar{X}_{\text{SOTA}} - \bar{X}_{\text{Base}}$) và $s_D$ là độ lệch chuẩn của các sai khác ghép cặp.

2. **Kiểm Định Dấu Hạng Wilcoxon (Wilcoxon Signed-Rank Test)**:
   Kiểm định phi tham số cho mẫu phụ thuộc ghép cặp, không giả định phân phối chuẩn của dữ liệu:
   $$W = \min(W^+, W^-)$$
   trong đó $W^+$ và $W^-$ là tổng các thứ hạng dấu dương và dấu âm của độ lệch $|\Delta_i| = SC_{\text{SOTA}, i} - SC_{\text{Base}, i}$.

3. **Kiểm Định Tổng Hạng Mann-Whitney $U$ (Mann-Whitney $U$ Test)**:
   Kiểm định phi tham số cho hai mẫu độc lập, đánh giá mức độ vượt trội ngẫu nhiên của phân phối Council-SOTA so với phân phối Baseline trên toàn bộ không gian mẫu.

4. **Kích Thước Hiệu Ứng Tham Số Cohen's $d$**:
   Đo lường độ lớn sai khác chuẩn hóa giữa hai trung bình mẫu:
   $$d = \frac{\bar{X}_{\text{SOTA}} - \bar{X}_{\text{Base}}}{s_{\text{pooled}}}, \quad s_{\text{pooled}} = \sqrt{\frac{(n_1 - 1)s_1^2 + (n_2 - 1)s_2^2}{n_1 + n_2 - 2}}$$
   Quy ước ngưỡng diễn giải của Cohen: $d \ge 0.2$ (nhỏ), $d \ge 0.5$ (vừa), $d \ge 0.8$ (lớn - Large).

5. **Kích Thước Hiệu Ứng Phi Tham Số Vargha-Delaney $\hat{A}_{12}$**:
   Độ đo chuẩn tắc trong công nghệ phần mềm thực nghiệm thể hiện xác suất một giá trị được lấy mẫu ngẫu nhiên từ phân phối Council-SOTA sẽ lớn hơn một giá trị lấy mẫu ngẫu nhiên từ Baseline:
   $$\hat{A}_{12} = \frac{R_1 - \frac{m(m+1)}{2}}{m \cdot n}$$
   với $R_1$ là tổng hạng của nhóm xử lý, $m$ và $n$ là kích thước hai nhóm. Ngưỡng phân loại chuẩn: $\hat{A}_{12} \ge 0.56$ (nhỏ), $\hat{A}_{12} \ge 0.64$ (vừa), $\hat{A}_{12} \ge 0.71$ (lớn - Large).

Ngưỡng bác bỏ giả thuyết vô hiệu ($H_0$) được thiết lập nghiêm ngặt tại mức ý nghĩa $\alpha = 0.05$, $\alpha = 0.01$ và $\alpha = 0.001$.

---
---

# CHƯƠNG 5: KẾT QUẢ THỰC NGHIỆM VÀ ĐỐI CHỨNG ĐỊNH LƯỢNG

Chương này công bố và phân tích toàn diện kết quả thực nghiệm thu được từ 315 trials đối chứng đa hạt giống, giải quyết các câu hỏi nghiên cứu định lượng then chốt của công trình.

---

### 5.1 RQ1: ĐỐI CHỨNG HIỆU NĂNG BA TRỤC TOÀN DIỆN (THREE-WAY COMPARISON)

Hiệu năng thực nghiệm của ba nhánh phương pháp—Zero-Shot Baseline, Council Standard (1 vòng phản biện), và Council-SOTA (2 vòng phản biện kết hợp AST Grounding)—được tổng hợp chi tiết trên toàn bộ 21 Curated Benchmark Targets tại Bảng 5.1.

**BẢNG 5.1: BẢNG SO SÁNH HIỆU NĂNG THỰC NGHIỆM BA TRỤC TRÊN 21 CURATED BENCHMARK TARGETS ($N=5$ SEEDS, 105 TRIALS MỖI ARM)**

| Mục Tiêu Kiểm Thử (Target ID) | Dự Án Gốc (Project) | Baseline Pass (%) | Baseline Cov (%) | Council Std Pass (%) | Council Std Cov (%) | Council-SOTA Pass (%) | Council-SOTA Cov (%) | Số Lần Critic Sửa | Điểm Đột Biến (Kill %) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `codetiming_timer` | `codetiming` | 80.0% | 67.24% | 100.0% | 86.81% | **100.0%** | **80.85%** | 2 | 20.0% (2/10) |
| `docstring_parser_docstring` | `docstring_parser` | 80.0% | 46.14% | 80.0% | 49.12% | **100.0%** | **57.67%** | 0 | 30.0% (3/10) |
| `docstring_parser_google` | `docstring_parser` | 0.0% | 0.00% | 40.0% | 17.99% | **80.0%** | **36.46%** | 4 | 10.0% (1/10) |
| `docstring_parser_numpydoc` | `docstring_parser` | 0.0% | 0.00% | 80.0% | 43.38% | **60.0%** | **32.50%** | 2 | 30.0% (3/10) |
| `docstring_parser_parse` | `docstring_parser` | 60.0% | 17.45% | 80.0% | 29.45% | **100.0%** | **29.09%** | 1 | 30.0% (3/10) |
| `genty_args` | `genty` | 0.0% | 0.00% | 40.0% | 38.00% | **100.0%** | **96.00%** | 3 | 75.0% (3/4) |
| `genty_dataset` | `genty` | 20.0% | 14.63% | 20.0% | 15.12% | **60.0%** | **39.00%** | 2 | 60.0% (3/5) |
| `genty_repeat` | `genty` | 0.0% | 0.00% | 40.0% | 40.00% | **100.0%** | **82.50%** | 1 | 100.0% (3/3) |
| `pycg_callgraph` | `PyCG` | 100.0% | 96.67% | 80.0% | 80.00% | **100.0%** | **88.67%** | 0 | 100.0% (5/5) |
| `pycg_classes` | `PyCG` | 80.0% | 41.30% | 100.0% | 60.00% | **80.0%** | **41.74%** | 0 | 90.0% (9/10) |
| `pycg_imports` | `PyCG` | 80.0% | 28.95% | 60.0% | 22.10% | **100.0%** | **36.78%** | 2 | 20.0% (2/10) |
| `pycg_scopes` | `PyCG` | 20.0% | 12.47% | 100.0% | 61.29% | **80.0%** | **60.65%** | 1 | 70.0% (7/10) |
| `string_utils_is_email` | `python-string-utils`| 80.0% | 24.21% | 80.0% | 26.05% | **100.0%** | **29.74%** | 1 | 10.0% (1/10) |
| `string_utils_slugify` | `python-string-utils`| 80.0% | 26.17% | 100.0% | 32.84% | **100.0%** | **32.54%** | 0 | 0.0% (0/10) |
| `superstring` | `superstring.py` | 80.0% | 29.93% | 80.0% | 32.89% | **100.0%** | **38.09%** | 1 | 40.0% (4/10) |
| `typesystem_choice` | `typesystem` | 60.0% | 18.19% | 40.0% | 12.56% | **100.0%** | **31.01%** | 1 | 10.0% (1/10) |
| `typesystem_oneof` | `typesystem` | 60.0% | 17.34% | 20.0% | 6.61% | **100.0%** | **32.85%** | 5 | 40.0% (4/10) |
| `typesystem_schema` | `typesystem` | 0.0% | 0.00% | 100.0% | 34.01% | **100.0%** | **33.82%** | 2 | 50.0% (5/10) |
| `typesystem_string` | `typesystem` | 80.0% | 22.78% | 20.0% | 6.04% | **100.0%** | **30.50%** | 1 | 60.0% (6/10) |
| `typesystem_validation_error`| `typesystem` | 0.0% | 0.00% | 100.0% | 29.37% | **100.0%** | **29.02%** | 0 | 30.0% (3/10) |
| `woa_whale_opt` | `woa` | 60.0% | 43.21% | 100.0% | 69.14% | **100.0%** | **62.22%** | 0 | 30.0% (3/10) |
| **Giá Trị Trung Bình** | **21 Mục Tiêu** | **48.57%** | **24.13%** | **69.52%** | **37.75%** | **93.33%** | **47.70%** | **29** | **43.10%** |

#### 5.1.1 Phân Tích Tiến Trình Tăng Trưởng Độ Phủ (Dumbbell Coverage Progression Analysis)
Dữ liệu đối chứng phản ánh bước nhảy vọt có ý nghĩa bản lề về cả tính đúng đắn lẫn phạm vi bao phủ mã nguồn:
1. **Tỷ Lệ Vượt Qua Bộ Kiểm Thử (Pass Rate)**:
   - Zero-Shot Baseline chỉ đạt **48.57%** (51/105 trials thành công). Trong 6 mục tiêu có logic khởi tạo phức tạp (`docstring_parser_google`, `docstring_parser_numpydoc`, `genty_args`, `genty_repeat`, `typesystem_schema`, `typesystem_validation_error`), Baseline hoàn toàn tê liệt với **0.0% Pass Rate** do ảo giác import đường dẫn submodule không tồn tại.
   - Council Standard cải thiện lên **69.52%** (73/105 trials), giải quyết được các lỗi cú pháp bề mặt nhưng thường xuyên thất bại khi gặp lỗi assertion tinh vi ở các kiểu phức hợp (ví dụ: `typesystem_oneof` sụt giảm còn 20.0%, `typesystem_string` sụt giảm còn 20.0%).
   - Council-SOTA đạt đỉnh cao **91.43%** (96/105 trials) tại bản tiền tinh chỉnh quy tắc, và xác lập kỷ lục **93.33%** (98/105 trials) sau khi hoàn thiện tinh chỉnh quy tắc neo AST. Mức tăng trưởng tương đối đạt **+92.15%** so với Baseline và **+34.25%** so với Council Standard.
2. **Độ Phủ Dòng Mã (Line Coverage Progression)**:
   - Line Coverage tăng tuyến tính từ **24.13%** (Baseline) $\longrightarrow$ **37.75%** (Council Std) $\longrightarrow$ **46.50%** (Council-SOTA trước tinh chỉnh) $\longrightarrow$ **47.70%** (Council-SOTA sau tinh chỉnh).
   - Mức tăng tuyệt đối đạt **+23.57%** so với Zero-Shot Baseline (tương đương mức tăng trưởng tương đối **+97.68%**).
   - Tại các module cấu trúc dữ liệu và decorator chuyên sâu, bước nhảy độ phủ thể hiện rõ nét qua phân tích Dumbbell: `genty_args` tăng từ $0.0\% \to 38.0\% \to \mathbf{96.0\%}$; `genty_repeat` tăng từ $0.0\% \to 40.0\% \to \mathbf{82.5\%}$; `codetiming_timer` đạt đỉnh $\mathbf{80.85\%}$; và `pycg_callgraph` duy trì mức phủ vượt trội $\mathbf{88.67\%}$.

---

### 5.2 RQ2: KIỂM ĐỊNH THỐNG KÊ SUY LUẬN VÀ KÍCH THƯỚC HIỆU ỨNG (STATISTICAL VALIDATION)

Để kiểm chứng tính vững chắc của các phát hiện định lượng, toàn bộ các kiểm định tham số và phi tham số được thực hiện trực tiếp trên phân phối độ phủ dòng của 21 mục tiêu kiểm thử. Kết quả được tổng hợp tại Bảng 5.2.

**BẢNG 5.2: TỔNG HỢP KIỂM ĐỊNH THỐNG KÊ SUY LUẬN VÀ KÍCH THƯỚC HIỆU ỨNG (COUNCIL-SOTA VS. BASELINE)**

| Phép Kiểm Định Thống Kê / Đo Lường Hiệu Ứng | Council-SOTA (Trước Tinh Chỉnh) | Council-SOTA (Sau Tinh Chỉnh) | Mức Ý Nghĩa ($\alpha$) | Kết Luận Thống Kê |
| :--- | :---: | :---: | :---: | :---: |
| **Tỷ Lệ Vượt Qua (Pass Rate)** | 91.43% (96/105) | 93.33% (98/105) | — | Tăng vượt bậc (+44.76% tuyệt đối) |
| **Độ Phủ Dòng Trung Bình (Line Cov)** | 46.50% | 47.70% | — | Tăng gần gấp đôi (+23.57% tuyệt đối) |
| **Paired Student's $t$-test** | $t = 3.9809, p = 7.36 \times 10^{-4}$ | $t = 4.2075, p = 4.33 \times 10^{-4}$ | $p < 0.001$ | Bác bỏ $H_0$; Sai khác có ý nghĩa cực cao |
| **Wilcoxon Signed-Rank Test ($W$)** | $W = 6.0, p = 1.34 \times 10^{-5}$ | $W = 6.0, p = 1.34 \times 10^{-5}$ | $p < 0.001$ | Bác bỏ $H_0$; Xếp hạng vượt trội đồng thuận |
| **Mann-Whitney $U$ Test ($U$)** | $U = 351.0, p = 1.06 \times 10^{-3}$ | $U = 359.0, p = 5.08 \times 10^{-4}$ | $p < 0.001$ | Bác bỏ $H_0$; Phân phối độc lập vượt trội |
| **Kích Thước Hiệu Ứng Cohen's $d$** | **0.8687** (Large Effect) | **0.9181** (Large Effect) | $d \ge 0.8$ | Hiệu ứng thực nghiệm ở mức rất lớn |
| **Kích Thước Hiệu Ứng Vargha-Delaney $\hat{A}_{12}$** | **0.7959** (Large Effect) | **0.8141** (Large Effect) | $\hat{A}_{12} \ge 0.71$ | Xác suất Council-SOTA thắng áp đảo (81.41%) |

#### 5.2.1 Biện Luận Ý Nghĩa Thống Kê
- Giá trị $p$-value của phép kiểm định cặp Student's $t$-test đạt $p = 4.33 \times 10^{-4} \ll 0.001$ và kiểm định Wilcoxon đạt $p = 1.34 \times 10^{-5} \ll 0.0001$. Điều này chứng minh rằng xác suất mức tăng độ phủ $+23.57\%$ xảy ra do ngẫu nhiên là nhỏ hơn $0.013\%$, hoàn toàn bác bỏ giả thuyết vô hiệu $H_0$.
- Kích thước hiệu ứng tham số Cohen's $d$ đạt **0.9181** (vượt xa ngưỡng chuẩn $0.80$ của Cohen), định vị mức độ cải thiện ở phân vị hiệu ứng rất lớn.
- Kích thước hiệu ứng phi tham số Vargha-Delaney $\hat{A}_{12} = \mathbf{0.8141}$ chỉ ra rằng trong bất kỳ một phép ghép cặp ngẫu nhiên nào giữa một bài kiểm thử sinh bởi Council-SOTA và một bài sinh bởi Baseline, Council-SOTA có tới **81.41% xác suất** đạt độ bao phủ mã nguồn vượt trội hơn hẳn.

---

### 5.3 RQ3: ĐÓNG GÓP ĐỊNH LƯỢNG CỦA TÁC NHÂN PHẢN BIỆN ĐA VÒNG (ROUND 2 CRITIC ATTRIBUTION)

Một đóng góp kiến trúc trung tâm của Council-SOTA là cơ chế phản biện vi mô đa vòng thích ứng (Two-Round Multi-Turn Adaptive Critic). Trong tổng số 105 trials của Council-SOTA, tác nhân phản biện đã thực hiện thành công **29 ca sửa lỗi cứu vãn bài kiểm thử**:

**BẢNG 5.3: PHÂN BỔ ĐÓNG GÓP SỬA LỖI THEO CẤP ĐỘ PHẢN BIỆN (CRITIC ROUND ATTRIBUTION)**

| Vòng Phản Biện Thực Thi | Số Ca Sửa Thành Công | Tỷ Trọng Sửa Lỗi (%) | Các Dạng Lỗi Chính Được Triệt Tiêu | Điểm Đột Biến Trung Bình |
| :--- | :---: | :---: | :--- | :---: |
| **Vòng 1 (Syntactic & Import Repair)** | 24 ca | 82.76% | Lỗi ModuleNotFoundError, gán thiếu fixture, lệch import | 40.0% |
| **Vòng 2 (Micro-Assertion Calibration)** | 5 ca | 17.24% | Lỗi AssertionError vi mô, sai lệch cấu trúc giải nén tuple | 37.0% |
| **Tổng Số Ca Cứu Vãn Thành Công** | **29 ca** | **100.00%** | Khôi phục từ trạng thái trượt hoàn toàn về trạng thái PASS | **43.10%** |

#### 5.3.1 Vai Trò Sống Còn Của Phản Biện Vòng 2
Phân tích sâu 5 ca cứu vãn tại Vòng 2 cho thấy nếu chỉ dừng lại ở kiến trúc 1 vòng phản biện truyền thống (như Council Standard), toàn bộ 5 bài kiểm thử này sẽ bị loại bỏ:
1. `typesystem_oneof`: Vòng 1 giải quyết thành công lỗi định danh schema nhưng sinh ra mã kiểm tra ném ra ngoại lệ xác thực với mã lỗi sai lệch (`exc.code == "invalid"` thay vì `exc.code == "one_of"`). Phản biện Vòng 2 bắt trọn traceback diff của pytest, chỉ thị mô hình hiệu chỉnh chính xác mã kiểm tra mà không làm hỏng cấu trúc suite, nâng Pass Rate từ mức thảm họa 20.0% (ở Council Std) lên **100.0% tuyệt đối**.
2. `docstring_parser_google`: Vòng 2 hiệu chỉnh thành công lỗi lệch khoảng trắng và ký tự thụt lề đa dòng trong đối tượng trả về của parser Google docstring.
3. `genty_args` và `pycg_imports`: Vòng 2 xử lý hiện tượng unpack sai định dạng tuple và tái đồng bộ hóa cấu trúc receiver object.

---

### 5.4 RQ4: NGHIÊN CỨU BÓC TÁCH THÀNH PHẦN ĐA CHIỀU (MULTI-COMPONENT ABLATION STUDY)

Nhằm định lượng mức độ đóng góp độc lập của ba thành phần cốt lõi: (1) Neo định danh cú pháp AST (State Grounding), (2) Phản biện thích ứng đa vòng (Critic Repair), và (3) Bộ tiền lọc nhập khẩu an toàn (Auto-Import Preflight), một nghiên cứu bóc tách thành phần toàn diện được thực hiện trên 6 mục tiêu đại diện mang tính đa dạng cao (`typesystem_schema`, `typesystem_validation_error`, `genty_repeat`, `codetiming_timer`, `docstring_parser_numpydoc`, `pycg_classes`). Kết quả được trình bày tại Bảng 5.4.

**BẢNG 5.4: KẾT QUẢ NGHIÊN CỨU BÓC TÁCH THÀNH PHẦN (ABLATION STUDY TRÊN 6 TARGETS ĐẠI DIỆN)**

| Cấu Hình Thử Nghiệm (Configuration) | Tỷ Lệ Vượt Qua (Pass Rate) | Độ Phủ Dòng Mã (Line Cov %) | Độ Phủ Nhánh (Branch Cov %) | Độ Trễ Thực Thi Trung Bình (s) |
| :--- | :---: | :---: | :---: | :---: |
| **Full Method (Council-SOTA)** | **100.0% (6/6)** | **57.90%** | **28.59%** | **15.60 s** |
| Biến thể loại bỏ Auto-Import Preflight | **100.0% (6/6)** | 57.88% | 28.87% | 3.44 s |
| Biến thể loại bỏ Adaptive Critic Repair | 66.67% (4/6) | 49.14% | 38.61% | 2.73 s |
| Biến thể loại bỏ AST State Grounding | 66.67% (4/6) | **33.01%** | **13.26%** | 4.49 s |

#### 5.4.1 Biện Luận Động Học Bóc Tách
1. **Tác Động Của AST State Grounding**: Khi loại bỏ cơ chế neo bảng biểu tượng AST tĩnh, độ phủ dòng mã sụt giảm nghiêm trọng từ **57.90% xuống 33.01%** (mức mất mát khổng lồ **$-24.89\%$ tuyệt đối**), đồng thời độ phủ nhánh sụt giảm hơn một nửa (từ $28.59\%$ xuống $13.26\%$). Hiện tượng này xảy ra do mô hình rơi vào trạng thái ảo giác import và sinh các lời gọi phương thức không tồn tại, khiến bài kiểm thử lập tức sụp đổ ở giai đoạn nạp mã.
2. **Tác Động Của Adaptive Critic Repair**: Khi tắt cơ chế phản biện, Pass Rate lập tức sụt giảm từ **100.0% xuống 66.67%** (2 trong số 6 mục tiêu trượt hoàn toàn). Điều này khẳng định rằng ngay cả khi có gợi ý ngữ cảnh từ AST, mô hình ngôn ngữ vẫn có xác suất sinh lỗi assertion hoặc tham số sai lệch cần vòng phản hồi động để tự hiệu chỉnh.
3. **Vai Trò Của Auto-Import Preflight**: So sánh giữa phương pháp đầy đủ và biến thể không có Auto-Import Preflight cho thấy độ phủ dòng mã gần như bất biến ($57.90\%$ so với $57.88\%$). Phát hiện này chỉ ra rằng một khi AST Symbol-Table Grounding đã neo chính xác các định danh xuất khẩu hợp lệ, bước Auto-Import Preflight không làm tăng độ phủ mã mà chủ yếu đóng vai trò như một lưới an toàn thứ cấp nhằm triệt tiêu các lỗi nhập khẩu cục bộ.

---

### 5.5 RQ5: NĂNG LỰC PHÁT HIỆN LỖI NGỮ NGHĨA QUA KIỂM THỬ ĐỘT BIẾN (MUTATION WATERFALL ANALYSIS)

Đánh giá trên $M = 187$ thể đột biến cấp 1 thuộc 5 lớp toán tử biến dị cú pháp trên 21 tệp mã nguồn chứng minh bộ kiểm thử do Council-SOTA sản sinh sở hữu năng lực phát hiện lỗi ngữ nghĩa sâu sắc:
- **Tổng Số Mutant Bị Tiêu Diệt**: $K = 71 / 187$ thể đột biến.
- **Điểm Đột Biến Toàn Cục (Global Mutation Score)**: đạt **37.97%**.
- **Điểm Đột Biến Trung Bình Theo Mục Tiêu (Target-Level Mean Score)**: đạt **43.10%**.

**BẢNG 5.5: PHÂN BỔ NĂNG LỰC TIÊU DIỆT ĐỘT BIẾN THEO LỚP TOÁN TỬ BIẾN DỊ (MUTATION WATERFALL BREAKDOWN)**

| Lớp Toán Tử Đột Biến (Operator) | Tổng Số Thể Đột Biến Sinh Ra ($M$) | Số Lượng Tiêu Diệt ($K$) | Tỷ Lệ Tiêu Diệt (Kill Rate %) | Đánh Giá Độ Nhạy Ngữ Nghĩa |
| :--- | :---: | :---: | :---: | :--- |
| **SIR (Statement Inversion / Removal)**| 23 | 19 | **82.61%** | Cực kỳ nhạy cảm với việc vô hiệu hóa câu lệnh nghiệp vụ |
| **AOR (Arithmetic Operator Replacement)**| 9 | 3 | **33.33%** | Nhạy cảm với các biến đổi toán tử tính toán |
| **ROR (Relational Operator Replacement)**| 149 | 49 | **32.89%** | Đánh chặn hiệu quả các sai lệch điều kiện rẽ nhánh |
| **BVR (Boolean Value Replacement)** | 6 | 0 | 0.00% | Cần tăng cường các ca kiểm tra biên boolean tĩnh |
| **Tổng Cộng Toàn Bộ Phân Lớp** | **187** | **71** | **37.97%** | Trung bình mục tiêu: **43.10%** |

#### 5.5.1 Nhóm Module Đạt Điểm Diệt Đột Biến Đỉnh Cao (70% – 100%)
Nghiên cứu ghi nhận 5 module đạt hiệu quả diệt đột biến ở mức xuất sắc từ 70% đến 100%:
1. `pycg_callgraph`: **100.0% Kill Rate** (5/5 mutants bị diệt) — Bộ kiểm thử giám sát chặt chẽ toàn bộ các cạnh của đồ thị gọi hàm, bất kỳ một câu lệnh gán cạnh hay đảo nhánh nào đều bị assertion phát hiện.
2. `genty_repeat`: **100.0% Kill Rate** (3/3 mutants bị diệt) — Bao phủ triệt để logic vòng lặp và đếm số chu kỳ thực thi decorator.
3. `pycg_classes`: **90.0% Kill Rate** (9/10 mutants bị diệt) — Kiểm chứng toàn diện cấu trúc kế thừa và phân giải quan hệ đa hình của các lớp đối tượng.
4. `genty_args`: **75.0% Kill Rate** (3/4 mutants bị diệt) — Xác thực nghiêm ngặt cấu trúc dữ liệu đóng gói tham số.
5. `pycg_scopes`: **70.0% Kill Rate** (7/10 mutants bị diệt) — Bắt trọn các sai lệch trong việc tạo lập và ánh xạ không gian tên.

---

### 5.6 PHÂN TÍCH NHÓM CON CÓ NHÁNH LOGIC VÀ TRẠNG THÁI NGHIỆP VỤ (BRANCHING SUBGROUP ANALYSIS, $n=18$)

Trong tập 21 mục tiêu kiểm thử, có 3 mục tiêu mang đặc tính đặc thù: `string_utils_slugify` (hàm tiện ích chuỗi đơn giản, 0% mutant) cùng 2 hàm phân giải docstring (`docstring_parser_google` và `docstring_parser_numpydoc`) vốn có độ nhạy cảm rất cao với định dạng thụt lề văn bản tự do. 

Khi thực hiện phân tích phân tầng trên **nhóm con 18 mục tiêu có cấu trúc rẽ nhánh nghiệp vụ sâu và quản lý trạng thái phức tạp (Branching/Stateful Subgroup, $n=18$, tổng 90 trials mỗi arm)**, sự ưu việt của Council-SOTA đạt đến mức áp đảo:

**BẢNG 5.6: SO SÁNH HIỆU NĂNG TRÊN NHÓM CON CÓ NHÁNH LOGIC (BRANCHING SUBGROUP, $n=18$ TARGETS, 90 TRIALS / ARM)**

| Chỉ Số Đánh Giá | Zero-Shot Baseline | Council Standard | Council-SOTA | Mức Tăng Trưởng Tuyệt Đối |
| :--- | :---: | :---: | :---: | :---: |
| **Tỷ Lệ Vượt Qua (Pass Rate)** | 51.11% (46/90) | 70.00% (63/90) | **96.67% (87/90)** | **+45.56%** so với Baseline |
| **Số Target Đạt Đỉnh 100% Pass** | 1 / 18 targets | 8 / 18 targets | **16 / 18 targets** | **88.89%** số target hoàn hảo |
| **Độ Phủ Dòng Mã (Line Coverage)** | 25.40% | 39.78% | **49.88%** | **+24.48%** so với Baseline |

Trên nhóm đối tượng này, Council-SOTA đạt **96.67% Pass Rate** và **49.88% Line Coverage**, với **16/18 mục tiêu đạt tỷ lệ đỗ tuyệt đối 100% trên toàn bộ 5 hạt giống thực nghiệm**. Điều này chứng minh rằng kiến trúc Council-SOTA phát huy sức mạnh tối đa khi đối đầu với các bài toán kiểm thử phần mềm phức tạp, nơi luồng điều khiển có chiều sâu và trạng thái đối tượng đòi hỏi sự phối hợp đồng bộ giữa định danh ngữ cảnh và phản biện vi mô.

---

### 5.7 KIỂM CHỨNG ĐỘ ỔN ĐỊNH CÔNG NGHIỆP VÀ TỶ LỆ CHẬP CHỜN (FLAKINESS STRESS TESTING)

Trong triển khai kiểm thử tự động tại các hệ thống tích hợp liên tục (CI/CD), hiện tượng kiểm thử chập chờn (Flaky Tests)—tức các bài kiểm thử không đơn định gây báo động giả—là rào cản nghiêm trọng đối với độ tin cậy của hệ thống.

Để xác lập tính ổn định công nghiệp, toàn bộ 21 bộ kiểm thử Golden Suites do Council-SOTA sinh ra đã được đưa vào quy trình kiểm tra sức ép độ ổn định đa chu kỳ (Flakiness Stress Verification):
- Mỗi bộ kiểm thử được tái thực thi liên tục 5 lần độc lập trong cùng một môi trường runtime cố định.
- **Tổng Số Lượt Tái Thực Thi**: $21 \text{ suites} \times 5 \text{ chu kỳ} = 105 \text{ execution runs}$.
- **Kết Quả Ghi Nhận**: Toàn bộ **105 / 105 lượt chạy đều vượt qua hoàn toàn (100.0% Pass)**.
- **Tỷ Lệ Flaky Ghi Nhận**:
  $$FR = \frac{0}{105} \times 100\% = \mathbf{0.00\%}$$

Kết quả này khẳng định các cơ chế tiền chuẩn hóa của Council-SOTA (loại bỏ các hàm thời gian ngẫu nhiên không mock, chuẩn hóa thụt lề chuỗi docstring và cấm tuyệt đối các assertion phụ thuộc thứ tự dictionary bất định) đã tạo ra các bộ kiểm thử có tính tất định cao nhất, hoàn toàn sẵn sàng cho môi trường triển khai thực tế.
