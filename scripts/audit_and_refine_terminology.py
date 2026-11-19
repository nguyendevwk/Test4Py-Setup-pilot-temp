#!/usr/bin/env python3
"""Audit and refine Vietnamese technical terminology in MONOGRAPH_RESEARCH_REPORT.md

and all deliverable scripts.
"""

from pathlib import Path
import re

MD_PATH = Path("monograph_final_deliverables/reports/MONOGRAPH_RESEARCH_REPORT.md")
content = MD_PATH.read_text(encoding="utf-8")

# Replacement dictionary: (Pattern, Replacement, Explanation)
replacements = [
    # 1. Import paths: "nhập khẩu" -> "nạp module / import"
    (r'ảo giác đường dẫn nhập khẩu', 'ảo giác đường dẫn import nạp module', 'Import is not importing goods'),
    (r'Ảo giác đường dẫn nhập khẩu', 'Ảo giác đường dẫn import (nạp module)', 'Import is not importing goods'),
    (r'đường dẫn nhập khẩu', 'đường dẫn import (nạp module)', 'Import is not importing goods'),
    (r'cây phụ thuộc nhập khẩu tĩnh', 'cây phụ thuộc import tĩnh', 'Import dependencies'),

    # 2. Exports: "xuất khẩu" -> "công khai / exported"
    (r'bảng định danh xuất khẩu', 'bảng định danh công khai (Exported Symbol Table)', 'Exported symbols are not exported goods'),
    (r'bảng ký hiệu xuất khẩu', 'bảng ký hiệu công khai (Exported Symbols)', 'Exported symbols are not exported goods'),
    (r'sơ đồ xuất khẩu', 'sơ đồ định danh công khai (Export Schema)', 'Export schema'),
    (r'được xuất khẩu từ `typesystem\.base`', 'được định nghĩa và xuất (exported) từ `typesystem.base`', 'Exported symbol'),
    (r'được xuất khẩu công khai', 'được định nghĩa và xuất công khai (Exported Symbols)', 'Exported symbols'),

    # 3. Test Oracle: "tiên tri kiểm thử" -> "Oracle kiểm thử / cơ chế phán quyết kiểm thử"
    (r'suy biến tiên tri kiểm thử', 'suy biến Oracle kiểm thử (Oracle Degradation)', 'Oracle in SE is not a prophet/soothsayer'),
    (r'Bài toán Tiên tri Kiểm thử', 'Bài toán Oracle Kiểm thử (The Test Oracle Problem)', 'Test Oracle Problem'),
    (r'Tiên tri Kiểm thử \(Test Oracle\)', 'Oracle Kiểm thử (Test Oracle / Cơ chế Phán quyết)', 'Test Oracle definition'),
    (r'tiên tri kiểm thử', 'Oracle kiểm thử (Test Oracle)', 'Test Oracle'),

    # 4. Sandbox: "hộp cát" -> "môi trường cách ly (Sandbox)"
    (r'môi trường hộp cát cô lập', 'môi trường cách ly cô lập (Execution Sandbox)', 'Sandbox is isolation environment, not a sandpit'),
    (r'môi trường hộp cát', 'môi trường cách ly (Sandbox)', 'Sandbox'),

    # 5. Argument Unpacking: "giải nén" -> "phân rã đối số / unpacking đối số"
    (r'Decorator giải nén tập dữ liệu', 'Decorator phân rã tập dữ liệu (Dataset Unpacking)', 'Unpacking is not zip decompression'),
    (r'lỗi giải nén tham số', 'lỗi phân rã đối số (Argument Unpacking Error)', 'Argument unpacking'),
    (r'sai lệch cấu trúc giải nén tuple', 'sai lệch cấu trúc phân rã tuple (Tuple Unpacking Mismatch)', 'Tuple unpacking'),
    (r'quy ước giải nén \(unpacking protocol\)', 'giao thức phân rã đối số (Unpacking Protocol)', 'Unpacking protocol'),
    (r'decorator giải nén các phần tử', 'decorator phân rã các đối số (unpacks arguments)', 'Argument unpacking'),
    (r'chuẩn hóa cơ chế giải nén tham số', 'chuẩn hóa cơ chế phân rã đối số (Argument Unpacking)', 'Argument unpacking'),
    (r'giải nén đối số phức tạp', 'phân rã đối số phức tạp (Complex Argument Unpacking)', 'Argument unpacking'),
    (r'Lỗi Giải nén Tham số & Chữ ký Hàm', 'Lỗi Phân rã Đối số & Chữ ký Hàm (Argument Unpacking)', 'Argument unpacking'),
    (r'Lỗi Giải nén Tuple/Kwargs', 'Lỗi Phân rã Đối số Tuple/Kwargs (Unpacking Error)', 'Argument unpacking'),

    # 6. Single-Turn Truncation Trap: "ngắt mạch sửa lỗi đơn vòng" -> "cắt cụt sửa lỗi đơn vòng / dừng sớm"
    (r'Cái bẫy ngắt mạch sửa lỗi đơn vòng', 'Cái bẫy cắt cụt sửa lỗi đơn vòng (Single-Turn Truncation Trap)', 'Truncation is not circuit breaking'),
    (r'cái bẫy ngắt mạch sửa lỗi đơn vòng', 'cái bẫy cắt cụt sửa lỗi đơn vòng (Single-Turn Truncation Trap)', 'Truncation is not circuit breaking'),
    (r'bẫy ngắt mạch đơn vòng', 'bẫy cắt cụt đơn vòng (Truncation Trap)', 'Truncation trap'),
    (r'ngắt mạch đơn vòng', 'cắt cụt đơn vòng (Single-Turn Truncation)', 'Truncation'),

    # 7. Flaky Tests: "chập chờn" -> "bất định (Flaky Tests)"
    (r'chống kiểm thử chập chờn', 'chống kiểm thử bất định (Flakiness Defense)', 'Flaky tests are non-deterministic, not flickering'),
    (r'hiện tượng kiểm thử chập chờn', 'hiện tượng kiểm thử bất định (Flaky Tests)', 'Flaky tests'),
    (r'kiểm thử chập chờn \(Flaky Tests\)', 'kiểm thử bất định (Flaky Tests)', 'Flaky tests'),
    (r'tỷ lệ kiểm thử chập chờn', 'tỷ lệ kiểm thử bất định (Flaky Test Rate)', 'Flaky rate'),

    # 8. Tautological Assertions: "tự suy" -> "hằng đúng / hiển nhiên"
    (r'Khẳng định Tự suy / Rỗng', 'Khẳng định Hằng đúng / Hiển nhiên (Tautological Assertions)', 'Tautology is hằng đúng / đồng nhất thức'),
    (r'Khẳng định Tự suy', 'Khẳng định Hằng đúng (Tautological Assertions)', 'Tautological assertions'),
    (r'Khẳng định Rỗng & Tự suy Hiển nhiên', 'Khẳng định Rỗng & Hằng đúng Hiển nhiên (Tautological Assertions)', 'Tautological assertions'),

    # 9. Attribute Inflation: "Thổi phồng thuộc tính ngoại lệ" -> "Ảo giác thuộc tính ngoại lệ"
    (r'Thổi phồng thuộc tính ngoại lệ', 'Ảo giác thuộc tính ngoại lệ (Exception Attribute Hallucination)', 'Hallucination/fabrication of non-existent attributes'),
    (r'thổi phồng thuộc tính ngoại lệ', 'ảo giác thuộc tính ngoại lệ (Exception Attribute Hallucination)', 'Attribute hallucination'),

    # 10. Coverage: "độ bao phủ" -> "độ phủ"
    (r'Độ bao phủ thực tế', 'Độ phủ thực tế (Actual Coverage)', 'Code coverage is độ phủ, not độ bao phủ'),
    (r'độ bao phủ', 'độ phủ', 'Code coverage is độ phủ'),

    # 11. Random Seeds: "hạt giống" -> "seed ngẫu nhiên" where appropriate
    (r'hạt giống ngẫu nhiên độc lập', 'seed ngẫu nhiên độc lập (Random Seeds)', 'Random seed'),
    (r'hạt giống ngẫu nhiên', 'seed ngẫu nhiên (Random Seeds)', 'Random seed'),
    (r'đa hạt giống', 'đa seed ngẫu nhiên (Multi-seed)', 'Multi-seed'),
]

modified_content = content
changes_count = {}
for pattern, repl, desc in replacements:
    matches = len(re.findall(pattern, modified_content))
    if matches > 0:
        modified_content = re.sub(pattern, repl, modified_content)
        changes_count[pattern] = matches

print(f"Total replacement rules executed: {len(changes_count)}")
for pat, count in changes_count.items():
    print(f"  [{count:>2}x] '{pat}'")

MD_PATH.write_text(modified_content, encoding="utf-8")
print("\n[+] MONOGRAPH_RESEARCH_REPORT.md successfully updated with refined academic terminology!")
