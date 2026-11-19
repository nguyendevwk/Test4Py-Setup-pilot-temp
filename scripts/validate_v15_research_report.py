"""Validate the v15 research revision against preserved evidence and v14."""
import hashlib,json,re,subprocess
from pathlib import Path
from docx import Document
R=Path(__file__).resolve().parents[1];D=R/'research/editorial_v15';P=R/'reports';W=R/'research/groq_full_scope_20261119'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=P/'Tieu_Luan_CNPMTT_Council_SOTA_v14.docx';b=P/'Tieu_Luan_CNPMTT_Council_SOTA_v15.docx';pdf=P/'rendered'/b.with_suffix('.pdf').name
old=json.loads((P/'VALIDATION_v14.json').read_text());assert sha(a)==old['docx_sha256']
assert sha(Path('/home/heurix/Downloads/Tieu_Luan_CNPMTT_Council_SOTA.docx'))=='9a90877d5fe8c78b56c307042bffd59243e0a90884eec813ef295f13078310d9'
x,y=Document(a),Document(b)
assert [v._sectPr.xml for v in x.sections]==[v._sectPr.xml for v in y.sections]
# Preserve all cover/front text before the research body, excluding derived lists.
def cover(d):
 out=[]
 for p in d.paragraphs:
  if p.text=='LỜI CẢM ƠN':break
  out.append(p.text)
 return out
assert cover(x)==cover(y)
body=(D/'report_body.md').read_text();assert '{{' not in body
h=re.findall(r'^## (4\.\d+)\.',body,re.M);assert h==['4.'+str(i) for i in range(1,8)]
assert len(re.findall(r'^@table .*\| Bảng 3\.',body,re.M))==5
assert len(re.findall(r'^@table .*\| Bảng 4\.',body,re.M))==7
text='\n'.join(p.text for p in y.paragraphs)
for v in ['159','114','753','10 giây','20 giây','21 dự án mã nguồn mở bên ngoài','Phân tích hậu kiểm','3.870','645','169']:assert v in text,v
# Full primary empirical tables survive byte-equivalent cell text.
tables=[[c.text for row in t.rows for c in row.cells] for t in y.tables]
for t in x.tables:
 cells=[c.text for row in t.rows for c in row.cells]
 if '378/1290' in cells or '0,34644' in cells or '0,259993' in cells:assert cells in tables
from v15_research_tables import additional_tables
extra=additional_tables(R,lambda v,d=2:f'{v:.{d}f}'.replace('.',','))
assert len(extra['subgroups'])==11
for ci in range(1,4):assert sum(row[ci] for row in extra['failure_stages'][1:])==1290
for row in extra['paired'][1:]:assert sum(row[1:])==1290
analysis=json.loads((D/'deep_analysis.json').read_text())
for name,digest in analysis['input_sha256'].items():assert sha(R/name)==digest,name
assert json.loads((W/'completion.json').read_text())['complete']
for name,digest in json.loads((D/'evidence_manifest_v15.json').read_text()).items():assert sha(R/name)==digest,name
subprocess.run(['uv','run','--no-project','--python','3.10','--with','python-docx',str(R/'scripts/update_council_toc.py'),'--docx',str(b),'--pdf',str(pdf),'--check-only'],check=True)
pages=subprocess.check_output(['pdfinfo',str(pdf)],text=True);n=int(re.search(r'Pages:\s*(\d+)',pages).group(1))
record=dict(version='v15',final_docx=str(b),final_pdf=str(pdf),docx_sha256=sha(b),pdf_sha256=sha(pdf),previous_version_unchanged=True,original_unchanged=True,cover_and_section_settings_preserved=True,complete_experiment_retained=3870,raw_input_hashes_verified=len(analysis['input_sha256']),primary_empirical_tables_unchanged=True,main_chapter4_sections=7,tables=len(y.tables),pages=n,additional_analyses='Exploratory posthoc; all cases and strata retained',model_api_calls_this_revision=0)
(P/'VALIDATION_v15.json').write_text(json.dumps(record,ensure_ascii=False,indent=2));print(json.dumps(record,ensure_ascii=False,indent=2))
