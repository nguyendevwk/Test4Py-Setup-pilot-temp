#!/usr/bin/env python3
"""Locked paired exploratory study; preserve every planned attempt and response."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pilot.grounding import dependency_context
from pilot.multitarget import clean_code_block
from council.runner import repair_audit

WORK = ROOT / 'research/groq_study_20261118'
API_WORK = WORK/'api'
SOURCES = Path('/tmp/council-study-sources')
SPECS = [
    ('sty', 'sty.primitive', 'Style'),
    ('sty', 'sty.primitive', 'Register'),
    ('sty', 'sty.lib', 'mute'),
    ('pyMonet', 'pymonet.box', 'Box'),
    ('pyMonet', 'pymonet.maybe', 'Maybe'),
    ('pyMonet', 'pymonet.validation', 'Validation'),
    ('pytutils', 'pytutils.props', 'lazyclassproperty'),
    ('pytutils', 'pytutils.props', 'lazyperclassproperty'),
    ('pytutils', 'pytutils.excs', 'ok'),
]
RULES = '''Write a complete pytest module testing the real imported target.
Use production source as evidence. Test normal, boundary and error behavior.
Use precise assertions, pytest.raises or unittest assertions; no tautologies,
skips, xfail, suppression of unexpected exceptions or mocks of the target.
Do not modify product code, install packages, access network or real user files.
Temporary files must use tmp_path. Keep suites independent and deterministic.
Return exactly one complete Python code block. Do not output explanations.'''


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def safe_env(root, work):
    # Deliberately do not inherit API keys or the user's HOME into generated tests.
    return {'PATH': os.environ.get('PATH', '/usr/bin:/bin'),
            'HOME': str(work), 'LANG': 'C.UTF-8',
            'PYTHONPATH': str(root), 'PYTHONDONTWRITEBYTECODE': '1',
            'PYTEST_DISABLE_PLUGIN_AUTOLOAD': '1', 'COVERAGE_FILE': str(work / '.coverage')}


def execute(code, root, module, dest, timeout=20):
    dest.mkdir(parents=True, exist_ok=False)
    (dest / 'test_generated.py').write_text(code)
    cmd = [sys.executable, '-m', 'coverage', 'run', '--branch', '--source='+module,
           '-m', 'pytest', '-q', '-o', 'addopts=', '--confcutdir='+str(dest),
           '-p', 'pytest_jsonreport.plugin', '--json-report',
           '--json-report-file='+str(dest/'pytest.json'), str(dest/'test_generated.py')]
    env = safe_env(root, dest)
    started = time.monotonic()
    try:
        proc = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True, timeout=timeout)
        rc, out, err, timed = proc.returncode, proc.stdout, proc.stderr, False
    except subprocess.TimeoutExpired as exc:
        rc, out, err, timed = None, str(exc.stdout or ''), str(exc.stderr or ''), True
    (dest/'stdout.txt').write_text(out); (dest/'stderr.txt').write_text(err)
    report = json.loads((dest/'pytest.json').read_text()) if (dest/'pytest.json').exists() else {}
    tests = report.get('tests', [])
    passed = bool(rc == 0 and tests and all(t.get('outcome') == 'passed' for t in tests))
    result = dict(returncode=rc, timeout=timed, suite_pass=passed,
                  nodes=len(tests), passed_nodes=sum(t.get('outcome')=='passed' for t in tests),
                  seconds=time.monotonic()-started, line_pct=None, branch_pct=None)
    if passed:
        covproc = subprocess.run([sys.executable, '-m', 'coverage', 'json', '-o', str(dest/'coverage.json')],
                                 cwd=root, env=env, capture_output=True, text=True, timeout=timeout)
        if covproc.returncode == 0:
            cov = json.loads((dest/'coverage.json').read_text())['totals']
            result['coverage_counts'] = cov
            if cov['num_statements']:
                result['line_pct'] = 100*cov['covered_lines']/cov['num_statements']
            if cov['num_branches']:
                result['branch_pct'] = 100*cov['covered_branches']/cov['num_branches']
    write(dest/'evaluation.json', result)
    return result


def quality(code):
    tree = ast.parse(code)
    checks = 0
    for n in ast.walk(tree):
        if isinstance(n, ast.Assert):
            checks += 1
            if isinstance(n.test, ast.Constant):
                return False
            if isinstance(n.test, ast.Compare):
                if all(isinstance(x, ast.Constant) for x in [n.test.left, *n.test.comparators]):
                    return False
                if any(ast.dump(n.test.left)==ast.dump(c) for c in n.test.comparators):
                    return False
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr in {'skip', 'skipif', 'xfail'}:
                return False
            if n.func.attr.startswith('assert') or n.func.attr in {'raises','warns'}:
                checks += 1
    return checks > 0


def prepare():
    if (WORK/'manifest.json').exists():
        raise RuntimeError('Manifest already exists; use run to resume exact plan')
    targets = []
    for project, module, symbol in SPECS:
        root = SOURCES/project
        rel = module.replace('.', '/')+'.py'
        source = (root/rel).read_text()
        node = next(n for n in ast.parse(source).body if getattr(n, 'name', None)==symbol)
        imports = '\n'.join(ast.get_source_segment(source,n) for n in ast.parse(source).body
                            if isinstance(n,(ast.Import,ast.ImportFrom)))
        excerpt = ast.get_source_segment(source,node)
        deps = dependency_context(root, rel, symbol, max_chars=14000, max_nodes=12)
        preflight = subprocess.run([sys.executable, '-c', 'import importlib; m=importlib.import_module('+repr(module)+'); getattr(m,'+repr(symbol)+')'],
                                  cwd=root, env=safe_env(root, WORK), capture_output=True, text=True, timeout=15)
        target = dict(id=project+'__'+module+'__'+symbol, project=project, module=module,
                      symbol=symbol, file=rel, source_sha256=sha(source.encode()),
                      source=imports+'\n\n'+excerpt, dependencies=deps,
                      root=str(root), preflight_pass=preflight.returncode==0,
                      preflight_stderr=preflight.stderr,
                      commit=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip())
        targets.append(target)
    WORK.mkdir(parents=True, exist_ok=True)
    manifest = dict(status='locked_exploratory_new_projects_not_paper_replication',
                    model='openai/gpt-oss-20b', seed_values=[42,43,44],
                    seed_caveat='API seed best effort, not guaranteed determinism',
                    arms=['source_only','ast_dependencies'], repair_rounds=2,
                    max_completion_tokens=2048, temperature=.2,
                    budget_usd=2, targets=targets, planned=len(targets)*3*2,
                    selection='Three projects chosen for pure-Python feasibility; nine symbols chosen before inference. Not random or representative.',
                    primary='suite pass + positive module coverage + replay + static assertion gate',
                    pricing={'input_per_million':.075,'output_per_million':.30,
                             'source':'https://console.groq.com/docs/model/openai/gpt-oss-20b'},
                    rules=RULES, runner_sha256=sha(Path(__file__).read_bytes()),
                    preparation_timestamp=time.time())
    write(WORK/'manifest.json',manifest)
    print(json.dumps({'planned':manifest['planned'],'preflight_pass':sum(t['preflight_pass'] for t in targets),'targets':len(targets)}))


def summarize(manifest):
    rows=[]
    for p in sorted((WORK/'attempts').glob('*/outcome.json')):
        rows.append(json.loads(p.read_text()))
    summary=dict(planned=manifest['planned'], completed=len(rows), arms={}, rows=rows,
                 scope=manifest['status'], module_count=len({t['module'] for t in manifest['targets']}),
                 target_count=len(manifest['targets']), project_count=len({t['project'] for t in manifest['targets']}))
    for arm in manifest['arms']:
        r=[x for x in rows if x['arm']==arm]
        planned=manifest['planned']//2
        summary['arms'][arm]=dict(planned=planned,completed=len(r),passed=sum(x['accepted'] for x in r),
            first_pass=sum(x.get('first_pass',False) for x in r),
            end_to_end_line_pct=sum((x.get('line_pct') or 0) if x['accepted'] else 0 for x in r)/planned,
            seconds=sum(x['seconds'] for x in r),
            missing=planned-len(r))
    write(WORK/'summary.json',summary)
    return summary


def run():
    from study_groq_client import StudyClient
    manifest=json.loads((WORK/'manifest.json').read_text())
    if sha(Path(__file__).read_bytes())!=manifest['runner_sha256']:
        raise RuntimeError('Runner changed after locking')
    for t in manifest['targets']:
        if sha((Path(t['root'])/t['file']).read_bytes())!=t['source_sha256']:
            raise RuntimeError('Source changed after locking')
    client=StudyClient(API_WORK,budget_usd=2,input_price=.075,output_price=.30,max_tokens=2048)
    for ti,target in enumerate(manifest['targets']):
        for seed in manifest['seed_values']:
            arms=manifest['arms'] if (ti+seed)%2 else list(reversed(manifest['arms']))
            for arm in arms:
                label=target['id']+'__'+str(seed)+'__'+arm
                dest=WORK/'attempts'/label
                if (dest/'outcome.json').exists():
                    continue
                # An interrupted directory is retained; resuming does not overwrite evidence.
                if dest.exists():
                    raise RuntimeError('Incomplete attempt requires explicit audit: '+label)
                dest.mkdir(parents=True)
                start=time.monotonic()
                row=dict(target_id=target['id'], project=target['project'], module=target['module'],
                         seed=seed,arm=arm,accepted=False,first_pass=False,line_pct=None,
                         status='started',seconds=0)
                write(dest/'started.json',row)
                try:
                    if not target['preflight_pass']:
                        raise RuntimeError('preflight_failed')
                    context='Module: '+target['module']+'\nTarget: '+target['symbol']+'\nProduction source:\n'+target['source']
                    if arm=='ast_dependencies':
                        context+='\nBounded AST retrieved production dependencies (not curated hints):\n'+json.dumps(target['dependencies'])
                    messages=[{'role':'system','content':RULES},{'role':'user','content':context}]
                    raw=client.call(messages,seed=seed,label=label+'__generate')
                    content=raw['choices'][0]['message'].get('content') or ''
                    code=clean_code_block(content)
                    (dest/'v0.py').write_text(code)
                    result=None
                    for round_index in range(3):
                        if not quality(code):
                            row['status']='quality_gate_failed';break
                        result=execute(code,Path(target['root']),target['module'],dest/f'eval{round_index}')
                        if result['suite_pass'] and (result['line_pct'] or 0)>0:
                            replay=execute(code,Path(target['root']),target['module'],dest/'replay')
                            row.update(accepted=replay['suite_pass'] and replay['line_pct']==result['line_pct'],
                                       first_pass=round_index==0,line_pct=result['line_pct'],
                                       branch_pct=result['branch_pct'],repair_rounds=round_index,
                                       status='completed',final_code=str(dest/f'v{round_index}.py'))
                            break
                        if round_index==2:
                            row['status']='test_failure';break
                        diagnostic=(dest/f'eval{round_index}'/'stdout.txt').read_text()[-6000:]
                        repair_messages=[{'role':'system','content':RULES+'\nRepair imports/setup only. Preserve every existing assertion expression and test scenario exactly.'},
                            {'role':'user','content':context+'\nCurrent suite:\n'+code+'\nDiagnostics:\n'+diagnostic}]
                        raw=client.call(repair_messages,seed=seed,label=label+'__repair'+str(round_index+1))
                        new=clean_code_block(raw['choices'][0]['message'].get('content') or '')
                        (dest/f'v{round_index+1}.py').write_text(new)
                        audit=repair_audit(code,new)
                        write(dest/f'audit{round_index+1}.json',audit)
                        if not audit['accepted'] or audit['review_required']:
                            row['status']='repair_requires_semantic_review';break
                        code=new
                except Exception as exc:
                    # No raw exception text: transports can contain credential-bearing URLs.
                    row['status']='error:'+type(exc).__name__
                row['seconds']=time.monotonic()-start
                write(dest/'outcome.json',row)
                summarize(manifest)
                print(json.dumps({k:row[k] for k in ['target_id','arm','seed','accepted','status'] }),flush=True)
                if row['status']=='error:RuntimeError':
                    raise RuntimeError('Transport/provider error: queue paused; preserve failed attempt')
    print(json.dumps(summarize(manifest)['arms']),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','run','summarize'])
    parser.add_argument('--work',type=Path,default=WORK)
    args=parser.parse_args()
    WORK=args.work.resolve()
    if args.action=='prepare':prepare()
    elif args.action=='run':run()
    else:print(json.dumps(summarize(json.loads((WORK/'manifest.json').read_text()))['arms']))
