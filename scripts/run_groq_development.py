#!/usr/bin/env python3
"""Post-pilot DEVELOPMENT only: matched atomic prompting with runtime setup hints."""
import ast
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

from run_groq_study import ROOT, RULES, execute, safe_env, sha, write, quality
from study_groq_client import StudyClient

WORK=ROOT/'research/groq_development_20261118'
PILOT=ROOT/'research/groq_study_20261118_v2/manifest.json'
ATOMIC=RULES+'\nWrite exactly THREE independent test functions. Each tests one scenario with concrete observable assertions. Prefer small representative tests over sprawling suites. Do not use private APIs unless the target itself is private.'


def setup_hint(target):
    script='''import importlib,inspect,json
obj=getattr(importlib.import_module(MODULE), SYMBOL)
sig=inspect.signature(obj)
kwargs={}
for name,p in sig.parameters.items():
 if p.default is not inspect.Parameter.empty or p.kind in (p.VAR_POSITIONAL,p.VAR_KEYWORD):continue
 if p.kind==p.POSITIONAL_ONLY:raise ValueError('positional-only unsupported')
 if name in ('f','fn','func','function','callback','mapper'):value=lambda *args:1
 elif name.startswith('is_') or p.annotation is bool:value=False
 elif name in ('errors','items','values','rules'):value=[]
 else:value=1
 kwargs[name]=value
result=obj(**kwargs)
print(json.dumps({'signature':str(sig),'arguments':{k:('lambda *args: 1' if callable(v) else repr(v)) for k,v in kwargs.items()},'scope':'constructor/call completed; no oracle or method-state guarantee'}))
'''.replace('MODULE',repr(target['module'])).replace('SYMBOL',repr(target['symbol']))
    proc=subprocess.run([sys.executable,'-c',script],cwd=target['root'],
        env=safe_env(Path(target['root']),WORK),capture_output=True,text=True,timeout=15)
    return dict(accepted=proc.returncode==0,stdout=proc.stdout,stderr=proc.stderr,returncode=proc.returncode)


def prepare():
    manifest=json.loads(PILOT.read_text())
    manifest.update(status='post_pilot_development_not_heldout',seed_values=[45,46],
                    arms=['atomic_source','atomic_verified_setup'],repair_rounds=0,
                    planned=36,rules=ATOMIC,runner_sha256=sha(Path(__file__).read_bytes()),
                    note='Same nine subjects observed in earlier pilot; cannot use this as independent confirmation.')
    for target in manifest['targets']:
        target['setup_probe']=setup_hint(target)
    WORK.mkdir(parents=True,exist_ok=True)
    with (WORK/'manifest.json').open('x') as f:json.dump(manifest,f,indent=2)
    print('Development plan locked:',manifest['planned'],'probe successes:',sum(t['setup_probe']['accepted'] for t in manifest['targets']))


def summary(manifest):
    rows=[json.loads(p.read_text()) for p in sorted((WORK/'attempts').glob('*/outcome.json'))]
    arms={}
    for arm in manifest['arms']:
        r=[x for x in rows if x['arm']==arm]
        arms[arm]=dict(planned=18,completed=len(r),passed=sum(x['accepted'] for x in r),
            penalized_module_line_pct=sum((x.get('line_pct') or 0) if x['accepted'] else 0 for x in r)/18)
    write(WORK/'summary.json',dict(scope=manifest['status'],planned=36,completed=len(rows),arms=arms,rows=rows))
    return arms


def run():
    m=json.loads((WORK/'manifest.json').read_text())
    if m['runner_sha256']!=sha(Path(__file__).read_bytes()):raise RuntimeError('locked runner changed')
    c=StudyClient(ROOT/'research/groq_study_20261118/api',max_tokens=2048)
    for ti,t in enumerate(m['targets']):
        if sha((Path(t['root'])/t['file']).read_bytes())!=t['source_sha256']:raise RuntimeError('source changed')
        for seed in m['seed_values']:
            for arm in (m['arms'] if (ti+seed)%2 else m['arms'][::-1]):
                label=t['id']+'__'+str(seed)+'__'+arm;d=WORK/'attempts'/label
                if (d/'outcome.json').exists():continue
                d.mkdir(parents=True,exist_ok=False);started=time.monotonic()
                r=dict(target_id=t['id'],project=t['project'],module=t['module'],arm=arm,seed=seed,
                       accepted=False,line_pct=None,status='started')
                write(d/'started.json',r)
                try:
                    context='Module '+t['module']+' target '+t['symbol']+'\n'+t['source']
                    if arm=='atomic_verified_setup' and t['setup_probe']['accepted']:
                        context+='\nRuntime signature and successfully executed setup arguments (NOT expected results):\n'+t['setup_probe']['stdout']
                    raw=c.call([{'role':'system','content':ATOMIC},{'role':'user','content':context}],seed=seed,label=label)
                    from pilot.multitarget import clean_code_block
                    code=clean_code_block(raw['content'] or '');(d/'v0.py').write_text(code)
                    tests=[n for n in ast.walk(ast.parse(code)) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
                    if len(tests)!=3 or not quality(code):r['status']='quality_gate_failed'
                    else:
                        e=execute(code,Path(t['root']),t['module'],d/'eval0')
                        r['status']='test_failure'
                        if e['suite_pass'] and (e['line_pct'] or 0)>0:
                            replay=execute(code,Path(t['root']),t['module'],d/'replay')
                            r.update(accepted=replay['suite_pass'] and e['line_pct']==replay['line_pct'],
                                status='completed',line_pct=e['line_pct'],branch_pct=e['branch_pct'])
                except Exception as exc:r['status']='error:'+type(exc).__name__
                r['seconds']=time.monotonic()-started;write(d/'outcome.json',r);summary(m)
                print(json.dumps({k:r[k] for k in ('arm','target_id','seed','accepted','status')}),flush=True)
                if r['status'].startswith('error:RuntimeError'):raise RuntimeError('provider error; stop queue')
    print(json.dumps(summary(m)))


if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    else:run()
