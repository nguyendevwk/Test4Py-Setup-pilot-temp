"""Finish the authorized study only after complete immutable generation evidence."""
import fcntl,hashlib,json,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1];W=R/'research/groq_full_scope_20261119';PY=R/'.venv/bin/python'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def phase(name,**data):(W/'postprocess_progress.json').write_text(json.dumps(dict(phase=name,at=time.time(),**data),indent=2))
def run(name,cmd,allowed=(0,)):
 phase(name);p=subprocess.run([str(x) for x in cmd],cwd=R,capture_output=True,text=True);(W/(name+'.stdout.txt')).write_text(p.stdout);(W/(name+'.stderr.txt')).write_text(p.stderr)
 if p.returncode not in allowed:raise RuntimeError(name+' failed; inspect saved logs')
 return p

def main():
 with (W/'.postprocess.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  phase('waiting_for_generation')
  while True:
   if (W/'completion.json').exists():
    c=read(W/'completion.json')
    if c.get('complete') and c.get('completed')==3870:break
    # A resumed generation may have a historical incomplete completion receipt.
    with (W/'.runner.lock').open('rb') as generation:
     try:fcntl.flock(generation,fcntl.LOCK_SH|fcntl.LOCK_NB)
     except BlockingIOError:pass
     else:raise RuntimeError('Generation is stopped incomplete; final inference refused')
   time.sleep(10)
  lockdata=read(W/'execution_manifest.json')
  for name,value in lockdata['implementation_sha256'].items():assert sha(R/name)==value,'Frozen implementation changed: '+name
  assert sha(W/'manifest.json')==lockdata['manifest_sha256']
  if (W/'SCHEDULING_AMENDMENT.json').exists():
   for name,value in read(W/'SCHEDULING_AMENDMENT.json')['files_sha256'].items():assert sha(R/name)==value,'Scheduling implementation changed'
  for t in read(W/'manifest.json')['targets']:assert sha(Path(t['source_file_absolute']))==t['source_bytes_sha256']
  run('final_statistics',[PY,'scripts/analyze_groq_full_scope.py'])
  if not (W/'budget.json').exists():run('final_budget',[PY,'scripts/snapshot_groq_budget.py','--output',W/'budget.json','--prefix','full_scope__'])
  run('independent_replay',[PY,'scripts/replay_groq_full_scope.py','--output-root',W/'independent_replays/full_audit','--workers','6'],allowed=(0,1))
  run('joint_pack_evaluation',[PY,'scripts/assemble_groq_full_packs.py','--output-root',W/'joint_packs/main','--workers','2'],allowed=(0,1))
  run('resolve_report_text',[PY,'scripts/fill_v13_full_scope_text.py'])
  run('build_report',['uv','run','--no-project','--python','3.10','--with','python-docx','--with','matplotlib','scripts/build_v13_full_scope_report.py'])
  doc=R/'reports/Tieu_Luan_CNPMTT_Council_SOTA_v13.docx';pdf=R/'reports/rendered/Tieu_Luan_CNPMTT_Council_SOTA_v13.pdf'
  render=['libreoffice','-env:UserInstallation=file:///tmp/council-v13-full-render','--headless','--convert-to','pdf','--outdir',pdf.parent,doc]
  run('render_initial',render)
  toc=['uv','run','--no-project','--python','3.10','--with','python-docx','scripts/update_council_toc.py','--docx',doc,'--pdf',pdf]
  run('navigation_update',toc);run('render_final',render);run('navigation_check',toc+['--check-only'])
  phase('report_ready_for_visual_review',docx=str(doc),pdf=str(pdf),docx_sha256=sha(doc),pdf_sha256=sha(pdf))
  print('Complete3870-case analysis, replay and v13 report ready for final review',flush=True)
if __name__=='__main__':
 try:main()
 except Exception as exc:
  phase('interrupted',reason=str(exc));raise
