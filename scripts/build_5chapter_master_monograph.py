#!/usr/bin/env python3
"""Builds the 5-Chapter Master Monograph in Markdown format.

Assembles all 5 chapters, replaces ASCII diagrams with figure links,
and saves to monograph_final_deliverables/reports/MONOGRAPH_RESEARCH_REPORT.md.
"""

from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parents[1]
CHAPTER_DIR = BASE_DIR / "monograph_final_deliverables" / "chapters"
OUT_MD = BASE_DIR / "monograph_final_deliverables" / "reports" / "MONOGRAPH_RESEARCH_REPORT.md"

# Read chapter files
ch1_text = (CHAPTER_DIR / "chapter_front_matter_and_ch1.md").read_text(encoding="utf-8")
ch23_text = (CHAPTER_DIR / "chapter_2_and_3_architecture.md").read_text(encoding="utf-8")
ch45_text = (CHAPTER_DIR / "chapter_4_and_5_experiments.md").read_text(encoding="utf-8")
ch67_text = (CHAPTER_DIR / "chapter_6_and_7_qualitative_economics.md").read_text(encoding="utf-8")
ch89_text = (CHAPTER_DIR / "chapter_8_and_9_validity_conclusions.md").read_text(encoding="utf-8")

def clean_text(s):
    # Sanitize invalid XML/control characters
    s = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f]', '', s)
    
    # Strict academic terminology sanitization
    terms = [
        ("Ảo giác đường dẫn nhập khẩu", "Ảo giác đường dẫn nạp module (Import Hallucinations)"),
        ("ảo giác đường dẫn nhập khẩu", "ảo giác đường dẫn nạp module (Import Hallucinations)"),
        ("phụ thuộc nhập khẩu tĩnh", "phụ thuộc nạp module tĩnh"),
        ("Bộ tiền lọc nhập khẩu an toàn", "Bộ tiền xử lý nạp module an toàn"),
        ("bộ tiền lọc nhập khẩu", "bộ tiền xử lý nạp module"),
        ("lỗi nhập khẩu cục bộ", "lỗi nạp module (import errors) cục bộ"),
        ("lỗi nhập khẩu", "lỗi nạp module (import errors)"),
        ("nhập khẩu tĩnh", "nạp module tĩnh"),
        ("sơ đồ xuất khẩu thực tế", "sơ đồ định danh công khai thực tế"),
        ("symbol này được xuất khẩu từ", "symbol này được export từ"),
        ("định danh xuất khẩu hợp lệ", "định danh công khai hợp lệ (Exported Symbols)"),
        ("Thổi phồng thuộc tính ngoại lệ", "Ảo giác thuộc tính ngoại lệ"),
        ("thổi phồng thuộc tính ngoại lệ", "ảo giác thuộc tính ngoại lệ"),
        ("Cái bẫy ngắt mạch sửa lỗi đơn vòng", "Cái bẫy cắt cụt sửa lỗi đơn vòng (Single-Turn Truncation Trap)"),
        ("cái bẫy ngắt mạch sửa lỗi đơn vòng", "cái bẫy cắt cụt sửa lỗi đơn vòng (Single-Turn Truncation Trap)"),
        ("giải nén tuple", "phân rã tuple (Tuple Unpacking)"),
        ("giải nén đối số", "phân rã đối số (Argument Unpacking)"),
        ("giải nén tham số", "phân rã tham số"),
        ("bảng định danh xuất khẩu", "bảng định danh công khai (Exported Symbols)"),
        ("bảng ký hiệu xuất khẩu", "bảng định danh công khai (Exported Symbols)"),
        ("bảng xuất khẩu tĩnh", "bảng định danh công khai tĩnh"),
        ("danh mục định danh xuất khẩu", "danh mục định danh công khai (Exported Symbols)"),
        ("tái xuất khẩu (re-export)", "tái công khai / export (re-export)"),
        ("được xuất khẩu trực tiếp", "được export trực tiếp"),
        ("Bảng ký hiệu định danh AST xuất khẩu", "Bảng định danh công khai trích xuất từ AST (AST Exported Symbols)"),
        ("khẳng định tự suy", "khẳng định hằng đúng / hiển nhiên"),
        ("tiên tri kiểm thử", "Oracle kiểm thử (Test Oracle)"),
    ]
    for old, new in terms:
        s = s.replace(old, new)
    return s

# =============================================================================
# EXTRACT AND REORGANIZE INTO 5 CHAPTERS
# =============================================================================

# --- FRONT MATTER ---
# From ch1_text, extract Abstract VN, Extended Abstract, Abbreviations
fm_match = re.search(r'## PHẦN ĐẦU \(FRONT MATTER\)(.*?)# CHƯƠNG MỞ ĐẦU', ch1_text, re.DOTALL)
front_matter_content = fm_match.group(1).strip() if fm_match else ""

# Add Figure List and Table List to Front Matter
fm_lists = """
### DANH MỤC BẢNG (LIST OF TABLES)

- **Bảng 2.1**: Ma trận đối sánh toàn diện giữa Council-SOTA và các công trình SOTA quốc tế
- **Bảng 4.1**: Đặc tả kỹ thuật và phân tầng 21 Curated Benchmark Targets thuộc Test4Py
- **Bảng 4.2**: Đặc tả 5 toán tử đột biến cấp 1 trong First-Order Mutation Testing Framework
- **Bảng 4.3**: Đối chứng hiệu năng ba trục: Baseline vs. Council Standard vs. Council-SOTA
- **Bảng 4.4**: Kết quả kiểm định thống kê suy luận (Wilcoxon, Mann-Whitney U, Paired t, A12, Cohen's d)
- **Bảng 4.5**: Bảng phân bổ chi tiết 29 ca sửa lỗi thành công giữa Vòng 1 và Vòng 2 của Critic
- **Bảng 4.6**: Nghiên cứu bóc tách thành phần đa chiều (Multi-Component Ablation Study)
- **Bảng 4.7**: Bảng tổng hợp điểm đột biến và tỷ lệ tiêu diệt 187 mutants trên 21 targets
- **Bảng 4.8**: Phân tích nhóm con có nhánh rẽ logic và trạng thái nghiệp vụ (Branching Subgroup, n=18)
- **Bảng 4.9**: Kết quả 5 chu kỳ kiểm chứng độ ổn định (Flakiness Stress Test) trên 21 Golden Suites
- **Bảng 5.1**: Bảng phân loại học lỗi định tính của mô hình SLM 20B trong sinh test tự động
- **Bảng 5.2**: Phân rã chi phí token theo từng thành phần kiến trúc trong Council-SOTA
- **Bảng 5.3**: Ma trận trả lời trực diện 4 câu hỏi nghiên cứu cốt lõi (RQ1 – RQ4)

---

### DANH MỤC HÌNH VẼ VÀ BIỂU ĐỒ (LIST OF FIGURES)

- **Hình 2.1**: So sánh thời gian khởi động (Cold-Start Latency) và chiếm dụng VRAM giữa Call-Graph RAG và AST Grounding
- **Hình 3.1**: Sơ đồ kiến trúc hội đồng thích ứng khép kín Council-SOTA 5 trụ cột
- **Hình 4.1**: Tiến trình cải thiện Pass Rate từ Baseline qua Standard đến Council-SOTA trên 21 Curated Targets
- **Hình 4.2**: Biểu đồ Dumbbell đối chứng độ phủ dòng mã (Line Coverage Gain) giữa Baseline và Council-SOTA
- **Hình 4.3**: Phân bổ đóng góp định lượng 29 ca sửa lỗi cứu vãn bộ test của Critic Vòng 1 và Vòng 2
- **Hình 4.4**: Biểu đồ Thác nước (Waterfall) năng lực kiểm thử đột biến cấp 1 trên 187 mutants
- **Hình 4.5**: Biểu đồ Radar 5 trục đánh giá cân bằng đa chiều giữa các chiến lược sinh test
- **Hình 5.1**: Biểu đồ đối chứng tăng trưởng Pass Rate và Line Coverage trong 2 nghiên cứu trường hợp (Case Studies)
- **Hình 5.2**: Đánh đổi đường biên Pareto tối ưu giữa chất lượng kiểm thử và thời gian trễ / chi phí trong CI/CD

---

### DANH MỤC THUẬT TOÁN (LIST OF ALGORITHMS)

- **Thuật toán 1**: Neo Định Danh Cú Pháp AST và Sinh Bộ Kiểm Thử Cơ Sở (AST-Grounded Synthesis)
- **Thuật toán 2**: Quy Trình Phản Biện Sửa Lỗi Thích Ứng Hai Vòng Khép Kín (Two-Round Adaptive Critic Repair)
"""

# --- CHƯƠNG 1 ---
ch1_body_match = re.search(r'# CHƯƠNG MỞ ĐẦU \(INTRODUCTION\)(.*?)(?=# CHƯƠNG 1:|$)', ch1_text, re.DOTALL)
ch1_content = ch1_body_match.group(1).strip() if ch1_body_match else ""
ch1_text_formatted = f"# CHƯƠNG 1: GIỚI THIỆU VÀ ĐẶT VẤN ĐỀ NGHIÊN CỨU\n\n{ch1_content}"

# --- CHƯƠNG 2 ---
# Part A: Literature review from ch1_text
lit_match = re.search(r'# CHƯƠNG 1: TỔNG QUAN NGHIÊN CỨU & CÔNG TRÌNH LIÊN QUAN(.*?)(?=### TÀI LIỆU THAM KHẢO CHƯƠNG 1|$)', ch1_text, re.DOTALL)
lit_content = lit_match.group(1).strip() if lit_match else ""
lit_content = lit_content.replace("Bảng 1.1", "Bảng 2.1")
lit_content = lit_content.replace("### 1.1", "### 2.1").replace("### 1.2", "### 2.2").replace("### 1.3", "### 2.3").replace("### 1.4", "### 2.4")

# Part B: Empirical Motivation (Cold-start RAG bottleneck) from ch23_text
mot_match = re.search(r'# CHƯƠNG 2: ĐỘNG CƠ THỰC NGHIỆM: SỰ BẾ TẮC CỦA CALL-GRAPH RAG(.*?)(?=# CHƯƠNG 3:|$)', ch23_text, re.DOTALL)
mot_content = mot_match.group(1).strip() if mot_match else ""
# Replace ASCII block with Figure 2.1 reference
ascii_pattern_1 = re.compile(r'```text\n\+---.*?```', re.DOTALL)
fig21_ref = """
![Hình 2.1: So sánh thời gian khởi động (Cold-Start Latency) và chiếm dụng VRAM giữa Call-Graph RAG và AST Grounding](file:///home/heurix/Documents/Test4Py_Setup/monograph_final_deliverables/figures/fig_cold_start_comparison.png)

*Hình 2.1: So sánh thời gian khởi động (Cold-Start Latency) và chiếm dụng VRAM giữa Call-Graph RAG và AST Grounding.*
"""
mot_content = ascii_pattern_1.sub(fig21_ref, mot_content, count=1)

# Renumber sections in Ch2
mot_content = mot_content.replace("### 2.1.", "### 2.5.").replace("### 2.2.", "### 2.6.").replace("### 2.3.", "### 2.7.").replace("### 2.4.", "### 2.8.")

ch2_text_formatted = f"""# CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ TỔNG QUAN CÔNG TRÌNH LIÊN QUAN

{lit_content}

---

## 2.5. ĐỘNG CƠ THỰC NGHIỆM: SỰ BẾ TẮC CỦA CALL-GRAPH RAG TRÊN HẠ TẦNG GIỚI HẠN

{mot_content}
"""

# --- CHƯƠNG 3 ---
# Architecture from ch23_text
arch_match = re.search(r'# CHƯƠNG 3: THIẾT KẾ KIẾN TRÚC & PHƯƠNG PHÁP HỘI ĐỒNG TỐI ƯU \(COUNCIL-SOTA\)(.*?)$', ch23_text, re.DOTALL)
arch_content = arch_match.group(1).strip() if arch_match else ""

# Replace Mermaid block with Figure 3.1 reference
mermaid_pattern = re.compile(r'```mermaid\nflowchart TD.*?```', re.DOTALL)
fig31_ref = """
![Hình 3.1: Sơ đồ kiến trúc hội đồng thích ứng khép kín Council-SOTA 5 trụ cột](file:///home/heurix/Documents/Test4Py_Setup/monograph_final_deliverables/figures/fig_council_sota_architecture.png)

*Hình 3.1: Sơ đồ kiến trúc hội đồng thích ứng khép kín Council-SOTA 5 trụ cột.*
"""
arch_content = mermaid_pattern.sub(fig31_ref, arch_content, count=1)

# Replace ASCII auditor box with clean text
ascii_pattern_auditor = re.compile(r'```text\n\+---.*?QUY TRÌNH KIỂM TOÁN.*?```', re.DOTALL)
arch_content = ascii_pattern_auditor.sub("", arch_content)

ch3_text_formatted = f"""# CHƯƠNG 3: KIẾN TRÚC HỆ THỐNG VÀ PHƯƠNG PHÁP COUNCIL-SOTA

{arch_content}
"""

# --- CHƯƠNG 4 ---
# Experiments and results from ch45_text
exp_match = re.search(r'# CHƯƠNG 4: THIẾT KẾ THỰC NGHIỆM VÀ PHƯƠNG PHÁP ĐÁNH GIÁ(.*?)(?=# CHƯƠNG 5:|$)', ch45_text, re.DOTALL)
exp_content = exp_match.group(1).strip() if exp_match else ""

res_match = re.search(r'# CHƯƠNG 5: KẾT QUẢ THỰC NGHIỆM VÀ ĐỐI CHỨNG ĐỊNH LƯỢNG(.*?)$', ch45_text, re.DOTALL)
res_content = res_match.group(1).strip() if res_match else ""

# Add image embeddings for Chapter 4
fig41_42_ref = """
![Hình 4.1: Tiến trình cải thiện Pass Rate từ Baseline qua Standard đến Council-SOTA trên 21 Curated Targets](file:///home/heurix/Documents/Test4Py_Setup/monograph_final_deliverables/figures/chart_pass_rate_progression_elite.png)

*Hình 4.1: Tiến trình cải thiện Pass Rate từ Baseline qua Standard đến Council-SOTA trên 21 Curated Targets.*

![Hình 4.2: Biểu đồ Dumbbell đối chứng độ phủ dòng mã (Line Coverage Gain) giữa Baseline và Council-SOTA](file:///home/heurix/Documents/Test4Py_Setup/monograph_final_deliverables/figures/chart_coverage_gain_dumbbell.png)

*Hình 4.2: Biểu đồ Dumbbell đối chứng độ phủ dòng mã (Line Coverage Gain) giữa Baseline và Council-SOTA.*
"""
res_content = res_content.replace("### 5.1 RQ1: ĐỐI CHỨNG HIỆU NĂNG BA TRỤC TOÀN DIỆN (THREE-WAY COMPARISON)",
                                  f"### 4.3 RQ1: ĐỐI CHỨNG HIỆU NĂNG BA TRỤC TOÀN DIỆN (THREE-WAY COMPARISON)\n\n{fig41_42_ref}")

fig43_ref = """
![Hình 4.3: Phân bổ đóng góp định lượng 29 ca sửa lỗi cứu vãn bộ test của Critic Vòng 1 và Vòng 2](file:///home/heurix/Documents/Test4Py_Setup/monograph_final_deliverables/figures/fig_critic_repair_attribution.png)

*Hình 4.3: Phân bổ đóng góp định lượng 29 ca sửa lỗi cứu vãn bộ test của Critic Vòng 1 và Vòng 2.*
"""
res_content = res_content.replace("### 5.3 RQ3: ĐÓNG GÓP ĐỊNH LƯỢNG CỦA TÁC NHÂN PHẢN BIỆN ĐA VÒNG (ROUND 2 CRITIC ATTRIBUTION)",
                                  f"### 4.5 RQ3: ĐÓNG GÓP ĐỊNH LƯỢNG CỦA TÁC NHÂN PHẢN BIỆN ĐA VÒNG (ROUND 2 CRITIC ATTRIBUTION)\n\n{fig43_ref}")

fig44_ref = """
![Hình 4.4: Biểu đồ Thác nước (Waterfall) năng lực kiểm thử đột biến cấp 1 trên 187 mutants](file:///home/heurix/Documents/Test4Py_Setup/monograph_final_deliverables/figures/chart_mutation_waterfall.png)

*Hình 4.4: Biểu đồ Thác nước (Waterfall) năng lực kiểm thử đột biến cấp 1 trên 187 mutants.*
"""
res_content = res_content.replace("### 5.5 RQ5: NĂNG LỰC PHÁT HIỆN LỖI NGỮ NGHĨA QUA KIỂM THỬ ĐỘT BIẾN (MUTATION WATERFALL ANALYSIS)",
                                  f"### 4.7 RQ5: NĂNG LỰC PHÁT HIỆN LỖI NGỮ NGHĨA QUA KIỂM THỬ ĐỘT BIẾN (MUTATION WATERFALL ANALYSIS)\n\n{fig44_ref}")

fig45_ref = """
![Hình 4.5: Biểu đồ Radar 5 trục đánh giá cân bằng đa chiều giữa các chiến lược sinh test](file:///home/heurix/Documents/Test4Py_Setup/monograph_final_deliverables/figures/chart_radar_5dimensions.png)

*Hình 4.5: Biểu đồ Radar 5 trục đánh giá cân bằng đa chiều giữa các chiến lược sinh test.*
"""
res_content = res_content.replace("### 5.6 PHÂN TÍCH NHÓM CON CÓ NHÁNH LOGIC VÀ TRẠNG THÁI NGHIỆP VỤ (BRANCHING SUBGROUP ANALYSIS, $n=18$)",
                                  f"### 4.8 PHÂN TÍCH NHÓM CON CÓ NHÁNH LOGIC VÀ TRẠNG THÁI NGHIỆP VỤ (BRANCHING SUBGROUP ANALYSIS, $n=18$)\n\n{fig45_ref}")

res_content = res_content.replace("### 5.2 RQ2:", "### 4.4 RQ2:")
res_content = res_content.replace("### 5.4 RQ4:", "### 4.6 RQ4:")
res_content = res_content.replace("### 5.7 KIỂM CHỨNG ĐỘ ỔN ĐỊNH", "### 4.9 KIỂM CHỨNG ĐỘ ỔN ĐỊNH")

# Normalize Table and Subsection numbering in Chapter 4
res_content = re.sub(r'BẢNG 5\.1', 'BẢNG 4.3', res_content, flags=re.I)
res_content = re.sub(r'BẢNG 5\.2', 'BẢNG 4.4', res_content, flags=re.I)
res_content = re.sub(r'BẢNG 5\.3', 'BẢNG 4.5', res_content, flags=re.I)
res_content = re.sub(r'BẢNG 5\.4', 'BẢNG 4.6', res_content, flags=re.I)
res_content = re.sub(r'BẢNG 5\.5', 'BẢNG 4.7', res_content, flags=re.I)
res_content = re.sub(r'BẢNG 5\.6', 'BẢNG 4.8', res_content, flags=re.I)
res_content = re.sub(r'BẢNG 5\.7', 'BẢNG 4.9', res_content, flags=re.I)

res_content = re.sub(r'#### 5\.1\.1', '#### 4.3.1', res_content)
res_content = re.sub(r'#### 5\.2\.1', '#### 4.4.1', res_content)
res_content = re.sub(r'#### 5\.3\.1', '#### 4.5.1', res_content)
res_content = re.sub(r'#### 5\.4\.1', '#### 4.6.1', res_content)

ch4_text_formatted = f"""# CHƯƠNG 4: THIẾT KẾ THỰC NGHIỆM VÀ KẾT QUẢ ĐỐI CHỨNG ĐỊNH LƯỢNG

{exp_content}

---

## 4.3. KẾT QUẢ THỰC NGHIỆM VÀ ĐỐI CHỨNG ĐỊNH LƯỢNG

{res_content}
"""

# --- CHƯƠNG 5 ---
qual_match = re.search(r'# CHƯƠNG 6: PHÂN TÍCH LỖI ĐỊNH TÍNH, TINH CHỈNH GROUNDING VÀ KIỂM CHỨNG ĐỘ ỔN ĐỊNH(.*?)(?=# CHƯƠNG 7:|$)', ch67_text, re.DOTALL)
qual_content = qual_match.group(1).strip() if qual_match else ""

# Remove ASCII taxonomy box
ascii_taxonomy_pattern = re.compile(r'```\n\+---.*?TAXONOMY LỖI CỦA SLM 20B.*?```', re.DOTALL)
qual_content = ascii_taxonomy_pattern.sub('', qual_content)

fig51_ref = """
![Hình 5.1: Biểu đồ đối chứng tăng trưởng Pass Rate và Line Coverage trong 2 nghiên cứu trường hợp (Case Studies)](file:///home/heurix/Documents/Test4Py_Setup/monograph_final_deliverables/figures/fig_case_studies_comparison.png)

*Hình 5.1: Biểu đồ đối chứng tăng trưởng Pass Rate và Line Coverage trong 2 nghiên cứu trường hợp (Case Studies).*
"""
qual_content = re.sub(r'```\nPass Rate:.*?```', '', qual_content, flags=re.DOTALL)
qual_content = qual_content.replace("## 6.2. NGHIÊN CỨU TRƯỜNG HỢP 1", f"{fig51_ref}\n\n## 5.1.2. NGHIÊN CỨU TRƯỜNG HỢP 1")

econ_match = re.search(r'# CHƯƠNG 7: KINH TẾ HỌC HỆ THỐNG & ĐÁNH ĐỔI ĐƯỜNG BIÊN PARETO TRONG MÔI TRƯỜNG CI/CD(.*?)$', ch67_text, re.DOTALL)
econ_content = econ_match.group(1).strip() if econ_match else ""

# Omit Section 7.3 entirely (Economic TCO tradeoff between Cloud LPU and On-premise GPU)
econ_content = re.sub(r'## 7\.3\..*$', '', econ_content, flags=re.DOTALL).strip()

fig52_ref = """
![Hình 5.2: Đánh đổi đường biên Pareto tối ưu giữa chất lượng kiểm thử và thời gian trễ / chi phí trong CI/CD](file:///home/heurix/Documents/Test4Py_Setup/monograph_final_deliverables/figures/fig_pareto_frontier_ci_cd.png)

*Hình 5.2: Đánh đổi đường biên Pareto tối ưu giữa chất lượng kiểm thử và thời gian trễ / chi phí trong CI/CD.*
"""
econ_content = re.sub(r'```\n\s+Độ Bao phủ & Điểm Đột biến.*?```', fig52_ref, econ_content, flags=re.DOTALL)

val_match = re.search(r'# CHƯƠNG 8: TÍNH HỢP LỆ VÀ CÁC NGUY CƠ ĐE DỌA KẾT QUẢ \(THREATS TO VALIDITY\)(.*?)(?=# CHƯƠNG 9:|$)', ch89_text, re.DOTALL)
val_content = val_match.group(1).strip() if val_match else ""

conc_match = re.search(r'# CHƯƠNG 9: KẾT LUẬN VÀ PHƯƠNG HƯỚNG PHÁT TRIỂN(.*?)(?=# DANH MỤC TÀI LIỆU THAM KHẢO|$)', ch89_text, re.DOTALL)
conc_content = conc_match.group(1).strip() if conc_match else ""

ref_app_match = re.search(r'(# DANH MỤC TÀI LIỆU THAM KHẢO.*$)', ch89_text, re.DOTALL)
ref_app_content = ref_app_match.group(1).strip() if ref_app_match else ""

qual_content = qual_content.replace("## 6.1.", "## 5.1.").replace("Bảng 6.1", "Bảng 5.1")
qual_content = qual_content.replace("## 6.3.", "## 5.1.3.").replace("## 6.4.", "## 5.1.4.")
qual_content = re.sub(r'## 5.1.4. KIỂM CHỨNG ĐỘ ỔN ĐỊNH.*?$', '', qual_content, flags=re.DOTALL)

econ_content = econ_content.replace("## 7.1.", "## 5.2.").replace("## 7.2.", "## 5.3.")
econ_content = econ_content.replace("Bảng 7.1", "Bảng 5.2").replace("Bảng 7.2", "Bảng 5.2b")

# Renumber Threats to Validity to Section 5.4 (since TCO 5.4 was omitted)
val_content = val_content.replace("### 8.1.", "### 5.4.1.").replace("### 8.2.", "### 5.4.2.").replace("### 8.3.", "### 5.4.3.").replace("### 8.4.", "### 5.4.4.")
val_content = val_content.replace("#### 8.1.1.", "#### 5.4.1.1.").replace("#### 8.1.2.", "#### 5.4.1.2.")
val_content = val_content.replace("#### 8.2.1.", "#### 5.4.2.1.").replace("#### 8.2.2.", "#### 5.4.2.2.")
val_content = val_content.replace("#### 8.3.1.", "#### 5.4.3.1.").replace("#### 8.3.2.", "#### 5.4.3.2.")
val_content = val_content.replace("#### 8.4.1.", "#### 5.4.4.1.").replace("#### 8.4.2.", "#### 5.4.4.2.").replace("#### 8.4.3.", "#### 5.4.4.3.").replace("#### 8.4.4.", "#### 5.4.4.4.")
val_content = val_content.replace("Bảng 8.1", "Bảng 5.2c")

# Renumber Conclusions to Section 5.5
conc_content = conc_content.replace("### 9.1.", "### 5.5.1.").replace("### 9.2.", "### 5.5.2.").replace("### 9.3.", "### 5.5.3.")
conc_content = conc_content.replace("Bảng 9.1", "Bảng 5.3").replace("Bảng 5.4", "Bảng 5.3")

ch5_text_formatted = f"""# CHƯƠNG 5: PHÂN TÍCH CHUYÊN SÂU, BÀN LUẬN KINH TẾ HỌC VÀ KẾT LUẬN

{qual_content}

---

## 5.2. KINH TẾ HỌC HỆ THỐNG VÀ ĐÁNH ĐỔI ĐƯỜNG BIÊN PARETO TRONG CI/CD

{econ_content}

---

## 5.4. TÍNH HỢP LỆ VÀ CÁC NGUY CƠ ĐE DỌA KẾT QUẢ (THREATS TO VALIDITY)

{val_content}

---

## 5.5. TỔNG KẾT, TRẢ LỜI CÂU HỎI NGHIÊN CỨU VÀ HÀM Ý THỰC TIỄN

{conc_content}
"""

master_text = f"""# TIỂU LUẬN KẾT THÚC HỌC PHẦN CAO CẤP: KỸ NGHỆ PHẦN MỀM TIÊN TIẾN
# CHUYÊN KHẢO NGHIÊN CỨU: SINH VÀ SỬA LỖI BỘ KIỂM THỬ ĐƠN VỊ TỰ ĐỘNG BẰNG KIẾN TRÚC HỘI ĐỒNG TỐI ƯU (COUNCIL-SOTA) TRÊN HỆ QUY CHIẾU TEST4PY BENCHMARK

*Closed-Loop Multi-Turn Adaptive Critic Repair with Abstract Syntax Tree Symbol-Table Grounding and Mutation-Hardened Verification for Modern Python Ecosystems*

---

## PHẦN ĐẦU (FRONT MATTER)

{front_matter_content}

{fm_lists}

---

{ch1_text_formatted}

---

{ch2_text_formatted}

---

{ch3_text_formatted}

---

{ch4_text_formatted}

---

{ch5_text_formatted}

---

{ref_app_content}
"""

master_text = clean_text(master_text)
OUT_MD.write_text(master_text, encoding="utf-8")
print(f"[+] Master 5-Chapter Monograph successfully created at:\n{OUT_MD}")
print(f"Total characters: {len(master_text):,}")
print(f"Total lines: {len(master_text.splitlines()):,}")
