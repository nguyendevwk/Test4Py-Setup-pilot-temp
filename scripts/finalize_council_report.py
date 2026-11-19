"""Produce a new final copy with verified references and cost provenance."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from docx import Document
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_TAB_ALIGNMENT,WD_TAB_LEADER
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt,Cm

ROOT=Path(__file__).resolve().parents[1]


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def refresh_evidence_hashes(doc,source):
    metadata=source.with_suffix('.polish.json')
    changes=[]
    if not metadata.exists():return changes
    for entry in json.loads(metadata.read_text()).get('evidence',[]):
        path=Path(entry['path'])
        if not path.exists():continue
        current=sha(path);old=entry['sha256']
        if current==old:continue
        for p in doc.paragraphs:
            if old in p.text:p.text=p.text.replace(old,current)
        changes.append({'path':str(path),'previous_evidence_sha256':old,'current_evidence_sha256':current})
    return changes


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();before=sha(a.input)
    if a.output.exists() or a.input.resolve()==a.output.resolve():raise ValueError('New distinct output required')
    doc=Document(a.input);changes=[]
    for paragraph in list(doc.paragraphs):
        text=paragraph.text
        if text.startswith('[8]'):
            paragraph.text='[8] G. Fraser và A. Arcuri, “Whole Test Suite Generation,” IEEE Transactions on Software Engineering, vol. 39, no. 2, tr. 276–291, 2013. DOI: 10.1109/TSE.2012.14. https://www.evosuite.org/publications/'
            changes.append('Corrected EvoSuite title/pages/DOI from author publication record')
        if text.startswith('[17]'):
            paragraph._element.getparent().remove(paragraph._element)
            changes.append('Removed unverified flaky-study metadata; verified Luo et al. [16] remains')
        elif '[17]' in text:paragraph.text=text.replace('[17]','')
    # Close reference-number gaps only after unverified entries have been removed.
    present=[]
    for paragraph in doc.paragraphs:
        match=re.match(r'^\[(\d+)\]',paragraph.text)
        if match:present.append(int(match.group(1)))
    mapping={old:i+1 for i,old in enumerate(sorted(set(present)))}
    paragraphs=list(doc.paragraphs)+[p for table in doc.tables for row in table.rows for cell in row.cells for p in cell.paragraphs]
    for paragraph in paragraphs:
        value=re.sub(r'\[(\d+)\]',lambda m:'['+str(mapping.get(int(m.group(1)),int(m.group(1))))+']',paragraph.text)
        value=value.replace('Bảng 1.1','Bảng TABLE_SWAP').replace('Bảng 1.2','Bảng 1.1').replace('Bảng TABLE_SWAP','Bảng 1.2')
        value=value.replace('Ba vị trí target của black không đủ source tương ứng đã bị loại trước suy luận; không thay bằng target thuận lợi hơn.',
            'Ba vị trí target của black bị loại trước suy luận theo tiêu chí import-origin: loader trỏ tới binary extension (.so), dù có file .py đi kèm. Trình chuẩn bị chỉ nhận module được loader nạp từ .py, không cưỡng ép nạp source. Đây là giới hạn điều kiện thực thi, không phải thiếu mã nguồn; không thay bằng target thuận lợi hơn.')
        if value!=paragraph.text:paragraph.text=value
    changes.append({'reference_number_mapping':mapping})
    # Put the project results after the aggregate interpretation, not directly under the heading.
    project_note=next((p for p in doc.paragraphs if p.text.startswith('Bảng bổ sung: chênh lệch')),None)
    if project_note:
        for table in doc.tables:
            if len(table.columns)==4 and table.rows[0].cells[0].text=='Project':
                project_note._p.addprevious(table._tbl)
                break
    section=None;table_number=10;table_count={}
    for element in list(doc.element.body):
        if element.tag.endswith('}p'):
            value=''.join(element.itertext())
            match=re.match(r'^4\.(6|7|8|9|10)\.',value)
            if match:section=match.group(1)
            elif value.startswith('CHƯƠNG 5.'):section=None
        elif element.tag.endswith('}tbl') and section:
            table_count[section]=table_count.get(section,0)+1
            names={'6':['Phiên bản source của pilot mới','Kết quả đối chứng pilot mới'],
                   '7':['Phục hồi các node kiểm thử gốc không sửa đổi'],
                   '8':['Phân loại kết quả mutation screen mới'],
                   '9':['Kết quả thử nghiệm phát triển sau pilot'],
                   '10':['Kết quả đánh giá mở rộng theo từng project']}
            choices=names[section];label=choices[min(table_count[section]-1,len(choices)-1)]
            node=OxmlElement('w:p');element.addprevious(node)
            pp=Paragraph(node,doc._body);pp.style='Caption';pp.add_run(f'Bảng 4.{table_number}. {label}')
            table_number+=1
    # Regenerate navigation from the corrected body headings, not stale original titles.
    ps=list(doc.paragraphs)
    body_start=max(i for i,p in enumerate(ps) if p.text.strip()=='MỞ ĐẦU')
    toc_start=next(i for i,p in enumerate(ps) if p.text.strip()=='MỤC LỤC')
    toc_end=max(i for i,p in enumerate(ps[:body_start]) if p.text.strip()=='DANH MỤC BẢNG')
    headings=[]
    for paragraph in ps[body_start:]:
        title=paragraph.text.strip()
        if title in {'MỞ ĐẦU','TÀI LIỆU THAM KHẢO'} or re.match(r'^(CHƯƠNG \d+\.|\d+\.\d+(?:\.\d+)?\.\s|PHỤ LỤC)',title):
            if title not in headings:headings.append(title)
    for paragraph in ps[toc_start+1:toc_end]:paragraph._p.getparent().remove(paragraph._p)
    if 'CouncilTOC' not in doc.styles:
        style=doc.styles.add_style('CouncilTOC',WD_STYLE_TYPE.PARAGRAPH)
        style.font.name='Times New Roman';style.font.size=Pt(11)
        style.paragraph_format.line_spacing=1
        style.paragraph_format.space_after=Pt(2)
        style.paragraph_format.tab_stops.add_tab_stop(Cm(15.3),WD_TAB_ALIGNMENT.RIGHT,WD_TAB_LEADER.DOTS)
    anchor_toc=ps[toc_start]
    for title in headings:
        node=OxmlElement('w:p');anchor_toc._p.addnext(node)
        paragraph=Paragraph(node,anchor_toc._parent);paragraph.style='CouncilTOC'
        paragraph.add_run(title+'\t—')
        anchor_toc=paragraph
    changes.append({'rebuilt_toc_entries':len(headings),'pages':'populated after PDF render'})
    # Rebuild both lists from actual body captions; discard stale original page references.
    for list_title,next_title,prefix in [('DANH MỤC BẢNG','DANH MỤC HÌNH','Bảng'),('DANH MỤC HÌNH','DANH MỤC TỪ VIẾT TẮT','Hình')]:
        current=list(doc.paragraphs);body_i=max(i for i,p in enumerate(current) if p.text.strip()=='MỞ ĐẦU')
        start=max(i for i,p in enumerate(current[:body_i]) if p.text.strip()==list_title)
        end=max(i for i,p in enumerate(current[:body_i]) if p.text.strip()==next_title)
        captions=[]
        for pp in current[body_i:]:
            if re.match(r'^'+prefix+r' \d+\.\d+\.',pp.text.strip()) and pp.text.strip() not in captions:captions.append(pp.text.strip())
        for pp in current[start+1:end]:pp._p.getparent().remove(pp._p)
        an=current[start]
        for title in captions:
            node=OxmlElement('w:p');an._p.addnext(node);pp=Paragraph(node,an._parent);pp.style='CouncilTOC';pp.add_run(title+'\t—');an=pp
        changes.append({'rebuilt_caption_list':list_title,'entries':len(captions)})
    budget=json.loads((ROOT/'research/groq_study_20261118/FINAL_BUDGET.json').read_text())
    anchor=next(x for x in doc.paragraphs if x.style.name!='CouncilTOC' and x.text.startswith('4.10. Đánh giá mở rộng'))
    # These are bookkeeping estimates, clearly distinguished from a paid invoice.
    content=(f"Ngân sách toàn chiến dịch được giới hạn 3 USD. Sổ request ghi {budget['usage_requests_with_settlement']} response có usage, tổng {budget['prompt_tokens']:,} input token và {budget['completion_tokens']:,} output token; ước tính theo đơn giá đã ghi là {float(budget['settled_api_estimate_usd']):.6f} USD. Tổng phân bổ bảo thủ {budget['accounted_total_usd']:.6f} USD còn gồm khoản đặt trước chưa quyết toán và đối soát mốc 0,50 USD do người vận hành cung cấp. Hai số này không phải hai hóa đơn và không được cộng như hai khoản chi riêng. Ledger và FINAL_BUDGET.json lưu mọi request, cả sự cố cổng API; chưa có hóa đơn nhà cung cấp để khẳng định số tiền thanh toán thực tế.")
    node=OxmlElement('w:p');anchor._p.addnext(node);Paragraph(node,anchor._parent).add_run(content)
    usable=min(s.page_width-s.left_margin-s.right_margin for s in doc.sections)
    for shape in doc.inline_shapes:
        if shape.width>usable:
            scale=usable/shape.width;shape.width=int(usable);shape.height=int(shape.height*scale)
    for paragraph in doc.paragraphs:
        if paragraph._p.xpath('.//w:drawing'):
            paragraph.paragraph_format.first_line_indent=0
            paragraph.paragraph_format.left_indent=0
            paragraph.paragraph_format.right_indent=0
            paragraph.alignment=WD_ALIGN_PARAGRAPH.CENTER
    changes.extend(refresh_evidence_hashes(doc,a.input))
    a.output.parent.mkdir(parents=True,exist_ok=True);doc.save(a.output)
    if sha(a.input)!=before:raise RuntimeError('Input changed')
    a.output.with_suffix('.finalization.json').write_text(json.dumps({'input':str(a.input),'input_sha256':before,'input_unchanged':True,'output':str(a.output),'output_sha256':sha(a.output),'changes':changes,'budget_source':'research/groq_study_20261118/FINAL_BUDGET.json'},indent=2))
    print(a.output)


if __name__=='__main__':main()
