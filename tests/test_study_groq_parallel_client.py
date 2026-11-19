import concurrent.futures,json,sys,threading
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import study_groq_parallel_client as mod

def test_short_lock_allows_overlapping_http_and_retains_budget(tmp_path,monkeypatch):
 barrier=threading.Barrier(2);monkeypatch.setattr(mod.base,'_key',lambda:'unit-test-key')
 class Response:
  status=200;headers={'Content-Type':'application/json'}
  def __enter__(self):barrier.wait(timeout=5);return self
  def __exit__(self,*args):pass
  def read(self):return json.dumps(dict(choices=[dict(message=dict(content='unit fixture'),finish_reason='stop')],usage=dict(prompt_tokens=10,completion_tokens=10))).encode()
 monkeypatch.setattr(mod.urllib.request,'urlopen',lambda *a,**k:Response())
 client=mod.ParallelStudyClient(tmp_path)
 with concurrent.futures.ThreadPoolExecutor(2) as p:results=list(p.map(lambda i:client.call([dict(role='user',content='hello')],seed=i,label='unit_'+str(i)),range(2)))
 events=[json.loads(l) for l in (tmp_path/'ledger.jsonl').read_text().splitlines()]
 assert len(results)==2 and sum(e['event']=='reserve' for e in events)==2 and sum(e['event']=='settle' for e in events)==2
 assert client.spent_usd==pytest.approx(.0000075)

def test_token_reservation_released_to_actual_usage(tmp_path):
 client=mod.ParallelStudyClient(tmp_path,tpm=1000)
 events=[]
 for i in range(2):events.append(dict(event='reserve',id=str(i),charge_usd='.001',requested_at=10+i,rate_token_bound=600,input_token_bound=600,max_tokens=0))
 assert client.limits(events,500,20)[1]>20
 for i in range(2):events.append(dict(event='settle',id=str(i),charge_usd='.0001',usage=dict(prompt_tokens=100,completion_tokens=20)))
 assert client.limits(events,500,20)[1]==20

def test_budget_cap_checked_before_network(tmp_path,monkeypatch):
 monkeypatch.setattr(mod.base,'_key',lambda:'unit-test-key')
 (tmp_path/'ledger.jsonl').write_text(json.dumps(dict(event='reserve',id='opening',charge_usd='2.99999',requested_at=0,input_token_bound=0,max_tokens=0))+'\n')
 monkeypatch.setattr(mod.urllib.request,'urlopen',lambda *a,**k:pytest.fail('budget must block HTTP'))
 with pytest.raises(mod.base.BudgetExceeded):mod.ParallelStudyClient(tmp_path).call([dict(role='user',content='hello')],seed=1,label='unit')
