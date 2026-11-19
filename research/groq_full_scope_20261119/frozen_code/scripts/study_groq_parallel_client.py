"""Concurrent transport with short ledger locks and explicit rolling RPM/TPM caps."""
import fcntl,hashlib,json,math,os,time,uuid,urllib.request,urllib.error
from decimal import Decimal
import study_groq_client as base

class ParallelStudyClient(base.StudyClient):
 def __init__(self,*args,rpm=1000,tpm=250000,**kwargs):
  super().__init__(*args,**kwargs)
  if not 0<rpm<=1000 or not 0<tpm<=250000:raise ValueError('Rate limits exceed authorized caps')
  self.rpm=rpm;self.tpm=tpm;self._events_cache=None;self._events_signature=None;self.state_path=self.work/'parallel_rate_state.json'
 def events(self):
  stat=self.ledger.stat() if self.ledger.exists() else None;sig=(stat.st_size,stat.st_mtime_ns) if stat else None
  if self._events_cache is None or sig!=self._events_signature:
   self._events_cache=[json.loads(l) for l in self.ledger.read_text().splitlines()] if stat else [];self._events_signature=sig
  return self._events_cache
 def state(self):return json.loads(self.state_path.read_text()) if self.state_path.exists() else {}
 def save_state(self,state):
  p=self.state_path.with_name(self.state_path.name+'.'+uuid.uuid4().hex+'.tmp');p.write_bytes(base._json(state));os.replace(p,self.state_path)
 def limits(self,events,needed,now):
  reserves={};settles={}
  for e in events:
   if e['event']=='reserve':reserves[e['id']]=e
   else:settles[e['id']]=e
  balance=sum((Decimal(settles.get(rid,e)['charge_usd']) for rid,e in reserves.items()),Decimal(0))
  recent=[]
  for rid,e in reserves.items():
   sent=e.get('requested_at',0)
   if sent+60<=now:continue
   u=settles.get(rid,{}).get('usage')
   if u:
    cached=(u.get('prompt_tokens_details') or {}).get('cached_tokens',0) or 0
    tokens=max(0,u['prompt_tokens']-cached)+u['completion_tokens']
   else:tokens=e.get('rate_token_bound',e['input_token_bound']+e['max_tokens'])
   recent.append((sent,tokens,rid))
  recent.sort();deadline=now
  if len(recent)>=self.rpm:deadline=max(deadline,recent[len(recent)-self.rpm][0]+60)
  total=sum(t for _,t,_ in recent)+needed
  for sent,tokens,_ in recent:
   if total<=self.tpm:break
   deadline=max(deadline,sent+60);total-=tokens
  state=self.state();deadline=max(deadline,state.get('cooldown_until',0));headers=state.get('headers',{});received=state.get('received_at',0)
  for resource,amount in [('requests',1),('tokens',needed)]:
   try:remaining=float(headers['x-ratelimit-remaining-'+resource])
   except (KeyError,ValueError,TypeError):continue
   reset=base._delay(headers.get('x-ratelimit-reset-'+resource),received)
   after=sum(tokens if resource=='tokens' else 1 for sent,tokens,rid in recent if sent>received and rid not in settles)
   if now<received+reset and remaining<amount+after:deadline=max(deadline,received+reset)
  return balance,deadline,recent
 def call(self,messages,seed,label):
  key=base._key();payload=dict(model=self.model,messages=messages,seed=seed,max_tokens=self.max_tokens,temperature=.2)
  if self.model.startswith('openai/gpt-oss-'):payload['reasoning_effort']='low'
  body=base._json(payload)
  if key.encode() in body or key in label:raise ValueError('Request contains API credential')
  # Byte-level token upper bound for content plus framing. Cost uses the older, larger bound.
  input_bound=2*len(body)+4096;rate_bound=len(body)+256+self.max_tokens
  if rate_bound>self.tpm:raise ValueError('Single request exceeds configured token admission cap')
  charge=(input_bound*self.input_price+self.max_tokens*self.output_price)/1000000
  while True:
   with (self.work/'.lock').open('a') as lock:
    fcntl.flock(lock,fcntl.LOCK_EX);now=time.time();balance,deadline,_=self.limits(self.events(),rate_bound,now)
    if balance+charge>self.budget:raise base.BudgetExceeded('Conservative reservation would exceed cumulative3USD')
    if deadline<=now:
     rid=uuid.uuid4().hex;base._write(self.work/(rid+'.request.json'),body)
     self._append(dict(event='reserve',id=rid,label=label,requested_at=now,charge_usd=str(charge),model=self.model,input_token_bound=input_bound,rate_token_bound=rate_bound,max_tokens=self.max_tokens,input_price_per_million=str(self.input_price),output_price_per_million=str(self.output_price),price_source=base.PRICE_SOURCE,pricing='configured estimate',request_sha256=hashlib.sha256(body).hexdigest(),transport='parallel_short_ledger_lock',rpm_cap=self.rpm,tpm_cap=self.tpm))
     break
   time.sleep(min(.25,max(.01,deadline-time.time())))
  req=urllib.request.Request(base.ENDPOINT,data=body,headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','Accept':'application/json','User-Agent':base.USER_AGENT});http_error=False
  try:
   with urllib.request.urlopen(req,timeout=120) as response:status=getattr(response,'status',None) or 200;headers=response.headers;raw=response.read()
  except urllib.error.HTTPError as exc:status=exc.code;headers=exc.headers or {};raw=exc.read();http_error=True
  except Exception:raise RuntimeError('Uncertain Groq transport; reservation retained, no automatic retry') from None
  raw=raw.replace(key.encode(),b'[REDACTED]');base._write(self.work/(rid+'.response.json'),raw);received=time.time();safe={str(n).lower():str(v).replace(key,'[REDACTED]') for n,v in headers.items() if str(n).lower().startswith('x-ratelimit') or str(n).lower()=='retry-after'};response_sha=hashlib.sha256(raw).hexdigest()
  base._write(self.work/(rid+'.response.meta.json'),base._json(dict(id=rid,http_status=status,http_error=http_error,received_at=received,headers=safe,response_sha256=response_sha,response_bytes=len(raw),content_type=str(headers.get('Content-Type','')),transport='parallel_short_ledger_lock')))
  retry=base._delay(safe.get('retry-after'),received)
  if status==429 and not retry:retry=max([1]+[base._delay(v,received) for n,v in safe.items() if n.startswith('x-ratelimit-reset-')])
  with (self.work/'.lock').open('a') as lock:
   fcntl.flock(lock,fcntl.LOCK_EX);state=self.state()
   if received>=state.get('received_at',0):state.update(headers=safe,received_at=received)
   if retry:state['cooldown_until']=max(state.get('cooldown_until',0),received+retry)
   self.save_state(state)
   try:
    result=json.loads(raw);usage=result.get('usage',{});values=[usage.get('prompt_tokens'),usage.get('completion_tokens')]
    if all(type(v) is int and v>=0 for v in values):
     cost=(values[0]*self.input_price+values[1]*self.output_price)/1000000;self._append(dict(event='settle',id=rid,charge_usd=str(cost),usage=usage,http_status=status,response_sha256=response_sha))
   except (ValueError,TypeError):result=None
  if status==429:raise base.RateLimited(retry)
  try:
   if http_error or not result:raise ValueError('Provider error')
   choice=result['choices'][0];result.update(content=choice['message'].get('content'),finish_reason=choice.get('finish_reason'),http_status=status,usage=usage,_internal_request_id=rid);return result
  except Exception:raise RuntimeError(f'Groq response invalid HTTP{status}; inspect persisted artifacts; no retry') from None
