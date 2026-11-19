"""Audit extraction failures without altering original outcomes; final statistics."""
import hashlib,json,shutil,sys
from pathlib import Path
from decimal import Decimal
import analyze_groq_codamosa_extension as planned
from analyze_groq_confirmation_statistics import analyze_group
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pilot.multitarget import clean_code_block
R=Path(__file__).resolve().parents[1];W=R/'research/groq_codamosa_extension_20261119'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=json.loads((W/'manifest.json').read_text());s=json.loads((W/'summary.json').read_text());assert s['completed']==m['planned']
 api=R/'research/groq_study_20261118/api';events=[json.loads(l) for l in (api/'ledger.jsonl').read_text().splitlines()];labels={e['label']:e['id'] for e in events if e['event']=='reserve'};corrections=[]
 for row in s['rows']:
  if row['status']=='error:ValueError':
   assert not row['accepted'];label='codamosa_extension__'+row['target_id']+'__'+str(row['seed'])+'__'+row['arm'];response=api/(labels[label]+'.response.json');raw=json.loads(response.read_text());content=raw['choices'][0]['message'].get('content') or ''
   try:clean_code_block(content)
   except ValueError as exc:reason=str(exc)
   else:raise RuntimeError('Not an extraction failure; manual infrastructure investigation required')
   corrections.append(dict(target_id=row['target_id'],seed=row['seed'],arm=row['arm'],raw_status=row['status'],analysis_status='quality_gate_failed',reproduced_extraction_error=reason,response_sha256=sha(response),accepted_before=False,accepted_after=False,acceptance_changed=False))
   row['status']='quality_gate_failed'
 derived=W/'analysis_inputs';derived.mkdir(exist_ok=False)
 for name in ['manifest.json','PROVENANCE.json']:shutil.copy2(W/name,derived/name)
 (derived/'summary.json').write_text(json.dumps(s,indent=2))
 (W/'ANALYSIS_STATUS_CLASSIFICATION.json').write_text(json.dumps(dict(scope='Derived terminal failure classification only, original outcome and summary bytes retained; no rows removed or acceptance/coverage changed',corrections=corrections,original_summary_sha256=sha(W/'summary.json'),derived_summary_sha256=sha(derived/'summary.json')),indent=2))
 planned.W=derived;planned.main()
 for name in ['statistics.json','STATISTICS.md']:shutil.copy2(derived/name,W/name)
 disclosure=json.loads((W/'HISTORICAL_OVERLAP_DISCLOSURE.json').read_text());ids={t['id'] for t in m['targets'] if t['project'] not in disclosure['legacy_overlap_projects']};targets=[t for t in m['targets'] if t['id'] in ids];rows=[r for r in s['rows'] if r['target_id'] in ids];post=analyze_group(dict(m,targets=targets,planned=len(rows)),dict(s,rows=rows,completed=len(rows),planned=len(rows)))
 post['scope']='Post-hoc scope sensitivity excluding four historically used projects, not a prospectively specified primary. All204 original outcomes remain in primary analysis.'
 (W/'history_scope_sensitivity.json').write_text(json.dumps(post,indent=2))
 balances={};settled={};usage={'prompt_tokens':0,'completion_tokens':0};extensions=set();extensiontotal=Decimal(0)
 for e in events:
  balances[e['id']]=Decimal(e['charge_usd'])
  if e['event']=='reserve' and e.get('label','').startswith('codamosa_extension__'):extensions.add(e['id'])
  if e['event']=='settle':settled[e['id']]=Decimal(e['charge_usd'])
 for rid in settled:
  data=json.loads((api/(rid+'.response.json')).read_text());u=data.get('usage',{})
  for name in usage:usage[name]+=u.get(name,0)
  if rid in extensions:extensiontotal+=settled[rid]
 budget=dict(cumulative_cap_usd=3,accounted_total_usd=str(sum(balances.values(),Decimal(0))),settled_api_estimate_usd=str(sum(settled.values(),Decimal(0))),settled_responses=len(settled),**usage,extension_responses=len(extensions),extension_estimate_usd=str(extensiontotal),pricing='Configured .075 input/.30 output per million; estimated, not invoice',note='Accounted includes uncertain reservations and user opening allocation; do not add as separate bills')
 assert Decimal(budget['accounted_total_usd'])<=3
 (W/'budget.json').write_text(json.dumps(budget,indent=2));print(json.dumps(budget,indent=2))
if __name__=='__main__':main()
