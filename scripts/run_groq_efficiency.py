"""Paired output-cap engineering screen on the frozen, already-observed targets."""
import ast
import json
from pathlib import Path
import time

from run_groq_study import ROOT,execute,quality,write,sha
from run_groq_confirmation import witness
from pilot.multitarget import clean_code_block
from study_groq_client import StudyClient,RateLimited,BudgetExceeded

WORK=ROOT/'research/groq_efficiency_20261119'
SOURCE=ROOT/'research/groq_confirmation_20261118/manifest.json'


def prepare():
    if (WORK/'manifest.json').exists():return json.loads((WORK/'manifest.json').read_text())
    m=json.loads(SOURCE.read_text())
    m.update(status='output_cap_engineering_screen_on_previously_observed_targets',
        output_caps=[1536,2048],seed_values=[45],planned=len(m['targets'])*4,
        source_manifest_sha256=sha(SOURCE.read_bytes()),runner_sha256=sha(Path(__file__).read_bytes()),
        rationale='Compare cap cost/latency and operational acceptance; no pooling with prior efficacy cohorts or paper superiority claim.',
        current_authorized_cumulative_budget_usd=3)
    write(WORK/'manifest.json',m)
    return m


def summarize(m):
    rows=[json.loads(p.read_text()) for p in sorted((WORK/'attempts').glob('*/outcome.json'))]
    groups={}
    for arm in m['arms']:
        for cap in m['output_caps']:
            r=[x for x in rows if x['arm']==arm and x['output_cap']==cap];n=len(m['targets'])
            groups[arm+'__'+str(cap)]=dict(arm=arm,output_cap=cap,planned=n,completed=len(r),
                passed=sum(x['accepted'] for x in r),
                pass_rate_pct=100*sum(x['accepted'] for x in r)/n,
                module_line_penalized=sum((x.get('line_pct') or 0) if x['accepted'] else 0 for x in r)/n,
                completion_tokens=sum(x.get('usage',{}).get('completion_tokens',0) for x in r),
                prompt_tokens=sum(x.get('usage',{}).get('prompt_tokens',0) for x in r),
                output_limit_responses=sum(x.get('finish_reason')=='length' for x in r),
                total_seconds=sum(x['seconds'] for x in r),
                api_plus_pacing_seconds=sum(x.get('api_plus_pacing_seconds',0) for x in r))
    data=dict(scope=m['status'],planned=m['planned'],completed=len(rows),groups=groups,rows=rows,
        caveats=['Targets already observed: operational screen only.',
                 'API and pacing timing includes provider/network/rate-limit wait; not kernel inference latency.',
                 'Cap limit and finish reason do not by themselves establish correct/incorrect oracle.',
                 'One model repetition per target/arm/cap; target/project clustering remains.'])
    write(WORK/'summary.json',data)
    return data


def main():
    m=prepare()
    if sha(Path(__file__).read_bytes())!=m['runner_sha256']:raise RuntimeError('Locked runner changed')
    clients={cap:StudyClient(ROOT/'research/groq_study_20261118/api',budget_usd=3,max_tokens=cap) for cap in m['output_caps']}
    for i,t in enumerate(m['targets']):
        if sha(Path(t['source_file_absolute']).read_bytes())!=t['source_sha256']:raise RuntimeError('Source changed')
        cells=[(arm,cap) for arm in m['arms'] for cap in m['output_caps']]
        shift=i%len(cells);cells=cells[shift:]+cells[:shift]
        if i%2:cells=list(reversed(cells))
        for arm,cap in cells:
            label=t['id']+'__'+arm+'__cap'+str(cap);dest=WORK/'attempts'/label
            if (dest/'outcome.json').exists():continue
            dest.mkdir(parents=True,exist_ok=False);started=time.monotonic()
            row=dict(target_id=t['id'],project=t['project'],module=t['module'],seed=45,
                arm=arm,output_cap=cap,accepted=False,line_pct=None,status='started')
            write(dest/'started.json',row);fatal=False
            try:
                user='Module '+t['module']+' target '+t['symbol']+'\n'+t['source']
                if arm=='atomic_verified_setup' and t['setup_probe']['accepted']:
                    user+='\nRuntime signature and successfully executed setup arguments (NOT expected results):\n'+t['setup_probe']['stdout']
                api=time.monotonic()
                response=clients[cap].call([{'role':'system','content':m['rules']},{'role':'user','content':user}],seed=45,label='efficiency__'+label)
                row.update(api_plus_pacing_seconds=time.monotonic()-api,usage=response.get('usage',{}),finish_reason=response.get('finish_reason'))
                code=clean_code_block(response['content'] or '');(dest/'v0.py').write_text(code)
                tests=[n for n in ast.walk(ast.parse(code)) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
                if len(tests)!=3 or not quality(code):row['status']='quality_gate_failed'
                else:
                    e=execute(code,Path(t['root']),t['module'],dest/'eval0');row['status']='test_failure'
                    if e['suite_pass'] and (e['line_pct'] or 0)>0:
                        w=witness(t,dest/'eval0');row['target_witness']=w
                        if w['reached']:
                            replay=execute(code,Path(t['root']),t['module'],dest/'replay')
                            rw=witness(t,dest/'replay') if replay['suite_pass'] else {'reached':False}
                            row.update(accepted=replay['suite_pass'] and rw['reached'] and replay['line_pct']==e['line_pct'],
                                line_pct=e['line_pct'],branch_pct=e['branch_pct'],status='completed',final_code=str(dest/'v0.py'))
                        else:row['status']='target_not_reached'
            except (RateLimited,BudgetExceeded) as exc:row['status']=type(exc).__name__;fatal=True
            except RuntimeError:row['status']='provider_error';fatal=True
            except ValueError:row['status']='extraction_error'
            except Exception as exc:row['status']='error:'+type(exc).__name__
            row['seconds']=time.monotonic()-started;write(dest/'outcome.json',row);summarize(m)
            print(json.dumps({k:row[k] for k in ['target_id','arm','output_cap','accepted','status']}),flush=True)
            if fatal:raise RuntimeError('Provider/budget pause; evidence preserved')
    print(json.dumps(summarize(m)['groups']))


if __name__=='__main__':main()
