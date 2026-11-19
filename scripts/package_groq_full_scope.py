"""Immutable supplemental bundle; prior v4 supplies pinned production environments."""
import argparse,fcntl,hashlib,json,re,sys,tempfile,os,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];W=R/'research/groq_full_scope_20261119'
def digest(data):return hashlib.sha256(data).hexdigest()
def load(p):return json.loads(p.read_text())
def verify(path):
 with zipfile.ZipFile(path) as z:
  names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
  entries={line.split('  ',1)[1]:line.split('  ',1)[0] for line in z.read('MANIFEST.sha256').decode().splitlines()}
  assert set(entries)==set(names)-{'MANIFEST.sha256'}
  for name,value in entries.items():
   assert not Path(name).is_absolute() and '..' not in Path(name).parts
   assert digest(z.read(name))==value,name
 return len(names)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=R/'deliverables/council_full_scope_20261119_v1.zip');p.add_argument('--verify',type=Path);a=p.parse_args()
 if a.verify:print('Verified members',verify(a.verify));return
 assert not a.output.exists(),'Existing bundle preserved'
 c=load(W/'completion.json');s=load(W/'summary.json');m=load(W/'manifest.json');assert c['complete'] and s['completed']==s['planned']==len(s['rows'])==3870
 expected={(t['id'],seed,arm) for t in m['targets'] for seed in m['seed_values'] for arm in m['arms']};actual={(r['target_id'],r['seed'],r['arm']) for r in s['rows']};assert actual==expected
 validation=load(R/'reports/VALIDATION_v13.json');assert validation['visual_reviewed'];doc=R/validation['final_docx'];pdf=R/validation['final_pdf'];assert digest(doc.read_bytes())==validation['word_sha256'] and digest(pdf.read_bytes())==validation['pdf_sha256']
 base=R/'deliverables/council_repro_20261119_v4.zip';basehash=digest(base.read_bytes());files={}
 def add(path):
  if path.is_file() and not path.is_symlink():files[path.relative_to(R).as_posix()]=path
 for path in W.rglob('*'):
  if any(part in {'__pycache__','.venv','venv'} for part in path.relative_to(W).parts):continue
  if path.suffix in {'.json','.jsonl','.py','.txt','.md','.log','.stdout','.stderr'} or path.name=='.runner.lock':add(path)
 for path in (R/'research/editorial_v13').rglob('*'):add(path)
 for name in ['prepare_groq_full_scope.py','run_groq_full_scope.py','run_groq_full_scope_parallel.py','study_groq_parallel_client.py','analyze_groq_full_scope.py','replay_groq_full_scope.py','assemble_groq_full_packs.py','finish_groq_full_scope.py','snapshot_groq_budget.py','prepare_v13_full_scope_text.py','fill_v13_full_scope_text.py','build_v13_full_scope_report.py','package_groq_full_scope.py','validate_v13_full_scope.py','study_groq_client.py','run_groq_study.py','polish_council_report.py','revise_kaggle_groq_narrative.py','update_council_toc.py']:add(R/'scripts'/name)
 for name,value in load(W/'execution_manifest.json')['implementation_sha256'].items():
  assert digest((R/name).read_bytes())==value;add(R/name)
 for path in (R/'tests').glob('test_groq_full_scope*.py'):add(path)
 for version in ['v11','v12','v13']:
  add(R/'reports'/('Tieu_Luan_CNPMTT_Council_SOTA_'+version+'.docx'))
 for path in (R/'reports').glob('*v13*'):
  if path.is_file():add(path)
 for path in (R/'reports/Tieu_Luan_CNPMTT_Council_SOTA_v13_assets').glob('*'):add(path)
 add(pdf);add(R/'reports/VALIDATION_v13.json');add(R/'reports/START_HERE.md');add(R/'research/REPRODUCIBILITY_FULL_SCOPE.md')
 api=R/'research/groq_study_20261118/api'
 with (api/'.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_SH);ledger=(api/'ledger.jsonl').read_bytes()
  events=[json.loads(line) for line in ledger.decode().splitlines()];ids={e['id'] for e in events if e['event']=='reserve' and e.get('label','').startswith('full_scope__')}
  with zipfile.ZipFile(base) as z:oldledger=z.read('research/groq_study_20261118/api/ledger.jsonl')
  assert ledger.startswith(oldledger),'Shared ledger history changed'
 for rid in ids:
  for path in api.glob(rid+'.*'):add(path)
 extra={'research/groq_study_20261118/api/ledger.jsonl':ledger,'repro/FULL_SCOPE_BASE.json':(json.dumps(dict(required_prior_bundle=base.name,required_prior_sha256=basehash,scope='Supplemental layer; extract verified v4 first, then this layer for complete sources and pinned environments',base_ledger_sha256=digest(oldledger),current_ledger_sha256=digest(ledger),ledger_history_is_append_only=True,model_cases=3870),indent=2)+'\n').encode()}
 try:
  from study_groq_client import _key
  key=_key().encode()
 except RuntimeError:key=None
 a.output.parent.mkdir(exist_ok=True);checksums={}
 with tempfile.NamedTemporaryFile(dir=a.output.parent,suffix='.zip',delete=False) as temp:temporary=Path(temp.name)
 try:
  with zipfile.ZipFile(temporary,'w',zipfile.ZIP_DEFLATED) as z:
   for name,path in sorted(files.items()):
    data=path.read_bytes()
    if key and key in data:raise ValueError('Credential found in whitelisted artifact; package refused: '+name)
    z.writestr(name,data);checksums[name]=digest(data)
   for name,data in extra.items():z.writestr(name,data);checksums[name]=digest(data)
   z.writestr('MANIFEST.sha256',''.join(value+'  '+name+'\n' for name,value in sorted(checksums.items())))
  count=verify(temporary);os.link(temporary,a.output)
 finally:temporary.unlink(missing_ok=True)
 print(json.dumps(dict(output=str(a.output),members=count,bytes=a.output.stat().st_size,sha256=digest(a.output.read_bytes()),required_base=base.name,required_base_sha256=basehash),indent=2))
if __name__=='__main__':main()
