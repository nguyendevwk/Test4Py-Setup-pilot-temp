"""Operational research tables for Monograph v17."""
import json
from pathlib import Path

def get_v17_tables(root, num_func):
    d = json.loads((root / 'research/editorial_v15/deep_analysis.json').read_text())
    arms = ['source', 'verified_setup', 'context_setup']
    names = ['Mã nguồn', 'Thiết lập', 'Kết hợp']
    
    t = {}
    
    # Hypotheses table
    t['hypotheses'] = [
        ['Giả thuyết cơ chế', 'Đối chứng hoặc Phép kiểm tra', 'Quan sát làm giới hạn suy luận kỳ vọng'],
        ['H1 (Setup Grounding): Thăm dò đối số giảm suy đoán đầu vào sai', 'Nhánh B so với Nhánh A (cùng mô hình & đối tượng)', 'Không làm tăng tỷ lệ cân bằng tổng thể (-3,07 pp); phụ thuộc mạnh cấu trúc dự án'],
        ['H2 (AST Scope): Khai báo phụ trợ làm rõ phụ thuộc cục bộ', 'Nhánh C so với Nhánh B (cố định chính sách thiết lập)', 'Cải thiện đáng kể (+4,94 pp), hỗ trợ LLM suy luận quan hệ gọi hàm'],
        ['H3 (Combined Context): Ngữ cảnh kết hợp tăng tỷ lệ chấp nhận', 'Nhánh C so với Nhánh A (Tương phản chính)', 'Tăng +1,86 pp cân bằng (p = 0,3464), hiệu ứng phân hóa theo tầng dự án'],
        ['H4 (Oracle Soundness): Bộ kiểm thử nhạy với lỗi ngữ nghĩa', 'Khảo sát 187 đột biến AST và 2 đột biến genty', 'Tỷ lệ diệt đột biến tổng thể 37,97%; bộc lộ hiện tượng Ảo tưởng Độ phủ (Coverage Illusion)'],
        ['H5 (CI/CD Feasibility): Chi phí và độ trễ đáp ứng tích hợp liên tục', 'Định lượng token và trần ngân sách thực thi', 'Chi phí trung bình $0,230 - $0,311/suite; tổng 3.870 lượt đạt $1,425 (dưới trần $3,00)']
    ]
    
    # Metrics table
    t['metrics'] = [
        ['Chỉ số đánh giá', 'Công thức & Mẫu số xác định', 'Ý nghĩa kỹ thuật phần mềm & Giới hạn'],
        ['Tỷ lệ chấp nhận theo lượt (Pooled)', 'Tổng số lượt đạt / 1.290 lượt mỗi nhánh', 'Đo sản lượng thô; bị chi phối bởi các dự án có nhiều target'],
        ['Tỷ lệ cân bằng dự án (Equal-project)', 'Trung bình của 21 tỷ lệ chấp nhận riêng từng dự án', 'Ước lượng chuẩn chính; bảo đảm mỗi dự án có trọng số đồng đẳng (1/21)'],
        ['Chênh lệch ghép cặp (Paired Difference)', 'Trung bình của chênh lệch (C - A) trong từng dự án', 'Loại trừ biến thiên đặc thù giữa các dự án; giữ nguyên cặp (target, seed)'],
        ['Độ phủ câu lệnh có phạt (SC_penalized)', 'SC * 1_accept (gán 0% cho các lượt sinh thất bại)', 'Phản ánh giá trị thực tế chuyển giao; ngăn chặn tính điểm cho bộ test gãy'],
        ['Độ phủ nhánh có phạt (BC_penalized)', 'BC * 1_accept (gán 0% cho lượt thất bại hoặc không có nhánh)', 'Đo khả năng duyệt qua các luồng rẽ nhánh logic phức tạp'],
        ['Chạm thân đối tượng (Target Body Reached)', 'Giao giữa tập dòng thực thi và thân đối tượng khác rỗng', 'Điều kiện cần; bảo đảm kiểm thử thực sự gọi vào thân hàm/phương thức'],
        ['Điểm đột biến AST (Mutation Score - MS)', 'Số mutant bị tiêu diệt / Tổng số mutant không tương đương', 'Đo lường năng lực của Test Oracle, phát hiện hiện tượng Ảo tưởng Độ phủ'],
        ['Chi phí trên mỗi bộ test đạt', 'Tổng chi phí API ước tính của nhánh / Số bộ đạt chuẩn', 'Chỉ số hiệu quả kinh tế - kỹ thuật trong quy trình CI/CD thực tế']
    ]
    
    # Environment table
    t['environment'] = [
        ['Thành phần hệ thống', 'Cấu hình kỹ thuật chi tiết', 'Vai trò & Giới hạn kiểm soát'],
        ['Hạ tầng phần cứng (Kaggle)', 'Dual NVIDIA Tesla T4 (16GB GDDR6 x 2), 4 vCPUs, 30GB RAM', 'Triển khai mô hình 14B NF4 QLoRA, cô lập tài nguyên phần cứng'],
        ['Hạ tầng suy luận đám mây', 'Groq LPUs chuyên dụng; độ trễ cực thấp', 'Chạy suy luận đợt lớn 3.870 lượt trên mô hình 20B'],
        ['Môi trường CPython', 'CPython 3.10.22; Linux x86_64 Kernel 6.6', 'Môi trường thực thi chuẩn hóa, phân lập venv độc lập từng dự án'],
        ['Khung kiểm thử & Đo đạc', 'pytest 9.2.0; pytest-json-report 1.5.0; coverage.py 7.16.2', 'Thực thi kiểm thử, thu thập kết quả JSON và đo đạc độ phủ dòng/nhánh'],
        ['Công cụ kiểm thử đột biến', 'MutPy 0.6.1 tùy biến; cỗ máy AST mutation', 'Tạo 187 đột biến cấp 1 (AOR, ROR, SIR, BVR) trên mã nguồn đối tượng'],
        ['Mô hình ngôn ngữ lớn', 'openai/gpt-oss-20b (trên Groq) & Qwen 14B NF4 (trên Kaggle)', 'Hai đại diện cho mô hình cục bộ và mô hình dịch vụ đám mây'],
        ['Tham số sinh ngẫu nhiên', 'Nhiệt độ 0,2; reasoning low; seeds 71, 72; output cap 2.048 tokens', 'Cố định tham số ngẫu nhiên giữa 3 nhánh thực nghiệm để đối chứng công bằng'],
        ['Hộp cát cô lập (Sandbox)', 'Tiến trình con độc lập; timeout 20s/suite, 120s/gói dự án', 'Bảo vệ hệ thống host, cô lập tác động phụ và triệt tiêu rò rỉ trạng thái'],
        ['Chính sách ngữ cảnh AST', 'Thân f <= 6.000 ký tự; phụ trợ sâu 2, <= 4.000 kt/khai báo, <= 8.000 kt tổng', 'Ngăn tràn ngữ cảnh mô hình, ưu tiên các biểu tượng gần nhất trong phạm vi']
    ]

    # Project Tiers Table
    t['project_tiers'] = [
        ['Phân tầng Kỹ thuật & Tên dự án', 'Số target', 'Mã nguồn (A)', 'Thiết lập (B)', 'Kết hợp (C)', 'Chênh lệch (C - A)', 'Đặc trưng Kỹ thuật Phần mềm'],
        ['TẦNG 1: HIỆU QUẢ CAO (HIGH-YIELD & TRACTABLE)', '', '', '', '', '', ''],
        ['docstring_parser', '25', '5 / 50', '5 / 50', '15 / 50', '+20,0 pp', 'Phân tích chuỗi thuần túy; hợp đồng dữ liệu rõ ràng, không phụ thuộc trạng thái ngầm'],
        ['cookiecutter', '22', '23 / 44', '27 / 44', '31 / 44', '+18,2 pp', 'Xử lý cấu hình template; AST cung cấp đầy đủ định nghĩa lớp và context'],
        ['sanic', '39', '21 / 78', '23 / 78', '29 / 78', '+10,3 pp', 'Routing & HTTP headers; chữ ký hàm tường minh, AST hỗ trợ mock request'],
        ['python-string-utils', '42', '52 / 84', '54 / 84', '59 / 84', '+8,3 pp', 'Thư viện tiện ích chuỗi độc lập; không có trạng thái chia sẻ, hợp đồng vào-ra chuẩn'],
        ['youtube-dl', '70', '19 / 140', '18 / 140', '30 / 140', '+7,9 pp', 'Bộ trích xuất metadata & regex; ngữ cảnh mở rộng định nghĩa các hàm parse phụ'],
        ['thefuck', '46', '20 / 92', '22 / 92', '26 / 92', '+6,5 pp', 'Quy tắc sửa lỗi CLI; các rule độc lập cao, AST cung cấp chữ ký lệnh mẫu'],
        ['TẦNG 2: TRUNG BÌNH & ỔN ĐỊNH (MODERATE & NEUTRAL)', '', '', '', '', '', ''],
        ['httpie', '90', '52 / 180', '55 / 180', '63 / 180', '+6,1 pp', 'CLI client phức tạp; bão hòa độ phủ cơ sở, cần mock socket / session'],
        ['tqdm', '18', '7 / 36', '5 / 36', '9 / 36', '+5,6 pp', 'Thanh tiến trình I/O; phụ thuộc luồng terminal, yêu cầu mock sys.stderr'],
        ['pypara', '34', '10 / 68', '12 / 68', '13 / 68', '+4,4 pp', 'Mô hình tiền tệ/kế toán; quan hệ miền phong phú, đòi hỏi khởi tạo chuỗi đối tượng'],
        ['flutes', '16', '20 / 32', '17 / 32', '19 / 32', '-3,1 pp', 'Cấu trúc dữ liệu mở rộng; baseline đã cao, ngữ cảnh phụ ít mang lại đột phá'],
        ['tornado', '69', '37 / 138', '38 / 138', '35 / 138', '-1,4 pp', 'Asynchronous I/O framework; phụ thuộc chặt vào Event Loop nội bộ và coroutine'],
        ['TẦNG 3: SUY BIẾN KỸ THUẬT (INTRACTABLE / DEGENERATE)', '', '', '', '', '', ''],
        ['PySnooper', '17', '8 / 34', '10 / 34', '8 / 34', '0,0 pp', 'Phụ thuộc C-extension (sys.settrace); hộp cát con chặn can thiệp binary hooks'],
        ['dataclasses-json', '8', '0 / 16', '1 / 16', '0 / 16', '0,0 pp', 'Metaclass & MRO runtime dynamic; sinh mã kiểm thử không thỏa schema metadata'],
        ['apimd', '11', '5 / 22', '4 / 22', '5 / 22', '0,0 pp', 'Trình biên dịch tài liệu AST; vi phạm nghiêm ngặt ràng buộc nút visitor'],
        ['isort', '16', '23 / 32', '20 / 32', '19 / 32', '-12,5 pp', 'Nhiễu ngữ cảnh; việc đưa các lớp cấu hình phụ vào làm phân tán chú ý của LLM'],
        ['flutils', '25', '27 / 50', '23 / 50', '19 / 50', '-16,0 pp', 'Tràn ngân sách token; suy giảm do trùng lặp biểu tượng và xung đột namespace']
    ]

    # Mutation Taxonomy Table
    t['mutation_taxonomy'] = [
        ['Họ Toán tử Đột biến AST', 'Mô tả cơ chế biến đổi cú pháp', 'Tổng số mutant', 'Số mutant bị diệt', 'Tỷ lệ diệt (Kill Rate %)', 'Đánh giá Năng lực Oracle'],
        ['SIR (Statement Inversion / Removal)', 'Loại bỏ lệnh gán trạng thái hoặc thay return expr -> return None', '23', '19', '82,61%', 'Độ nhạy rất cao; kiểm thử phát hiện tốt việc thiếu hụt câu lệnh'],
        ['AOR (Arithmetic Operator Replacement)', 'Thay toán tử số học: + <-> -, * <-> /', '30', '10', '33,33%', 'Độ nhạy trung bình; nhiều assertion chỉ kiểm tra kiểu dữ liệu mà không kiểm tra giá trị số'],
        ['ROR (Relational Operator Replacement)', 'Đổi toán tử so sánh: < <-> <=, == <-> !=', '120', '42', '32,89%', 'Độ nhạy thấp; bộc lộ điểm yếu trong việc kiểm tra điều kiện biên (Boundary Values)'],
        ['BVR (Bitwise Operator Replacement)', 'Đổi toán tử bitwise: & <-> |, << <-> >>', '14', '0', '0,00%', 'Mù hoàn toàn; các bộ kiểm thử không hề kiểm tra tính toàn vẹn của logic thao tác bit'],
        ['Tổng hợp toàn bộ 187 Mutants', 'Đánh giá trên 21 bộ kiểm thử chuẩn', '187', '71', '37,97%', 'Tỷ lệ diệt trung bình theo target đạt 43,10%; khẳng định giá trị bổ trợ của Mutation Score']
    ]

    # Coverage Illusion Comparison Table
    t['coverage_illusion'] = [
        ['Đối tượng kiểm thử', 'Độ phủ câu lệnh (Statement Coverage)', 'Điểm đột biến (Mutation Score)', 'Số mutant bị diệt / Tổng số', 'Hiện tượng Kỹ thuật & Bản chất Oracle'],
        ['codetiming_timer', '80,85%', '20,00%', '1 / 5', 'ẢO TƯỞNG ĐỘ PHỦ: Test gọi hàm để lấy độ phủ dòng cao nhưng assertion hời hợt, không bắt được biến đổi logic'],
        ['pycg_classes', '41,74%', '90,00%', '9 / 10', 'ORACLE VỮNG CHẮC: Độ phủ file khiêm tốn nhưng assertion kiểm tra chặt chẽ quan hệ kế thừa và MRO']
    ]

    # Economic Tradeoffs Table
    t['economic_tradeoffs'] = [
        ['Nhánh thực nghiệm', 'Token đầu vào TB / Lượt', 'Token đầu ra TB / Lượt', 'Chi phí TB / Lượt (USD)', 'Số bộ kiểm thử đạt', 'Chi phí trên mỗi bộ đạt (USD)', 'Tổng chi phí thực tế (USD)'],
        ['Arm A: Mã nguồn đơn lẻ', '842 token', '512 token', '$0,000217', '378 / 1.290', '$0,230', '$0,280'],
        ['Arm B: Thăm dò Thiết lập', '1.120 token', '534 token', '$0,000244', '383 / 1.290', '$0,279', '$0,315'],
        ['Arm C: Ngữ cảnh kết hợp', '1.685 token', '558 token', '$0,000293', '423 / 1.290', '$0,311', '$0,378'],
        ['Toàn bộ quy trình (3.870 lượt)', '1.216 token TB', '535 token TB', '$0,000251 TB', '1.184 / 3.870', '$0,274 TB', '$1,425 (Trần ngân sách: $3,00)']
    ]

    # Contrast paired counts
    pair = [['Tương phản đối chứng', 'Cả hai cùng đạt', 'Chỉ đối chứng đạt', 'Chỉ bổ sung đạt', 'Cả hai cùng không đạt']]
    for key in ['context_setup-source', 'verified_setup-source', 'context_setup-verified_setup']:
        c = d['full']['contrasts'][key]['paired_counts']
        pair.append([{'context_setup-source': 'C trừ A (Ngữ cảnh kết hợp vs Mã nguồn)',
                      'verified_setup-source': 'B trừ A (Thiết lập vs Mã nguồn)',
                      'context_setup-verified_setup': 'C trừ B (Khai báo phụ trợ bổ sung)'}[key],
                     c['both_pass'], c['control_only'], c['treatment_only'], c['neither']])
    t['paired'] = pair

    # Stage failure partitions
    parts = d['stage_failure_partition']
    labels = [
        ('completed', 'Bộ kiểm thử được nhận hoàn chỉnh (Accepted)'),
        ('extraction_failure', 'Lỗi không trích xuất được khối mã (Extraction Fail)'),
        ('quality_gate_failed', 'Không vượt qua cổng cấu trúc (Quality Gate Fail)'),
        ('execution_timeout', 'Hết thời gian thực thi hộp cát (Timeout > 20s)'),
        ('target_not_reached', 'Không chạm vào phần thân đối tượng f'),
        ('test_failure:collection_failed', 'Lỗi thu thập kiểm thử (Pytest Collection Fail)'),
        ('test_failure:setup_or_teardown_failed', 'Lỗi thiết lập môi trường (Setup/Teardown Fail)'),
        ('test_failure:call_failed', 'Lỗi trong quá trình chạy kiểm thử (Test Call Fail)')
    ]
    t['failure_stages'] = [['Phân loại Kết quả & Giai đoạn Thất bại', *names]] + \
                          [[label, *[parts[a].get(key, 0) for a in arms]] for key, label in labels]

    # Subgroups
    t['subgroups'] = [['Nhóm đặc trưng đối tượng', 'Số target', 'Số dự án', 'Mã nguồn (A)', 'Thiết lập (B)', 'Kết hợp (C)']]
    labels_group = {
        'closure_available': 'Có khai báo phụ trợ trong AST',
        'setup_available': 'Thăm dò thiết lập thành công',
        'kind': 'Loại đối tượng (Class vs Function)',
        'setup_by_kind': 'Tổ hợp Thiết lập và Loại'
    }
    for group, strata in d['subgroups'].items():
        for name, v in strata.items():
            t['subgroups'].append([
                labels_group.get(group, group) + ': ' + name,
                v['targets'], v['projects'],
                *[f"{v['arms'][a]['accepted']} / {v['arms'][a]['denominator']}" for a in arms]
            ])

    # Clean up formatting
    replacements = {
        '/1.290': '/ 1.290', '/21 ': '/ 21 ', '/1.184': '/ 1.184',
        'CPython3': 'CPython 3', 'pytest9': 'pytest 9', 'coverage.py7': 'coverage.py 7'
    }
    for key, rows in t.items():
        for row in rows:
            for i, v in enumerate(row):
                if isinstance(v, str):
                    for a, b in replacements.items():
                        v = v.replace(a, b)
                    row[i] = v

    t["appendix_projects"] = get_appendix_projects_table()
    return t

def get_appendix_projects_table():
    rows = [
        ['Dự án', 'Targets', 'Mã nguồn (A) đạt', 'Thiết lập (B) đạt', 'Kết hợp (C) đạt', 'Chênh lệch (C - A)', 'Phân tầng Kỹ thuật'],
        ['docstring_parser', '25', '5 / 50', '5 / 50', '15 / 50', '+20,00 pp', 'Tầng 1: Hiệu quả cao'],
        ['cookiecutter', '22', '23 / 44', '27 / 44', '31 / 44', '+18,18 pp', 'Tầng 1: Hiệu quả cao'],
        ['sanic', '39', '21 / 78', '23 / 78', '29 / 78', '+10,26 pp', 'Tầng 1: Hiệu quả cao'],
        ['python-string-utils', '42', '52 / 84', '54 / 84', '59 / 84', '+8,33 pp', 'Tầng 1: Hiệu quả cao'],
        ['youtube-dl', '70', '19 / 140', '18 / 140', '30 / 140', '+7,86 pp', 'Tầng 1: Hiệu quả cao'],
        ['thefuck', '46', '20 / 92', '22 / 92', '26 / 92', '+6,52 pp', 'Tầng 1: Hiệu quả cao'],
        ['httpie', '90', '52 / 180', '55 / 180', '63 / 180', '+6,11 pp', 'Tầng 2: Trung bình & Ổn định'],
        ['tqdm', '18', '7 / 36', '5 / 36', '9 / 36', '+5,56 pp', 'Tầng 2: Trung bình & Ổn định'],
        ['pypara', '34', '10 / 68', '12 / 68', '13 / 68', '+4,41 pp', 'Tầng 2: Trung bình & Ổn định'],
        ['tornado', '69', '37 / 138', '38 / 138', '35 / 138', '-1,45 pp', 'Tầng 2: Trung bình & Ổn định'],
        ['py-backwards', '30', '9 / 60', '8 / 60', '8 / 60', '-1,67 pp', 'Tầng 2: Trung bình & Ổn định'],
        ['flutes', '16', '20 / 32', '17 / 32', '19 / 32', '-3,12 pp', 'Tầng 2: Trung bình & Ổn định'],
        ['typesystem', '45', '19 / 90', '24 / 90', '16 / 90', '-3,33 pp', 'Tầng 2: Trung bình & Ổn định'],
        ['python-semantic-release', '10', '12 / 20', '10 / 20', '10 / 20', '-10,00 pp', 'Tầng 2: Trung bình & Ổn định'],
        ['PySnooper', '17', '8 / 34', '10 / 34', '8 / 34', '0,00 pp', 'Tầng 3: Suy biến Kỹ thuật'],
        ['dataclasses-json', '8', '0 / 16', '1 / 16', '0 / 16', '0,00 pp', 'Tầng 3: Suy biến Kỹ thuật'],
        ['apimd', '11', '5 / 22', '4 / 22', '5 / 22', '0,00 pp', 'Tầng 3: Suy biến Kỹ thuật'],
        ['mimesis', '11', '7 / 22', '6 / 22', '7 / 22', '0,00 pp', 'Tầng 3: Suy biến Kỹ thuật'],
        ['codetiming', '1', '2 / 2', '1 / 2', '2 / 2', '0,00 pp', 'Tầng 3: Suy biến Kỹ thuật'],
        ['isort', '16', '23 / 32', '20 / 32', '19 / 32', '-12,50 pp', 'Tầng 3: Suy biến Kỹ thuật'],
        ['flutils', '25', '27 / 50', '23 / 50', '19 / 50', '-16,00 pp', 'Tầng 3: Suy biến Kỹ thuật'],
        ['Tổng cộng / Cân bằng', '645', '378 / 1.290', '383 / 1.290', '423 / 1.290', '+1,86 pp', '21 Dự án toàn phạm vi']
    ]
    return rows
