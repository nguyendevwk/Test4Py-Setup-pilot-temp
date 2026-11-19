"""Freeze all eligible stored symbols before full three-arm Groq evaluation."""
import ast,concurrent.futures,hashlib,json,os,signal,subprocess,time
from collections import defaultdict,deque
from pathlib import Path
from run_groq_development import ATOMIC

R=Path(__file__).resolve().parents[1];W=R/'research/groq_full_scope_20261119'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,j):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,indent=2,ensure_ascii=False))
PROBE='''import importlib,inspect,json
obj=getattr(importlib.import_module(MODULE),SYMBOL);sig=inspect.signature(obj);kw={}
for name,p in sig.parameters.items():
 if p.default is not inspect.Parameter.empty or p.kind in (p.VAR_POSITIONAL,p.VAR_KEYWORD):continue
 if p.kind==p.POSITIONAL_ONLY:raise ValueError('unsupported positional-only')
 if name in ('f','fn','func','function','callback','mapper'):v=lambda *args:1
 elif name.startswith('is_') or p.annotation is bool:v=False
 elif name in ('errors','items','values','rules'):v=[]
 else:v=1
 kw[name]=v
obj(**kw)
print('COUNCIL_SETUP_SIGNATURE_JSON='+json.dumps({'signature':str(sig),'arguments':{k:('lambda *args: 1' if callable(v) else repr(v)) for k,v in kw.items()},'scope':'call completed; no method precondition or oracle guarantee'}))
'''
def prepare_one(t):
 dest=W/'preparation'/t['id'];dest.mkdir(parents=True,exist_ok=False);env={'PATH':os.environ.get('PATH','/usr/bin:/bin'),'HOME':str(dest),'TMPDIR':str(dest),'LANG':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'}
 script=PROBE.replace('MODULE',repr(t['module'])).replace('SYMBOL',repr(t['symbol']))
 p=subprocess.Popen([t['python'],'-c',script],cwd=dest,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 try:stdout,stderr=p.communicate(timeout=10);timed=False
 except subprocess.TimeoutExpired:
  os.killpg(p.pid,signal.SIGKILL);stdout,stderr=p.communicate();timed=True
 (dest/'stdout.txt').write_bytes(stdout);(dest/'stderr.txt').write_bytes(stderr)
 hints=[line[len('COUNCIL_SETUP_SIGNATURE_JSON='):] for line in stdout.decode(errors='replace').splitlines() if line.startswith('COUNCIL_SETUP_SIGNATURE_JSON=')]
 accepted=p.returncode==0 and not timed and len(hints)==1
 t['setup_probe']=dict(accepted=accepted,returncode=p.returncode,timeout=timed,hint_json=hints[0] if accepted else '',scope='Only signature and arguments enter prompt; incidental program stdout and return values excluded')
 write(dest/'probe.json',t['setup_probe']);return t

def closure(t):
 source=Path(t['source_file_absolute']).read_text();tree=ast.parse(source);symbols={}
 for n in tree.body:
  names=[n.name] if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef)) else [x.id for x in ast.walk(n) if isinstance(x,ast.Name) and isinstance(x.ctx,ast.Store)] if isinstance(n,(ast.Assign,ast.AnnAssign)) else []
  for name in names:symbols[name]=n
 target=symbols[t['symbol']];pending={n.id for n in ast.walk(target) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)};seen={t['symbol']};parts=[];names=[];size=0
 for depth in range(2):
  nextnames=set()
  for name in sorted(pending):
   if name in seen or name not in symbols:continue
   seen.add(name);node=symbols[name];excerpt=ast.get_source_segment(source,node)
   if len(excerpt)>4000 or size+len(excerpt)>8000:continue
   parts.append(excerpt);names.append(name);size+=len(excerpt);nextnames.update(n.id for n in ast.walk(node) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load))
  pending=nextnames
 fns=[target] if isinstance(target,(ast.FunctionDef,ast.AsyncFunctionDef)) else [n for n in target.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
 t.update(context_closure='\n\n'.join(parts),context_closure_names=names,context_closure_characters=size,body_lines=sorted({n.lineno for fn in fns for stmt in fn.body for n in ast.walk(stmt) if isinstance(n,ast.stmt) and not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}))
 return t

def main():
 if W.exists():raise FileExistsError('Full study directory already exists; preserve it')
 W.mkdir();old=set();inputs={};targets=[];projects=[]
 for name in ['groq_confirmation_20261118','groq_codamosa_extension_20261119']:
  root=R/'research'/name;m=json.loads((root/'manifest.json').read_text());old.update(t['id'] for t in m['targets']);inputs[str((root/'manifest.json').relative_to(R))]=sha(root/'manifest.json')
  for p in sorted((root/'environments').glob('*/inventory.json')):
   j=json.loads(p.read_text());inputs[str(p.relative_to(R))]=sha(p);project=p.parent.name;projects.append(dict(project=project,version=j['version'],candidate_count=len(j['candidates']),site=j['site'],python=str(p.parent/'venv/bin/python'),packages=j['packages'],pre_inference_import_errors=j.get('errors',[])))
   for candidate in j['candidates']:
    t=dict(candidate,project=project,root=j['site'],source_file_absolute=candidate['file'],python=str(p.parent/'venv/bin/python'),id=project+'__'+candidate['module']+'__'+candidate['symbol'])
    assert hashlib.sha256(Path(t['file']).read_text().encode()).hexdigest()==t['source_sha256']
    t['source_bytes_sha256']=sha(Path(t['file']));targets.append(closure(t))
 assert len(targets)==len({t['id'] for t in targets})==645
 for t in targets:t['prior_normalized_evaluation']=t['id'] in old
 # Round-robin projects; arm order will also rotate within each target/seed.
 queues={p:deque(sorted([t for t in targets if t['project']==p],key=lambda t:hashlib.sha256(t['id'].encode()).hexdigest())) for p in sorted({t['project'] for t in targets})};ordered=[]
 while any(queues.values()):
  for q in queues.values():
   if q:ordered.append(q.popleft())
 write(W/'PREPARATION_PLAN.json',dict(planned_targets=645,eligible_projects=len(queues),eligible_modules=len({(t['project'],t['module']) for t in ordered}),source_inventory_sha256=inputs,preparer_sha256=sha(Path(__file__)),planned_calls=3870,arms=['source','verified_setup','context_setup'],seed_values=[71,72],rules=ATOMIC,created_at=time.time(),no_model_inference_yet=True))
 results={}
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  for i,t in enumerate(pool.map(prepare_one,ordered),1):
   results[t['id']]=t
   if i%25==0:print('Prepared',i,'/645',flush=True)
 ordered=[results[t['id']] for t in ordered]
 for t in ordered:assert sha(Path(t['source_file_absolute']))==t['source_bytes_sha256']
 manifest=dict(status='locked_full_eligibility_frame_three_arm_component_evaluation',design='All645 public source-eligible symbols across169 modules/21 already-observed projects; no model-outcome target filtering; paired3arms2seeds; no repairs',model='openai/gpt-oss-20b',arms=['source','verified_setup','context_setup'],seed_values=[71,72],planned=3870,rules=ATOMIC,repair_rounds=0,max_completion_tokens=2048,temperature=.2,reasoning_effort='low',cumulative_budget_usd=3,targets=ordered,projects=projects,primary_contrast=['context_setup','source'],secondary_contrasts=[['verified_setup','source'],['context_setup','verified_setup']],analysis_plan='Equal-project paired differences;20k paired project bootstrap seed20261119; exact cluster signflip; Holm across2secondary pvalues; no interim significance stopping or older-cohort pooling',prior_normalized_targets=sum(t['prior_normalized_evaluation'] for t in ordered),new_to_normalized_targets=sum(not t['prior_normalized_evaluation'] for t in ordered),project_scope='All21 projects already observed locally; target novelty is not project-held-out confirmation; four projects also overlap historical105 development',source_scope='Resolved PyPI releases and published module frames, not original complete Test4Py183module pipeline or original CodaMOSA Docker benchmark',preparation_plan_sha256=sha(W/'PREPARATION_PLAN.json'),prepared_at=time.time(),execution_environment='Pinned per-project Python3.10; minimal credential-free subprocess env, isolated cwd/HOME/TMPDIR; process isolation not OS sandbox',endpoint='Exactly3 test functions, static gate, all-pass, positive module coverage,target-body witness,same-coverage replay; passing not oracle proof')
 with (W/'manifest.json').open('x') as f:json.dump(manifest,f,indent=2,ensure_ascii=False)
 print(json.dumps(dict(targets=len(ordered),projects=len(queues),setup_probe_accepted=sum(t['setup_probe']['accepted'] for t in ordered),closure_available=sum(bool(t['context_closure']) for t in ordered),planned=3870)),flush=True)
if __name__=='__main__':main()
