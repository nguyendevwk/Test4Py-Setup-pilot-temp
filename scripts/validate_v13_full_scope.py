"""Final report/data checks; visual approval flag is supplied after manual PDF review."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
from docx import Document
R=Path(__file__).resolve().parents[1];W=R/'research/groq_full_scope_20261119'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--visual-reviewed',action='store_true');a=p.parse_args()
 doc=R/'reports/Tieu_Luan_CNPMTT_Council_SOTA_v13.docx';pdf=R/'reports/rendered/Tieu_Luan_CNPMTT_Council_SOTA_v13.pdf';source=R/'reports/Tieu_Luan_CNPMTT_Council_SOTA_v12.docx';revision=load(doc.with_suffix('.revision.json'));assert sha(source)==revision['input_sha256']
 c=load(W/'completion.json');m=load(W/'manifest.json');s=load(W/'summary.json');st=load(W/'statistics.json');lock=load(W/'execution_manifest.json');assert c['complete'] and s['completed']==s['planned']==len(s['rows'])==st['completed']==3870
 assert sha(W/'manifest.json')==lock['manifest_sha256']
 for name,value in lock['implementation_sha256'].items():assert sha(R/name)==value,name
 if (W/'SCHEDULING_AMENDMENT.json').exists():
  for name,value in load(W/'SCHEDULING_AMENDMENT.json')['files_sha256'].items():assert sha(R/name)==value,name
 assert st['input_sha256']['manifest.json']==sha(W/'manifest.json') and st['input_sha256']['summary.json']==sha(W/'summary.json')
 for t in m['targets']:assert sha(Path(t['source_file_absolute']))==t['source_bytes_sha256']
 expected={(t['id'],seed,arm) for t in m['targets'] for seed in m['seed_values'] for arm in m['arms']};actual={(r['target_id'],r['seed'],r['arm']) for r in s['rows']};assert actual==expected
 d=Document(doc);old=Document(source);assert [p._p.xml for p in old.paragraphs[:28]]==[p._p.xml for p in d.paragraphs[:28]];assert [x._sectPr.xml for x in old.sections]==[x._sectPr.xml for x in d.sections]
 original=Path('/home/heurix/Downloads/Tieu_Luan_CNPMTT_Council_SOTA.docx');assert sha(original)=='9a90877d5fe8c78b56c307042bffd59243e0a90884eec813ef295f13078310d9'
 start=max(i for i,p in enumerate(d.paragraphs) if p.text=='MỞ ĐẦU');end=next(i for i,p in enumerate(d.paragraphs) if p.text=='TÀI LIỆU THAM KHẢO');main=d.paragraphs[start:end];body='\n'.join(p.text for p in main);alltext=body+'\n'+'\n'.join(c.text for t in d.tables for row in t.rows for c in row.cells)
 assert '{{' not in alltext
 assert not any(word in body for word in ['SYMBOL_GROUNDING_MAP','repair_audit','research/','SHA256'])
 assert len([p for p in main if p.style.name=='Heading 2' and re.match(r'^4\.\d+\.',p.text)])==7
 for arm,data in st['arms'].items():assert f"{data['successes']}/{data['denominator']}" in alltext,arm
 nav=subprocess.run(['uv','run','--no-project','--python','3.10','--with','python-docx','scripts/update_council_toc.py','--docx',str(doc),'--pdf',str(pdf),'--check-only'],cwd=R,capture_output=True,text=True);assert nav.returncode==0,nav.stderr
 info=subprocess.check_output(['pdfinfo',str(pdf)],text=True);pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1));scope=load(R/'research/editorial_v13/full_benchmark_scope.json');replay=load(R/scope['independent_replay_report']);assert replay['complete'] and replay['accepted_count']==sum(x['successes'] for x in st['arms'].values())
 budget=load(W/'budget.json');assert float(budget['accounted_total_usd'])<=3
 result=dict(final_docx=str(doc.relative_to(R)),final_pdf=str(pdf.relative_to(R)),word_sha256=sha(doc),pdf_sha256=sha(pdf),source_v12_sha256=sha(source),source_v12_unchanged=True,original_unchanged=True,cover_and_page_template_unchanged=True,pdf_pages=pages,visual_reviewed=a.visual_reviewed,main_chapter4_sections=7,toc_verification=nav.stdout.strip(),model_cases=3870,targets=645,modules=169,projects=21,arms=m['arms'],seed_values=m['seed_values'],source_post_replay_hashes_verified=True,frozen_code_verified=True,analysis_input_hashes_verified=True,independent_replay=dict(accepted=replay['accepted_count'],replayed=replay['replayed'],passed=replay['pass_count'],exact_coverage_matches=replay['exact_coverage_matches']),budget=budget,primary_contrast=st['contrasts']['context_setup-source'],scope_limit='Existing eligibility frame and already-observed projects, not complete original Test4Py or independent new-project validation')
 target=R/'reports/VALIDATION_v13.json';target.write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
