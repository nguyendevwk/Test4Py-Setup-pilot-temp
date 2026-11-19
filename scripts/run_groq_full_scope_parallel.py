"""User-directed scheduling amendment; frozen evaluator/payload/targets unchanged."""
import concurrent.futures,fcntl,json,threading,time
from pathlib import Path
import run_groq_full_scope as old
from study_groq_parallel_client import ParallelStudyClient
from study_groq_client import RateLimited
W=old.W;STOP=threading.Event();COUNTER=threading.Lock()
def jobs(m):
 for ti,t in enumerate(m['targets']):
  for si,seed in enumerate(m['seed_values']):
   arms=m['arms'][:];shift=(ti+si)%len(arms);arms=arms[shift:]+arms[:shift]
   if (ti+si)%2:arms=arms[::-1]
   for arm in arms:
    label=t['id']+'__'+str(seed)+'__'+arm;dest=W/'attempts'/label
    if not (dest/'outcome.json').exists():yield t,seed,arm,label,dest

def get_response(client,m,job):
 t,seed,arm,label,dest=job
 if STOP.is_set():return None
 if (dest/'inference.json').exists():return job
 if dest.exists() and old.recover_inference(label,dest):return job
 dest.mkdir(parents=True,exist_ok=True)
 context='Module '+t['module']+' target '+t['symbol']+'\n'+t['source']
 if arm in ['verified_setup','context_setup'] and t['setup_probe']['accepted']:context+='\nRuntime signature and successfully executed setup arguments (NOT expected results):\n'+t['setup_probe']['hint_json']
 if arm=='context_setup' and t['context_closure']:context+='\nAdditional bounded production helper/global declarations (source evidence, NOT expected test results):\n'+t['context_closure']
 start=time.monotonic()
 for attempt in range(5):
  if STOP.is_set():return None
  try:r=client.call([{'role':'system','content':m['rules']},{'role':'user','content':context}],seed=seed,label='full_scope__'+label);break
  except RateLimited as exc:
   old.write(dest/('api_incident_'+str(time.time_ns())+'.json'),dict(kind='RateLimited',retry_after=exc.retry_after,occurred_at=time.time(),phase='parallel',attempt=attempt+1,scope='Known rejected request, no model output; reservation retained'))
   time.sleep(max(1,exc.retry_after)+.25)
 else:raise RuntimeError('Repeated429 needs review; results preserved')
 r['_api_plus_pacing_seconds']=time.monotonic()-start;old.write(dest/'inference.json',r);return job

def main():
 with (W/'.runner.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  m=old.read(W/'manifest.json');frozen=old.read(W/'execution_manifest.json')
  assert old.sha(W/'manifest.json')==frozen['manifest_sha256']
  for name,value in frozen['implementation_sha256'].items():assert old.sha(old.ROOT/name)==value
  todo=list(jobs(m));before=old.summarize(m)['completed'];amend=W/'SCHEDULING_AMENDMENT.json'
  spec=dict(user_authorized=True,reason='User requested up to1000RPM/250000TPM; serial HTTP lock was transport bottleneck',recorded_at=time.time(),completed_before_phase=before,remaining_cases=len(todo),request_cap_per_minute=1000,token_cap_per_minute=250000,http_workers=8,local_eval_workers=6,cumulative_budget_usd=3,manifest_sha256=old.sha(W/'manifest.json'),frozen_evaluator_unchanged=True,endpoint_payload_seeds_targets_unchanged=True,files_sha256={str(p.relative_to(old.ROOT)):old.sha(p) for p in [Path(__file__),old.ROOT/'scripts/study_groq_parallel_client.py']},remaining_case_ids=[j[3] for j in todo],scope='Scheduling/throughput amendment only; previous outcomes immutable; no outcome-driven sample change')
  if amend.exists():
   previous=old.read(amend)
   for name,value in previous['files_sha256'].items():assert old.sha(old.ROOT/name)==value
  else:old.write(amend,spec)
  client=ParallelStudyClient(old.API,budget_usd=3,max_tokens=2048,rpm=1000,tpm=250000);completed=before;errors=[];pending_eval=[]
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as api_pool, concurrent.futures.ThreadPoolExecutor(max_workers=6) as eval_pool:
   api_jobs={api_pool.submit(get_response,client,m,job):job for job in todo}
   for f in concurrent.futures.as_completed(api_jobs):
    try:
     job=f.result()
     if job is not None:
      t,seed,arm,label,dest=job;pending_eval.append(eval_pool.submit(old.evaluate,t,seed,arm,dest))
    except Exception as exc:
     STOP.set();errors.append(dict(stage='provider',case=api_jobs[f][3],kind=type(exc).__name__,message=str(exc)[:500]));old.write(W/'parallel_interruption.json',dict(errors=errors,at=time.time()))
    ready=[e for e in pending_eval if e.done()]
    for e in ready:
     pending_eval.remove(e)
     try:e.result();completed+=1
     except Exception as exc:STOP.set();errors.append(dict(stage='evaluation',kind=type(exc).__name__,message=str(exc)[:500]))
    if ready and completed%25< len(ready):
     data=old.summarize(m);print(json.dumps(dict(completed=data['completed'],planned=3870,phase='parallel',pending_evaluations=len(pending_eval),at=time.time())),flush=True)
   for e in concurrent.futures.as_completed(pending_eval):
    try:e.result();completed+=1
    except Exception as exc:errors.append(dict(stage='evaluation',kind=type(exc).__name__,message=str(exc)[:500]))
    if completed%25==0:
     data=old.summarize(m);print(json.dumps(dict(completed=data['completed'],planned=3870,phase='evaluation_drain',at=time.time())),flush=True)
  data=old.summarize(m);old.write(W/'completion.json',dict(complete=data['completed']==3870 and not errors,completed=data['completed'],planned=3870,accounted_total_usd=client.spent_usd,phase='parallel_user_authorized',errors=errors,at=time.time()));print(json.dumps(old.read(W/'completion.json')),flush=True)
  if errors:raise SystemExit(2)
if __name__=='__main__':main()
