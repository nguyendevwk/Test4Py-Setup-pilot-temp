#!/usr/bin/env python3
"""Multi-project locked component evaluation, cumulative provider budget 3 USD."""
import ast
import json
from pathlib import Path
import sys
import time

from run_groq_study import ROOT,execute,quality,write,sha
from pilot.multitarget import clean_code_block
from study_groq_client import StudyClient,RateLimited,BudgetExceeded

WORK=ROOT/'research/groq_confirmation_20261118'


def witness(target,folder):
    path=Path(target['source_file_absolute'])
    node=next(n for n in ast.parse(path.read_text()).body if getattr(n,'name',None)==target['symbol'])
    functions=[node] if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) else [n for n in node.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
    bodylines={n.lineno for fn in functions for stmt in fn.body for n in ast.walk(stmt)
               if isinstance(n,ast.stmt) and not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
    cov=json.loads((folder/'coverage.json').read_text())
    executed=set()
    for name,entry in cov.get('files',{}).items():
        resolved=Path(name) if Path(name).is_absolute() else Path(target['root'])/name
        if resolved.resolve()==path.resolve():executed.update(entry.get('executed_lines',[]))
    return dict(body_line_candidates=len(bodylines),executed_body_lines=sorted(bodylines&executed),
                reached=bool(bodylines&executed),scope='coverage witness, not oracle correctness')


def summarize(manifest):
    rows=[json.loads(p.read_text()) for p in sorted((WORK/'attempts').glob('*/outcome.json'))]
    perarm={}
    for arm in manifest['arms']:
        r=[x for x in rows if x['arm']==arm];n=manifest['planned']//2
        perarm[arm]=dict(planned=n,completed=len(r),passed=sum(x['accepted'] for x in r),
            pass_rate_pct=100*sum(x['accepted'] for x in r)/n,
            penalized_module_line_pct=sum((x.get('line_pct') or 0) if x['accepted'] else 0 for x in r)/n,
            positive_target_witness=sum(x.get('target_witness',{}).get('reached',False) for x in r),
            seconds=sum(x.get('seconds',0) for x in r))
    data=dict(scope=manifest['status'],planned=manifest['planned'],completed=len(rows),
        arms=perarm,rows=rows,target_count=len(manifest['targets']),
        project_count=len({t['project'] for t in manifest['targets']}),
        expected_target_slots=manifest['expected_target_slots'],missing_target_slots=manifest['missing_target_slots'])
    write(WORK/'summary.json',data)
    return data


def main():
    manifest=json.loads((WORK/'manifest.json').read_text())
    lockpath=WORK/'execution_manifest.json'
    current=dict(source_manifest_sha256=sha((WORK/'manifest.json').read_bytes()),
        runner_sha256=sha(Path(__file__).read_bytes()),
        client_sha256=sha((ROOT/'scripts/study_groq_client.py').read_bytes()),
        budget_cumulative_usd=3,locked_at=time.time(),
        primary='Exactly 3 independent test functions; static quality + all-pass + target-body coverage witness + replay; no repair',
        intended_projects=10,eligible_projects=9,missing_project='black: upstream-listed Python modules unavailable in current distribution; exclusion before model inference',
        source_scope='Resolved PyPI releases; Test4Py module frame adaptation, not original pinned paper experiment')
    if not lockpath.exists():write(lockpath,current)
    else:
        saved=json.loads(lockpath.read_text())
        for key in ['source_manifest_sha256','runner_sha256','client_sha256']:
            if saved[key]!=current[key]:raise RuntimeError('Locked '+key+' changed')
    client=StudyClient(ROOT/'research/groq_study_20261118/api',budget_usd=3,max_tokens=2048)
    for ti,t in enumerate(manifest['targets']):
        if sha(Path(t['source_file_absolute']).read_bytes())!=t['source_sha256']:raise RuntimeError('Target source changed')
        for seed in manifest['seed_values']:
            for arm in (manifest['arms'] if (ti+seed)%2 else manifest['arms'][::-1]):
                label=t['id']+'__'+str(seed)+'__'+arm;dest=WORK/'attempts'/label
                if (dest/'outcome.json').exists():continue
                if dest.exists():raise RuntimeError('Incomplete attempt preserved: '+label)
                dest.mkdir(parents=True)
                start=time.monotonic();row=dict(target_id=t['id'],project=t['project'],module=t['module'],
                    seed=seed,arm=arm,accepted=False,line_pct=None,status='started')
                write(dest/'started.json',row)
                fatal=False
                try:
                    context='Module '+t['module']+' target '+t['symbol']+'\n'+t['source']
                    if arm=='atomic_verified_setup' and t['setup_probe']['accepted']:
                        context+='\nRuntime signature and successfully executed setup arguments (NOT expected results):\n'+t['setup_probe']['stdout']
                    raw=client.call([{'role':'system','content':manifest['rules']},{'role':'user','content':context}],
                                    seed=seed,label='confirmation__'+label)
                    code=clean_code_block(raw['content'] or '');(dest/'v0.py').write_text(code)
                    tests=[n for n in ast.walk(ast.parse(code)) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
                    if len(tests)!=3 or not quality(code):row['status']='quality_gate_failed'
                    else:
                        e=execute(code,Path(t['root']),t['module'],dest/'eval0')
                        row['status']='test_failure'
                        if e['suite_pass'] and (e['line_pct'] or 0)>0:
                            w=witness(t,dest/'eval0');row['target_witness']=w
                            if w['reached']:
                                replay=execute(code,Path(t['root']),t['module'],dest/'replay')
                                wr=witness(t,dest/'replay') if replay['suite_pass'] else {'reached':False}
                                row.update(accepted=replay['suite_pass'] and wr['reached'] and e['line_pct']==replay['line_pct'],
                                    status='completed',line_pct=e['line_pct'],branch_pct=e['branch_pct'],
                                    final_code=str(dest/'v0.py'))
                            else:row['status']='target_not_reached'
                except RateLimited as exc:
                    row.update(status='rate_limited',retry_after=exc.retry_after);fatal=True
                except BudgetExceeded:
                    row['status']='budget_exhausted';fatal=True
                except RuntimeError:
                    row['status']='provider_error';fatal=True
                except Exception as exc:row['status']='error:'+type(exc).__name__
                row['seconds']=time.monotonic()-start;write(dest/'outcome.json',row)
                summarize(manifest)
                print(json.dumps({k:row[k] for k in ['target_id','arm','seed','accepted','status']}),flush=True)
                if fatal:raise RuntimeError('Provider/budget pause; all prior evidence retained')
    print(json.dumps(summarize(manifest)['arms']))


if __name__=='__main__':main()
