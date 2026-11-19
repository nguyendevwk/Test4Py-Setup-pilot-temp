from pathlib import Path

path = Path("monograph_final_deliverables/reports/MONOGRAPH_RESEARCH_REPORT.md")
text = path.read_text(encoding="utf-8")

substitutions = [
    ("AST Symbol-Table Export Grounding (Trích xuất bảng xuất khẩu tĩnh, 0 token, < 50ms CPU)",
     "AST Symbol-Table Export Grounding (Trích xuất bảng định danh công khai tĩnh, 0 token, < 50ms CPU)"),
    ("Trích xuất tự động danh mục định danh xuất khẩu từ `__init__.py`",
     "Trích xuất tự động danh mục định danh công khai (Exported Symbols) từ `__init__.py`"),
    ("thường tái xuất khẩu (re-export) các lớp và hàm cốt lõi",
     "thường tái công khai và xuất (re-export) các lớp và hàm cốt lõi"),
    ("trong khi hàm `parse` chuẩn được xuất khẩu trực tiếp tại gốc `docstring_parser`",
     "trong khi hàm `parse` chuẩn được export trực tiếp tại gốc `docstring_parser`"),
    ("trích xuất toàn bộ các định danh xuất khẩu hợp lệ",
     "trích xuất toàn bộ các định danh công khai hợp lệ (Exported Symbols)"),
    ("(3) Bộ tiền lọc nhập khẩu an toàn (Auto-Import Preflight)",
     "(3) Bộ tiền xử lý nạp module an toàn (Auto-Import Preflight)"),
    ("các định danh xuất khẩu hợp lệ, bước Auto-Import Preflight không làm tăng độ phủ mã mà chủ yếu đóng vai trò như một lưới an toàn thứ cấp nhằm triệt tiêu các lỗi nhập khẩu cục bộ.",
     "các định danh công khai hợp lệ (Exported Symbols), bước Auto-Import Preflight không làm tăng độ phủ mã mà chủ yếu đóng vai trò như một chốt chặn an toàn thứ cấp nhằm triệt tiêu các lỗi nạp module (import errors) cục bộ."),
    ("Bảng ký hiệu định danh AST xuất khẩu",
     "Bảng ký hiệu định danh công khai trích xuất từ AST (AST Exported Symbols)"),
]

for old, new in substitutions:
    if old in text:
        text = text.replace(old, new)
        print(f"Replaced: {old[:50]}...")
    else:
        print(f"Warning: NOT found: {old[:50]}...")

path.write_text(text, encoding="utf-8")
print("[+] Final replacements applied successfully!")
