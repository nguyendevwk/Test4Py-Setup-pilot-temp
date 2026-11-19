#!/usr/bin/env python3
"""Gated upstream Test4Py + NF4 paired pilot. Never silently substitutes Council.

Actions: plan -> prepare -> stress -> small -> run. `run` requires a completed
small hardware/worker check; it does not require baseline quality to be perfect.
Each action is explicit; the notebook ends after small and exports review evidence.
"""
import argparse
import ast
import csv
import hashlib
import json
import os
from pathlib import Path
import random
import shutil
import sys
import time
import urllib.request

from pilot.common import BASE, UPSTREAM, checkout, checked, command, digest, write_json, package_versions
from pilot.benchmark import locate_module
from pilot.module_mutation import pool
from pilot.scheduling import execute_modes, gpu_slots
from pilot.console import Console
from pilot.progress import emit

MODEL = 'Qwen/Qwen2.5-Coder-14B-Instruct'
FRAME = {
    'genty': dict(repo='https://github.com/box/genty.git', sha='85f7c960a2b67cf9e58e0d9e677e4a0bc4f05081',
                  modules=['genty.genty_repeat', 'genty.genty_args']),
    'woa': dict(repo='https://github.com/docwza/woa.git', sha='474737951cb0b0952e245e666e66ea51835cfd07',
                modules=['src.whale_optimization']),
}


def build_plan(max_input_tokens=4096, max_new_tokens=512, test_output_contract=None, mechanism=None):
    if test_output_contract not in (None, 'single-test-v1'):
        raise ValueError('Unknown test output contract')
    if mechanism not in (None, 'api-contract-v1'):
        raise ValueError('Unknown mechanism')
    if mechanism and test_output_contract:
        raise ValueError('API mechanism study must not reuse the failed one-test output constraint')
    files = [BASE/'paired_study.py', BASE/'benchmark_worker.py', BASE/'gpu_context_probe.py',
             BASE/'requirements-modern.txt', BASE/'requirements-paired.txt', *sorted((BASE/'pilot').glob('*.py')),
             BASE/'council/critic.py', BASE/'council/runner.py', BASE/'council/engine.py']
    plan = dict(protocol='test4py-nf4-paired-pilot-v1', upstream=UPSTREAM, frame=FRAME,
                sampling='fixed development pilot, 3 modules/2 NA projects; not representative of 183',
                small=dict(project='genty', modules=['genty.genty_repeat','genty.genty_args'], seeds=[42], rounds=1),
                main=dict(seeds=[42,43], rounds=3), arms=['baseline','improved'],
                settings=dict(model=MODEL, quantization='nf4', attention_policy='t4-efficient-sdpa-v1', max_input_tokens=max_input_tokens,
                    max_new_tokens=max_new_tokens, max_sequence_tokens=max_input_tokens+max_new_tokens, embedding='BAAI/bge-large-en-v1.5',
                    embedding_device='cpu', cpu_threads=1, score_timeout=60,
                    prompt_policy='upstream-original', code_extraction='single-complete-block-v2',
                    paired_protocol=True, initialization_greedy=True, generation=dict(do_sample=True, temperature=0.7, top_p=0.95)),
                mutation_limit=4, worker_timeout=3600, screen_budget_seconds=3600,
                source_sha256={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
    if test_output_contract:
        plan['settings']['test_output_contract'] = test_output_contract
        plan['protocol'] += '+single-test-v1'
    if mechanism:
        plan['protocol'] += '+api-contract-v1'
        plan['arms'] = ['baseline', 'api_contract']
        plan['settings'].update(mechanism=mechanism,acceptance_policy='preserve-assertions-v1',api_contract_max_chars=2500)
    return plan


def validate_plan(root, plan):
    saved=json.loads((root/'plan.json').read_text())
    if digest(saved) != digest(plan):
        raise ValueError('Plan/source changed. Preserve this run and use a NEW output path.')


def resolve_hf(model, revision='main'):
    request=urllib.request.Request('https://huggingface.co/api/models/'+model+'/revision/'+revision,
                                   headers={'User-Agent':'Test4Py-paired-pilot'})
    with urllib.request.urlopen(request,timeout=60) as response:
        sha=json.load(response)['sha']
    if len(sha)!=40:
        raise ValueError('Model revision did not resolve to an immutable SHA')
    return sha


def environment(gpu=None, extra=None):
    result=dict(os.environ, USE_TF='0',USE_FLAX='0',TOKENIZERS_PARALLELISM='false',
                PYTHONDONTWRITEBYTECODE='1',PYTHONUNBUFFERED='1',OMP_NUM_THREADS='1',
                OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
    if gpu is not None:
        result['CUDA_VISIBLE_DEVICES']=str(gpu)
    if extra:
        result.update(extra)
    return result


def project_install_command(python, product):
    """Constrain project dependencies; requirements files are never bare operands."""
    prefix = [python, '-m', 'pip', 'install', '-c', BASE/'requirements-modern.txt']
    if any((product/name).exists() for name in ('setup.py', 'pyproject.toml', 'setup.cfg')):
        return [*prefix, '-e', product]
    if (product/'requirements.txt').exists():
        return [*prefix, '-r', product/'requirements.txt']
    return None


def prepare(root, plan):
    if (root/'preflight.json').exists():
        raise ValueError('Preparation already attempted; preserve logs and use a fresh output for changes')
    upstream=root/'upstream'
    if not upstream.exists():
        checkout('https://github.com/Test4DT/Test4Py.git',UPSTREAM,upstream)
    if checked(['git','-C',upstream,'rev-parse','HEAD']) != UPSTREAM:
        raise ValueError('Upstream revision changed')
    resolved=root/'resolved_models.json'
    if not resolved.exists():
        write_json(resolved,dict(model=resolve_hf(plan['settings']['model']),
                    embedding=resolve_hf(plan['settings']['embedding'])))
    state={}
    for name,spec in plan['frame'].items():
        work=root/'prepared'/name;work.mkdir(parents=True,exist_ok=True)
        product=work/'source'
        print('Preparing '+name+' at '+spec['sha'],flush=True)
        item=dict(status='preparing',modules=spec['modules'],commit=spec['sha'])
        try:
            if not product.exists():
                checkout(spec['repo'],spec['sha'],product)
            if checked(['git','-C',product,'rev-parse','HEAD'])!=spec['sha']:
                raise ValueError('Wrong target commit')
            python=work/'venv/bin/python'
            if not python.exists():
                proc=command([sys.executable,BASE/'bootstrap_modern.py','--venv',work/'venv'],
                             cwd=BASE,timeout=1800,log_path=work/'bootstrap.log',stream=True,label=name,console=Console('compact'))
                if proc['returncode'] or proc['timeout']:
                    raise RuntimeError('Bootstrap failed; inspect bootstrap.log')
            deps=command([python,'-m','pip','install','-r',BASE/'requirements-paired.txt'],
                         cwd=BASE,timeout=900,log_path=work/'paired-dependencies.log')
            if deps['returncode'] or deps['timeout']:
                raise RuntimeError('Paired NF4 dependencies failed; inspect '+str(work/'paired-dependencies.log'))
            # An existing venv is not proof that dependency installation succeeded.
            install=project_install_command(python,product)
            if install:
                proc=command(install,cwd=product,timeout=900,log_path=work/'dependencies.log')
                write_json(work/'dependency-install.json',proc)
                if proc['returncode'] or proc['timeout']:
                    raise RuntimeError('Dependencies failed; inspect '+str(work/'dependencies.log')+'; no source/constraint fallback')
            locations=[locate_module(product,m) for m in spec['modules']]
            imports={str(i) for _,i,_ in locations};packages={str(p) for _,_,p in locations}
            if len(imports)!=1 or len(packages)!=1:
                raise ValueError('Selected modules have incompatible source roots')
            import_root=Path(next(iter(imports)))
            source_path=str((product/next(iter(packages))).relative_to(import_root))
            check=command([python,'-c',
                'import importlib,json,sys; print(json.dumps({n:importlib.import_module(n).__file__ for n in sys.argv[1:]}))',
                *spec['modules']],cwd=import_root,env=environment(extra={'PYTHONPATH':str(import_root)}),timeout=60)
            write_json(work/'import_check.json',check)
            if check['returncode'] or check['timeout']:
                raise RuntimeError('Pinned module import failed')
            imported=json.loads(check['stdout'].splitlines()[-1])
            if any(not Path(p).resolve().is_relative_to(product.resolve()) for p in imported.values()):
                raise RuntimeError('Imported installed package instead of pinned checkout')
            mutation_pools={m:pool(path.read_text(),plan['mutation_limit']) for m,(path,_,_) in zip(spec['modules'],locations)}
            write_json(work/'mutant-pools.json',mutation_pools)
            checked(['git','-C',product,'diff','--exit-code','HEAD'])
            write_json(work/'source_hashes.json',{str(p.relative_to(import_root)):hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (import_root/source_path).rglob('*.py') if not any(n in p.parts for n in ('tests','test','__pycache__'))})
            freeze=command([python,'-m','pip','freeze'],timeout=60)
            (work/'requirements-resolved.txt').write_text(freeze['stdout'] or '')
            item.update(status='prepared',product=str(product),import_root=str(import_root),
                        source_path=source_path,python=str(python),
                        module_functions={m:sum(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) for n in ast.walk(ast.parse(path.read_text())))
                                          for m,(path,_,_) in zip(spec['modules'],locations)})
        except Exception as exc:
            item.update(status='failed',error=repr(exc))
            print(name+' preparation failed: '+repr(exc),flush=True)
        state[name]=item;write_json(root/'preflight.json',state)
    return all(s['status']=='prepared' for s in state.values())


def screen_remaining(root):
    clock=json.loads((root/'screen-clock.json').read_text())
    return max(0,clock['deadline_epoch']-time.time())


def stress(root, plan, jobs):
    if (root/'screen-clock.json').exists():
        raise ValueError('Screen already attempted; preserve its time budget and use a new output')
    if not (root/'preflight.json').exists():
        raise ValueError('Run prepare first')
    ready=json.loads((root/'preflight.json').read_text())
    if not all(v['status']=='prepared' for v in ready.values()):
        raise ValueError('Preflight contains failures; no inference')
    settings=dict(plan['settings'],model_revision=json.loads((root/'resolved_models.json').read_text())['model'],seed=42)
    write_json(root/'stress-settings.json',settings)
    slots=gpu_slots(jobs,'auto')
    if len(slots)!=jobs or any(s is None for s in slots):
        # Explicit device list also in serial mode, so evidence names a real slot.
        slots=gpu_slots(jobs,'0,1' if jobs==2 else '0')
    results={}
    for gpu in slots:
        folder=root/('stress-gpu-'+str(gpu))
        if folder.exists():
            raise ValueError('Stress already attempted. Keep evidence; use a new output for another configuration.')
    started=time.time()
    write_json(root/'screen-clock.json',dict(started_epoch=started,
               deadline_epoch=started+plan['screen_budget_seconds'],budget_seconds=plan['screen_budget_seconds'],
               scope='stress including model downloads/load plus small; excludes CPU bootstrap/preparation'))
    def probe(gpu, unused_slot):
        folder=root/('stress-gpu-'+str(gpu))
        proc=command([sys.executable,BASE/'gpu_context_probe.py','--settings',root/'stress-settings.json',
                      '--output',folder,'--inputs',','.join(str(n) for n in (2048,4096,6144) if n<=settings['max_input_tokens']),
                      '--output-tokens',str(settings['max_new_tokens'])],env=environment(gpu),timeout=max(1,min(1800,int(screen_remaining(root)))),log_path=root/('stress-'+str(gpu)+'.log'),stream=True,label='stress-'+str(gpu),console=Console('compact'))
        report=json.loads((folder/'probe.json').read_text()) if (folder/'probe.json').exists() else {}
        return dict(status=report.get('status','missing') if proc['returncode']==0 and not proc['timeout'] else 'failed',process=proc,
                    probe=dict(status=report.get('status','missing'),tests=report.get('tests',[]),error=report.get('error')))
    # Independent stress on both T4s concurrently; one probe process per GPU.
    for gpu,result in execute_modes(slots,slots,probe):
        results[str(gpu)]=result
        print(f"[stress GPU {gpu}] {result['status']}; log: {root/('stress-'+str(gpu)+'.log')}",flush=True)
        for test in result.get('probe',{}).get('tests',[]):
            print('[stress] '+json.dumps(test),flush=True)
        if result.get('probe',{}).get('error'):
            print('[stress ERROR] '+result['probe']['error'],flush=True)
        write_json(root/'stress.json',dict(config_hash=digest(plan['settings']),plan_hash=digest(plan),
                   model_revision=settings['model_revision'],gpus=results))
    return all(r['status']=='passed' for r in results.values())


def tasks(plan, stage):
    seeds=plan[stage]['seeds'];rounds=plan[stage]['rounds']
    projects=[plan['small']['project']] if stage=='small' else list(plan['frame'])
    rows=[]
    for project in projects:
        modules=plan['small']['modules'] if stage=='small' else plan['frame'][project]['modules']
        for seed in seeds:
            for arm in plan['arms']:
                rows.append(dict(project=project,modules=modules,seed=seed,arm=arm,rounds=rounds))
    # Same predetermined order on every execution, independent of scores.
    random.Random(42).shuffle(rows)
    return rows


def collect(root, plan, stage, queue):
    rows=[];process_ok=True
    for task in queue:
        key=f"{task['project']}-{task['seed']}-{task['arm']}"
        folder=root/stage/key
        report=json.loads((folder/'report.json').read_text()) if (folder/'report.json').exists() else {}
        process=json.loads((folder/'process.json').read_text()) if (folder/'process.json').exists() else {}
        worker_status='timeout' if process.get('timeout') else report.get('status','missing')
        done=report.get('status')=='execution_complete' and process.get('returncode')==0 and not process.get('timeout') and report.get('hardware_budget_ok',True) and not report.get('unexpected_generation_errors',0)
        process_ok=process_ok and done
        for module in task['modules']:
            row=next((dict(r) for r in report.get('modules',[]) if r['module']==module),
                     dict(module=module,status='timeout_unmeasured' if process.get('timeout') else 'worker_incomplete',passed=None,line_pct=None,branch_pct=None,mutation_score=None))
            row.update(arm=task['arm'],seed=task['seed'],project=task['project'],
                       worker_status=worker_status,worker_seconds=report.get('seconds') if report.get('seconds') is not None else process.get('seconds'),
                       input_tokens=report.get('input_tokens'),output_tokens=report.get('output_tokens'),
                       generation_input_tokens=report.get('generation_input_tokens'),
                       generation_output_tokens=report.get('generation_output_tokens'),
                       initialization_cache_hits=report.get('initialization_cache_hits'),
                       gpu_peak_allocated_gib=report.get('gpu_peak_allocated_gib'),
                       process_peak_rss_gib=report.get('process_peak_rss_gib'),
                       execution_complete=bool(done))
            rows.append(row)
    measurement_exercised=any(r.get('status')=='scored' and r.get('line_pct') is not None for r in rows)
    write_json(root/(stage+'-summary.json'),dict(protocol=plan['protocol'],rows=rows,
               planned_module_trials=sum(len(t['modules']) for t in queue),reported_module_rows=len(rows),
               finished_module_rows=sum(r['execution_complete'] for r in rows),
               execution_ready=process_ok,semantic_review_required=True,
               measurement_path_exercised=measurement_exercised,
               larger_ready=bool(process_ok and measurement_exercised),
               scope='paired pilot, not full paper reproduction; coverage is not assertion accuracy'))
    cols=['project','module','arm','seed','worker_status','status','passed','line_pct','branch_pct','mutation_score',
          'covered_lines','total_lines','covered_branches','total_branches',
          'retained_collected_nodes','retained_passed_nodes','retained_failed_nodes','retained_error_nodes',
          'retained_skipped_nodes','retained_suite_all_pass','retained_collection_complete',
          'coverage_scope','mutants_planned','mutants_killed','mutants_survived','mutants_unresolved',
          'semantic_assertion_accuracy','execution_complete',
          'worker_seconds','input_tokens','output_tokens','generation_input_tokens','generation_output_tokens','initialization_cache_hits',
          'gpu_peak_allocated_gib','process_peak_rss_gib']
    with (root/(stage+'-modules.csv')).open('w') as stream:
        writer=csv.DictWriter(stream,fieldnames=cols,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
    measures={}
    for arm in plan['arms']:
        group=[r for r in rows if r['arm']==arm]
        def coverage_summary(prefix):
            valid=[r for r in group if r.get(prefix+'_pct') is not None]
            return dict(measured_trials=len(valid),missing_trials=len(group)-len(valid),
                        macro_mean_pct=sum(r[prefix+'_pct'] for r in valid)/len(valid) if valid else None,
                        interpretation='conditional on measured trials; not an unconditional treatment effect')
        measures[arm]=dict(planned_module_trials=len(group),execution_complete_trials=sum(r['execution_complete'] for r in group),
                retained_all_pass_trials=sum(r.get('retained_suite_all_pass') is True for r in group),
                retained_all_pass_rate=sum(r.get('retained_suite_all_pass') is True for r in group)/len(group)
                    if group and any(r.get('retained_suite_all_pass') is not None for r in group) else None,
                observed_successes_per_planned=sum(r.get('retained_suite_all_pass') is True for r in group)/len(group) if group else None,
                rate_status='complete' if group and all(r.get('retained_suite_all_pass') is not None for r in group) else 'incomplete_or_unmeasured',
                retained_suite_unmeasured_trials=sum(r.get('retained_suite_all_pass') is None for r in group),
                line=coverage_summary('line'),branch=coverage_summary('branch'),
                mutation_measured_trials=sum(r.get('mutation_score') is not None for r in group),
                hallucination_rate=None,semantic_assertion_accuracy=None,
                review_status='not measured; requires common error taxonomy and source-based assertion review')
    write_json(root/(stage+'-measurement-summary.json'),dict(arms=measures,
               scope='retained suites after upstream generation/repair/reduction, not first-attempt accuracy',
               note='Unavailable trials remain in planned denominator. Rates are observed successful trials/planned; missing coverage is never zero-imputed.'))
    # Pair only matching targets/seeds and original mutant pools. Do not compare unrelated means.
    paired=[]
    for a in rows:
        if a['arm']!='baseline':continue
        treatment='api_contract' if plan['settings'].get('mechanism') else 'improved'
        b=next((r for r in rows if r['arm']==treatment and (r['project'],r['module'],r['seed'])==(a['project'],a['module'],a['seed'])),None)
        if b is None:continue
        compatible=bool(a.get('mutant_pool_hash') and a.get('mutant_pool_hash')==b.get('mutant_pool_hash'))
        comparable=bool(a['execution_complete'] and b['execution_complete'] and a['status']=='scored' and b['status']=='scored')
        delta=lambda k: b[k]-a[k] if comparable and b.get(k) is not None and a.get(k) is not None else None
        paired.append(dict(project=a['project'],module=a['module'],seed=a['seed'],
                          line_delta_pp=delta('line_pct'),branch_delta_pp=delta('branch_pct'),
                          mutation_delta=delta('mutation_score') if compatible else None, mutant_pool_match=compatible,comparison_eligible=comparable))
    write_json(root/(stage+'-paired-differences.json'),paired)
    def fmt(v):return 'NA' if v is None else str(round(v,3)) if isinstance(v,float) else str(v)
    lines=['# Upstream Test4Py NF4 paired pilot',f'Stage: {stage}. Engineering execution complete: {process_ok}.',
           'Baseline uses actual pinned Test4Py init/type inference/RAG/generation/repair. Shared CPU embeddings and extraction adapters are recorded.',
           ('api_contract adds bounded static API/closure evidence; both arms share the assertion-preservation acceptance policy.'
            if plan['settings'].get('mechanism') else
            'Improved adds verified type/member context, source dependencies and stdlib-import repair; assertion-changing reductions receive no automatic improved credit.'),
           'All failures remain. Coverage uses replayed original-passing retained nodes, NOT an all-pass candidate suite. Retained-suite pass is reported separately.',
           'Mutation pool is small; equivalent mutants not filtered. Oracle accuracy is not measured.',
           'Project costs are shared across its modules; do not sum repeated project cost columns per module.',
           'Greedy initialization uses an exact-prompt shared cache. Fresh token costs depend on warm-cache order, not treatment. Compare generation/repair costs separately; initialization seeds are not independent replicas.',
           '', '| Project | Module | Arm | Seed | Status | Pass nodes | Line % | Branch % | Mutation |',
           '|---|---|---|---|---|---|---|---|---|']
    if plan['settings'].get('test_output_contract'):
        lines.insert(3, 'Both arms use the shared single-test-v1 generation/repair output contract. '
                        'This is an adapted upstream baseline; raw upstream prompts are not identical.')
    if plan['settings'].get('mechanism'):
        lines.insert(3, 'Mechanism ablation: shared concise-file instruction and assertion-preservation gate in both arms; '
                        'api_contract adds only static API/closure evidence. Multiple pytest tests are allowed. '
                        'The legacy improved arm is not used.')
    lines += ['| '+' | '.join(fmt(r.get(k)) for k in ['project','module','arm','seed','status','passed','line_pct','branch_pct','mutation_score'])+' |' for r in rows]
    (root/(stage+'-report.md')).write_text('\n'.join(lines)+'\n')
    return process_ok


def validate_stress(calibrated, plan, revisions, slots):
    if (calibrated.get('config_hash')!=digest(plan['settings']) or calibrated.get('plan_hash')!=digest(plan)
        or calibrated.get('model_revision')!=revisions['model']
        or any(calibrated.get('gpus',{}).get(str(g),{}).get('status')!='passed' for g in slots)):
        raise ValueError('Missing matching stress/headroom/model revision evidence for requested GPU slots')


def execute(root, plan, stage, jobs):
    preflight=json.loads((root/'preflight.json').read_text())
    if set(preflight)!=set(plan['frame']) or any(p.get('status')!='prepared' for p in preflight.values()):
        raise ValueError('Every locked project must pass preparation before inference')
    calibrated=json.loads((root/'stress.json').read_text())
    slots=gpu_slots(jobs,'0,1' if jobs==2 else '0')
    revisions=json.loads((root/'resolved_models.json').read_text())
    validate_stress(calibrated,plan,revisions,slots)
    if stage=='main':
        small=json.loads((root/'small-summary.json').read_text())
        if not small.get('larger_ready',False):
            raise ValueError('Small hardware/framework check incomplete or no real measured coverage path; do not run larger stage')
    revisions=json.loads((root/'resolved_models.json').read_text())
    queue=tasks(plan,stage)
    if (root/stage).exists():
        raise ValueError('Stage already attempted; no score-driven retries in the same output')
    (root/stage).mkdir()
    write_json(root/(stage+'-queue.json'),queue)
    emit(root,stage,'schedule',workers_finished=0,workers_total=len(queue),
         planned_module_trials=sum(len(t['modules']) for t in queue))
    # Download is bounded too: a parent-process HF request must not bypass the screen clock.
    remaining=screen_remaining(root) if stage=='small' else plan['worker_timeout']
    download=command([sys.executable,'-c',
        "import sys; from huggingface_hub import snapshot_download; print(snapshot_download(sys.argv[1],revision=sys.argv[2],ignore_patterns=['*.onnx','onnx/*','*.h5','*.msgpack']))",
        plan['settings']['embedding'],revisions['embedding']],env=environment(),
        timeout=max(1,int(remaining)),log_path=root/(stage+'-embedding-download.log')) if remaining>0 else dict(returncode=124,timeout=True)
    write_json(root/(stage+'-embedding-download.json'),download)
    if download['returncode'] or download['timeout']:
        collect(root,plan,stage,queue)
        return False
    embedding_path=download['stdout'].strip().splitlines()[-1]
    def run_one(task,gpu):
        name=task['project'];key=f"{name}-{task['seed']}-{task['arm']}"
        folder=root/stage/key;folder.mkdir()
        prepared=preflight[name]
        try:
            import_original=Path(prepared['import_root'])
            product=folder/'product'
            shutil.copytree(import_original,product,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
            # Refuse a changed prepared source, including changed production paths.
            expected=json.loads((root/'prepared'/name/'source_hashes.json').read_text())
            for path,sha in expected.items():
                if hashlib.sha256((product/path).read_bytes()).hexdigest()!=sha:
                    raise ValueError('Prepared product changed since preflight')
            config=dict(plan['settings'],**task,model_revision=revisions['model'],embedding_revision=revisions['embedding'],
                        upstream_root=str(root/'upstream'),import_root=str(product),source_path=prepared['source_path'],
                        mutation_manifest=str(root/'prepared'/name/'mutant-pools.json'),target_commit=plan['frame'][name]['sha'],
                        initialization_cache=str(root/'initialization-cache'),adapter_source_hash=digest(plan['source_sha256']))
            write_json(folder/'worker-settings.json',config)
            python=prepared['python']
            env=environment(gpu,dict(OPENAI_API_KEY='local-inference',USER_PYTHON_PATH=python,
                    PYTHONPATH=os.pathsep.join([str(root/'upstream'),str(product),str(BASE)]),
                    TRANSFORMER_PATH=embedding_path,PYTHONHASHSEED=str(task['seed']),
                    PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTEST_PLUGINS='pytest_jsonreport.plugin'))
            remaining=screen_remaining(root) if stage=='small' else plan['worker_timeout']
            if remaining<=0:
                write_json(folder/'report.json',dict(status='screen_budget_exhausted',error='No inference started after screen deadline'))
                proc=dict(returncode=124,timeout=True,seconds=0)
            else:
                proc=command([python,BASE/'benchmark_worker.py',folder/'worker-settings.json'],cwd=product,env=env,
                             timeout=max(1,min(plan['worker_timeout'],int(remaining))),log_path=folder/'worker.log',stream=True,label=key,console=Console('compact'))
            write_json(folder/'process.json',proc)
        except Exception as exc:
            write_json(folder/'report.json',dict(status='launch_failed',error=repr(exc)))
        return key
    for completed,(_,key) in enumerate(execute_modes(queue,slots,run_one),1):
        print('Ended: '+key,flush=True)
        collect(root,plan,stage,queue)
        emit(root,stage,'worker_completed',workers_finished=completed,workers_total=len(queue),
             planned_module_trials=sum(len(t['modules']) for t in queue))
    return collect(root,plan,stage,queue)


def make_bundle(root):
    """Retain model/test evidence; omit reproducible environments/checkouts/weights."""
    import zipfile
    root=Path(root)
    with zipfile.ZipFile(str(root)+'.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for p in sorted(root.rglob('*')):
            relative=p.relative_to(root)
            if p.is_file() and not any(n in relative.parts for n in ('venv','.git','__pycache__','upstream')):
                archive.write(p,str(relative))
    return Path(str(root)+'.zip')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--action',choices=['plan','prepare','stress','small','run','report'],required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--jobs',type=int,choices=[1,2],default=2)
    parser.add_argument('--max-input-tokens',type=int,choices=[4096,6144])
    parser.add_argument('--max-new-tokens',type=int,choices=[512,1024])
    parser.add_argument('--test-output-contract',choices=['single-test-v1'])
    parser.add_argument('--mechanism',choices=['api-contract-v1'])
    args=parser.parse_args();root=args.output.resolve()
    saved = json.loads((root/'plan.json').read_text()) if args.action != 'plan' else None
    max_input=args.max_input_tokens or (saved['settings']['max_input_tokens'] if saved else 6144)
    max_output=args.max_new_tokens or (saved['settings']['max_new_tokens'] if saved else 1024)
    contract=args.test_output_contract or (saved['settings'].get('test_output_contract') if saved else None)
    mechanism=args.mechanism or (saved['settings'].get('mechanism') if saved else None)
    plan=build_plan(max_input,max_output,contract,mechanism)
    if args.action=='plan':
        root.mkdir(parents=True,exist_ok=False);write_json(root/'plan.json',plan)
        write_json(root/'environment.json',dict(python=sys.version,packages=package_versions()))
        print('Locked plan: '+str(root/'plan.json'));return 0
    validate_plan(root,plan)
    ok=False
    try:
        if args.action=='prepare':ok=prepare(root,plan)
        elif args.action in ('stress','small','run'):
            from pilot.gpu_lease import gpu_lease
            with gpu_lease(root,gpu_slots(args.jobs,'0,1' if args.jobs==2 else '0'),args.action):
                ok=stress(root,plan,args.jobs) if args.action=='stress' else execute(root,plan,'small' if args.action=='small' else 'main',args.jobs)
        elif args.action=='report':
            for stage in ('small','main'):
                if (root/(stage+'-queue.json')).exists():collect(root,plan,stage,json.loads((root/(stage+'-queue.json')).read_text()))
            ok=True
    except Exception as exc:
        write_json(root/(args.action+'-failure.json'),dict(error=repr(exc)))
        print(repr(exc),flush=True)
    finally:
        make_bundle(root)
    print('Reports: '+str(root));return 0 if ok else 2


if __name__=='__main__':
    sys.exit(main())
