#!/usr/bin/env python3
"""Build publication-ready v11 monograph with refined architecture figure and polished narrative flow."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import zipfile

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(__file__).resolve().parents[1]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    src_docx = ROOT / 'reports/Tieu_Luan_CNPMTT_Council_SOTA_v10.docx'
    out_docx = ROOT / 'reports/Tieu_Luan_CNPMTT_Council_SOTA_v11.docx'
    out_pdf = ROOT / 'reports/rendered/Tieu_Luan_CNPMTT_Council_SOTA_v11.pdf'
    
    expected_v10_sha = "7a6daa601583588b8118f0aa4a7deda0ed6afb85e21a2f821646a7e72afc414e"
    actual_v10_sha = digest(src_docx)
    if actual_v10_sha != expected_v10_sha:
        raise ValueError(f"v10 docx sha mismatch: {actual_v10_sha} != {expected_v10_sha}")
    
    if out_docx.exists():
        os.remove(out_docx)
    
    assets_v10 = ROOT / 'reports/Tieu_Luan_CNPMTT_Council_SOTA_v10_assets'
    assets_v11 = ROOT / 'reports/Tieu_Luan_CNPMTT_Council_SOTA_v11_assets'
    if assets_v11.exists():
        shutil.rmtree(assets_v11)
    shutil.copytree(assets_v10, assets_v11)
    
    # 1. Copy v10 to v11
    shutil.copy2(src_docx, out_docx)
    
    # 2. Update Image 3.1 in docx zip directly
    new_arch_img = Path('/tmp/fig_council_sota_architecture_v11.png')
    if not new_arch_img.exists():
        raise FileNotFoundError("New architecture image /tmp/fig_council_sota_architecture_v11.png not found")
    
    shutil.copy2(new_arch_img, assets_v11 / 'fig_council_sota_architecture_v11.png')
    
    # Update word/media/image3.png inside out_docx
    tmp_zip = ROOT / 'reports/tmp_v11_repack.zip'
    with zipfile.ZipFile(out_docx, 'r') as zin, zipfile.ZipFile(tmp_zip, 'w') as zout:
        for item in zin.infolist():
            if item.filename == 'word/media/image3.png':
                zout.writestr(item, new_arch_img.read_bytes())
            else:
                zout.writestr(item, zin.read(item.filename))
    shutil.move(tmp_zip, out_docx)
    print("[+] Successfully replaced image3.png in v11 docx with updated architecture diagram!")
    
    # 3. Polish Narrative Flow using python-docx
    doc = Document(out_docx)
    
    # In Section 4.10: replace the out-of-place 688-response budget paragraph
    found_410_budget = False
    for p in doc.paragraphs:
        if p.style.name != 'CouncilTOC' and p.text.startswith("Ngân sách toàn chiến dịch được giới hạn 3 USD. Sau đợt benchmark và screen phát triển bổ sung"):
            p.text = (
                "Đánh giá mở rộng được thực hiện với trần ngân sách phân bổ theo dõi qua sổ request độc lập. "
                "Trong cohort 9 project này (162 lượt hoàn tất), toàn bộ các request đều được ghi nhận token usage, "
                "kiểm soát hạn mức và rate limit, đóng góp vào tổng ngân sách kiểm soát an toàn dưới trần 3 USD của đề tài."
            )
            found_410_budget = True
            break
    print(f"[+] Replaced premature budget in Section 4.10: {found_410_budget}")
    
    # At the end of Section 4.14: Insert comprehensive campaign budget
    # Anchor: "CHƯƠNG 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN"
    anchor_ch5 = next(p for p in doc.paragraphs if p.style.name != 'CouncilTOC' and p.text.startswith("CHƯƠNG 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN"))
    
    # Create paragraph before anchor
    budget_summary_text = (
        "Tổng kết ngân sách toàn chiến dịch: Toàn bộ quá trình thực nghiệm trên Groq "
        "(gồm các cohort thăm dò ban đầu, đợt mở rộng 9 project, đợt mở rộng 12 project CodaMOSA và screen cải tiến ngữ cảnh) "
        "được giới hạn trần 3 USD. Sổ request ghi nhận tổng cộng 688 response có usage; "
        "ước tính usage theo giá cấu hình (.075 USD/1M input, .30 USD/1M output) là 0.158223 USD. "
        "Tổng phân bổ bảo thủ ghi sổ cộng các khoản reserve và đối soát mốc ban đầu là 0.605180 USD, nằm an toàn trong hạn mức. "
        "Đây không phải hóa đơn nhà cung cấp mà là số liệu kiểm toán chi phí nội bộ; không cộng hai con số thành chi phí trùng lặp. "
        "Riêng đợt CodaMOSA-frame 204 response có ước tính 0.041849 USD và đợt screen cải tiến ngữ cảnh 68 response có ước tính 0.014155 USD. "
        "Nguồn đối soát: research/groq_codamosa_extension_20261119/budget.json và research/groq_context_development_20261119/budget.json."
    )
    
    p_budget = anchor_ch5.insert_paragraph_before(budget_summary_text)
    p_budget.paragraph_format.first_line_indent = Inches(0.3)
    p_budget.paragraph_format.space_before = Pt(6)
    p_budget.paragraph_format.space_after = Pt(6)
    p_budget.paragraph_format.line_spacing = 1.15
    print("[+] Added unified campaign budget summary at the end of Chapter 4 before Chapter 5!")
    
    # Save modified docx
    doc.save(out_docx)
    print(f"[+] Saved updated docx: {out_docx}")

if __name__ == '__main__':
    main()
