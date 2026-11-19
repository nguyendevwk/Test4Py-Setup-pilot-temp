"""Build the Master Monograph v17 with advanced Software Engineering depth and publication formatting."""
from __future__ import annotations
import copy, hashlib, json, os, re, shutil, subprocess
from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
from polish_council_report import polish_tables
from revise_kaggle_groq_narrative import rebuild_lists
import v17_research_tables as vt

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'reports/Tieu_Luan_CNPMTT_Council_SOTA_v15.docx'
OUT = ROOT / 'reports/Tieu_Luan_CNPMTT_Council_SOTA_v17.docx'
CONTENT = ROOT / 'research/editorial_v17/report_body.md'
ASSETS = ROOT / 'reports/Tieu_Luan_CNPMTT_Council_SOTA_v17_assets'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def num(x, d=2):
    if d == 2 and x and abs(x) < 0.005:
        d = 6
    return f"{x:.{d}f}".replace('.', ',')

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def add_formatted_text(p, text):
    """Parse inline markdown: **bold**, *italic*, `code`, ~sub~, ^sup^."""
    token_pattern = re.compile(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|~[^~]+~|\^[^^]+\^)')
    tokens = token_pattern.split(text)
    for t in tokens:
        if not t:
            continue
        if t.startswith('**') and t.endswith('**') and len(t) >= 4:
            run = p.add_run(t[2:-2])
            run.bold = True
        elif t.startswith('*') and t.endswith('*') and len(t) >= 2:
            run = p.add_run(t[1:-1])
            run.italic = True
        elif t.startswith('`') and t.endswith('`') and len(t) >= 2:
            run = p.add_run(t[1:-1])
            run.font.name = 'Consolas'
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(0x37, 0x47, 0x4F)
        elif t.startswith('~') and t.endswith('~') and len(t) >= 2:
            run = p.add_run(t[1:-1])
            run.font.subscript = True
        elif t.startswith('^') and t.endswith('^') and len(t) >= 2:
            run = p.add_run(t[1:-1])
            run.font.superscript = True
        else:
            p.add_run(t)

def main():
    print(f"Building v17 from base {SRC.name}...")
    if not SRC.exists():
        raise FileNotFoundError(f"Source file {SRC} not found!")

    shutil.copy2(SRC, OUT)
    doc = Document(OUT)

    # Cut everything after "MỞ ĐẦU" to insert v17 content
    start = max(i for i, p in enumerate(doc.paragraphs) if p.text.strip() == 'MỞ ĐẦU')
    first = doc.paragraphs[start]._p
    container = doc._element.body
    cut = False
    for element in list(container):
        if element is first:
            cut = True
        if cut and element.tag != qn('w:sectPr'):
            container.remove(element)

    # Reference mapping from existing v11 docx
    old = Document(ROOT / 'reports/Tieu_Luan_CNPMTT_Council_SOTA_v11.docx')
    refs = {}
    for p in old.paragraphs:
        m = re.match(r'^\[(\d+)\]\s', p.text)
        if m:
            refs[int(m.group(1))] = p.text
    refs[24] = '[24] R. Mukherjee et al., “BugsInPy: A Database of Existing Bugs in Python Programs to Enable Controlled Testing and Debugging Studies,” trong Proceedings of the 28th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE), 2020.'

    body = CONTENT.read_text(encoding='utf-8')
    used = sorted({int(x) for x in re.findall(r'\[(\d+)\]', body)})
    ids = {n: i + 1 for i, n in enumerate(used)}

    def cite(text):
        return re.sub(r'\[(\d+)\]', lambda m: f"[{ids.get(int(m.group(1)), int(m.group(1)))}]", text)

    def para(text, style=None):
        p = doc.add_paragraph(style=style)
        add_formatted_text(p, cite(text))
        if not style:
            p.paragraph_format.keep_with_next = False
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(4)
        return p

    def bullet_item(text):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.6)
        p.paragraph_format.first_line_indent = Cm(-0.4)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = False
        r_bullet = p.add_run("• ")
        r_bullet.bold = True
        r_bullet.font.color.rgb = RGBColor(0x1E, 0x88, 0xE5)
        add_formatted_text(p, cite(text))
        return p

    def numbered_item(num_str, text):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.7)
        p.paragraph_format.first_line_indent = Cm(-0.5)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = False
        r_num = p.add_run(f"{num_str} ")
        r_num.bold = True
        add_formatted_text(p, cite(text))
        return p

    def callout_box(text):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, "F0F4F8")
        
        # Set left border thick blue, others none
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="none"/>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="1E88E5"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(tcBorders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.left_indent = Cm(0.2)
        p.paragraph_format.right_indent = Cm(0.2)
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        add_formatted_text(p, cite(text))
        
        # Empty space after table
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        return table

    def equation_box(eq_num, formula_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        
        # Add formula run
        r_formula = p.add_run(f"{formula_text}    ")
        r_formula.italic = True
        r_formula.bold = False
        r_formula.font.size = Pt(10.5)
        
        # Add equation number
        r_num = p.add_run(f"({eq_num})")
        r_num.bold = True
        r_num.font.size = Pt(10)
        r_num.font.color.rgb = RGBColor(0x45, 0x5A, 0x64)
        return p

    def heading(text, level):
        p = doc.add_paragraph(style=f"Heading {level}")
        add_formatted_text(p, cite(text))
        p.paragraph_format.keep_with_next = True
        if level == 1:
            p.paragraph_format.page_break_before = True
        return p

    def caption(text):
        p = doc.add_paragraph(style='Caption')
        add_formatted_text(p, cite(text))
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.first_line_indent = 0
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        return p

    def table(rows, cap=None):
        if cap:
            caption(cap)
        t = doc.add_table(rows=0, cols=len(rows[0]))
        t.style = 'Table Grid'
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for row in rows:
            r = t.add_row()
            for c, value in zip(r.cells, row):
                c.text = str(value)
        return t

    code_tables = []
    main_tables = {}

    def code(text, cap=None):
        if cap:
            caption(cap)
        t = doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = t.cell(0, 0)
        set_cell_background(cell, "F8F9FA")
        p = cell.paragraphs[0]
        p.text = text
        p.paragraph_format.line_spacing = 1.05
        for r in p.runs:
            r.font.name = 'Consolas'
            r.font.size = Pt(9)
        code_tables.append(t)
        return t

    def figure(key, cap):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = 0
        p.paragraph_format.keep_with_next = True
        width = min(s.page_width - s.left_margin - s.right_margin for s in doc.sections)
        fig_path = ASSETS / f"{key}.png"
        if not fig_path.exists():
            raise FileNotFoundError(f"Figure not found: {fig_path}")
        p.add_run().add_picture(str(fig_path), width=width)
        c = caption(cap)
        c.paragraph_format.keep_with_next = False

    # Load operational tables
    TABLES = vt.get_v17_tables(ROOT, num)

    # Line-by-line parsing of markdown
    lines = body.splitlines()
    in_code_block = False
    code_buffer = []

    for line in lines:
        stripped = line.strip()

        # Handle Code blocks
        if stripped.startswith('```'):
            if in_code_block:
                in_code_block = False
                code_text = '\n'.join(code_buffer)
                first_line = code_buffer[0] if code_buffer else ""
                if "Thuật toán" in first_line or "QUY CÁCH" in first_line:
                    cap_text = first_line
                    body_c = '\n'.join(code_buffer[1:])
                    code(body_c, cap_text)
                else:
                    code(code_text)
                code_buffer.clear()
            else:
                in_code_block = True
                code_buffer.clear()
            continue

        if in_code_block:
            code_buffer.append(line)
            continue

        if not stripped:
            continue

        # Handle Headings
        if stripped.startswith('# '):
            heading(stripped[2:], 1)
        elif stripped.startswith('### '):
            heading(stripped[4:], 3)
        elif stripped.startswith('## '):
            heading(stripped[3:], 2)

        # Handle Figures, Tables, Equations
        elif stripped.startswith('@figure '):
            key, cap = [x.strip() for x in stripped[8:].split('|', 1)]
            figure(key, cap)
        elif stripped.startswith('@table '):
            key, cap = [x.strip() for x in stripped[7:].split('|', 1)]
            if key not in TABLES:
                raise KeyError(f"Table key '{key}' not in TABLES dictionary!")
            main_tables[key] = table(TABLES[key], cap)
        elif stripped.startswith('@equation '):
            eq_num, formula = [x.strip() for x in stripped[10:].split('|', 1)]
            equation_box(eq_num, formula)

        # Handle Blockquotes
        elif stripped.startswith('> '):
            callout_box(stripped[2:])

        # Handle Bullet items
        elif stripped.startswith('- ') or stripped.startswith('* '):
            bullet_item(stripped[2:])

        # Handle Numbered items
        elif re.match(r'^\d+\.\s', stripped):
            m = re.match(r'^(\d+\.)\s(.*)$', stripped)
            numbered_item(m.group(1), m.group(2))

        # Handle standard paragraph
        else:
            para(stripped)

    # Polish tables and formatting
    polish_tables(doc)
    for t in doc.tables:
        for ri, row in enumerate(t.rows):
            for ci, c in enumerate(row.cells):
                for p in c.paragraphs:
                    p.paragraph_format.first_line_indent = 0
                    p.paragraph_format.left_indent = 0
                    p.paragraph_format.right_indent = 0
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT if ci == 0 and ri > 0 else WD_ALIGN_PARAGRAPH.CENTER

    for t in code_tables:
        for p in t.cell(0, 0).paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.05
            for run in p.runs:
                run.font.name = 'Consolas'
                run.font.size = Pt(9)
                run.font.bold = False

    rebuild_lists(doc)
    for p in doc.paragraphs:
        if p.style.name == 'Caption' and p.text.startswith(('Bảng', 'Thuật toán', 'Mẫu', 'Hình')):
            p.paragraph_format.keep_with_next = True

    doc.save(OUT)
    print(f"Saved initial v17 document: {OUT}")

if __name__ == '__main__':
    main()
