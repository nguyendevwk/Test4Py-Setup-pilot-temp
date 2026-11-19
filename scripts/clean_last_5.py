from pathlib import Path

path = Path("monograph_final_deliverables/reports/MONOGRAPH_RESEARCH_REPORT.md")
text = path.read_text(encoding="utf-8")

substitutions = [
    ("Quản lý Nhập khẩu Phức tạp", "Quản lý Import / Nạp module Phức tạp"),
    ("Tính Toàn vẹn Hộp cát (Sandbox Isolation)", "Tính Toàn vẹn Môi trường Cách ly (Sandbox Isolation)"),
    ("Tính Toàn vẹn Hộp cát Thực thi (Subprocess Execution Sandbox)", "Tính Toàn vẹn Môi trường Thực thi Cách ly (Subprocess Execution Sandbox)"),
    ("Tỷ Lệ Kiểm Thử Chập Chờn (Flaky Test Rate - $FR$)", "Tỷ Lệ Kiểm Thử Bất Định (Flaky Test Rate - $FR$)"),
    ("KIỂM CHỨNG ĐỘ ỔN ĐỊNH CÔNG NGHIỆP VÀ TỶ LỆ CHẬP CHỜN (FLAKINESS STRESS TESTING)",
     "KIỂM CHỨNG ĐỘ ỔN ĐỊNH CÔNG NGHIỆP VÀ TỶ LỆ BẤT ĐỊNH (FLAKINESS STRESS TESTING)"),
]

for old, new in substitutions:
    if old in text:
        text = text.replace(old, new)
        print(f"Replaced: {old}")
    else:
        print(f"Warning: NOT found: {old}")

path.write_text(text, encoding="utf-8")
print("[+] Absolute 0 remaining awkward terms achieved!")
