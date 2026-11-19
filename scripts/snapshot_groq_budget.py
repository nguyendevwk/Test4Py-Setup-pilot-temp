"""Read-only ledger reconciliation; immutable output budget snapshot."""
import argparse,json
from pathlib import Path
from decimal import Decimal
R=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--prefix',default='context_development__');a=p.parse_args();api=R/'research/groq_study_20261118/api';events=[json.loads(l) for l in (api/'ledger.jsonl').read_text().splitlines()];balances={};settled={};labels={}
 for e in events:
  balances[e['id']]=Decimal(e['charge_usd'])
  if e['event']=='reserve':labels[e['id']]=e.get('label','')
  if e['event']=='settle':settled[e['id']]=Decimal(e['charge_usd'])
 usage={'prompt_tokens':0,'completion_tokens':0};statuses={};cohort=sum((v for k,v in settled.items() if labels[k].startswith(a.prefix)),Decimal(0))
 for rid in settled:
  d=json.loads((api/(rid+'.response.json')).read_text())
  for name in usage:usage[name]+=d.get('usage',{}).get(name,0)
  meta=json.loads((api/(rid+'.response.meta.json')).read_text());status=str(meta.get('status',meta.get('http_status','unspecified')));statuses[status]=statuses.get(status,0)+1
 data=dict(cumulative_cap_usd=3,accounted_total_usd=str(sum(balances.values(),Decimal(0))),settled_api_estimate_usd=str(sum(settled.values(),Decimal(0))),settled_responses=len(settled),**usage,cohort_label_prefix=a.prefix,cohort_responses=sum(v.startswith(a.prefix) for v in labels.values()),cohort_estimate_usd=str(cohort),settled_http_status_counts=statuses,pricing='Configured .075 input/.30 output per million, estimates not invoices',note='Accounted includes outstanding reserves and user opening allocation; do not add usage estimates as distinct bills')
 assert Decimal(data['accounted_total_usd'])<=3
 with a.output.open('x') as f:json.dump(data,f,indent=2)
 print(json.dumps(data,indent=2))
if __name__=='__main__':main()
