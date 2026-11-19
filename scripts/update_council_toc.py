"""Populate derived-report navigation from its actual rendered PDF pages."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata
from docx import Document

ROOT=Path(__file__).resolve().parents[1]


def normalize(text):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',text)).strip()


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--docx',type=Path,required=True);p.add_argument('--pdf',type=Path,required=True);p.add_argument('--check-only',action='store_true');a=p.parse_args()
    if not a.docx.resolve().is_relative_to(ROOT/'reports'):raise ValueError('Only derived workspace reports may be updated')
    before=hashlib.sha256(a.docx.read_bytes()).hexdigest()
    pages=subprocess.check_output(['pdftotext','-layout',str(a.pdf),'-'],text=True).split('\f')
    doc=Document(a.docx);mapping={};unmatched=[]
    for paragraph in doc.paragraphs:
        if paragraph.style.name!='CouncilTOC':continue
        title=paragraph.text.split('\t')[0]
        matches=[]
        for i,page in enumerate(pages):
            if normalize(title) in normalize(page):
                footer=re.search(r'\n\s*(\d+)\s*$',page)
                matches.append(int(footer.group(1)) if footer else i+1)
        if not matches:unmatched.append(title);continue
        number=matches[-1];mapping[title]=number
        if a.check_only:
            if paragraph.text.rsplit('\t',1)[-1]!=str(number):unmatched.append('page mismatch: '+title)
        else:paragraph.text=title+'\t'+str(number)
    if unmatched:raise ValueError('Unresolved navigation: '+json.dumps(unmatched,ensure_ascii=False))
    if not a.check_only:
        doc.save(a.docx)
        a.docx.with_suffix('.navigation.json').write_text(json.dumps({'docx_sha256_before':before,'docx_sha256_after':hashlib.sha256(a.docx.read_bytes()).hexdigest(),'pdf_reference':str(a.pdf),'page_map':mapping,'method':'last exact normalized heading occurrence; actual printed footer when available'},ensure_ascii=False,indent=2))
    print('Navigation entries verified' if a.check_only else 'Navigation entries updated',len(mapping))


if __name__=='__main__':main()
