"""19/183-module NA-subset baseline, using upstream Test4Py init/generation/repair.

Selection frame is NA58, balanced across its nine projects. NOT a uniform sample
of all183, NOT evaluation of the PyCG-specific setup extension.
"""
import argparse
import csv
import json
import os
from pathlib import Path
import sys
import time
import traceback
import urllib.request

from pilot.common import BASE,UPSTREAM,checkout,command,digest,reserve_output,write_json
from pilot.benchmark import select_modules,locate_module,module_coverage
from pilot.model_profiles import DEFAULT_MODEL,profile
from pilot.scheduling import gpu_slots,execute_modes
from pilot.console import Console

DATA=BASE/'research/benchmark'


def resolve_revision(spec):
    prefix=spec['commit_prefix']
    if len(prefix)==40:return prefix
    repo=spec['repo'].removeprefix('https://github.com/').removesuffix('.git')
    request=urllib.request.Request(f'https://api.github.com/repos/{repo}/commits/{prefix}',headers={'User-Agent':'Test4Py-research-pilot'})
    with urllib.request.urlopen(request,timeout=60) as stream:sha=json.load(stream)['sha']
    if len(sha)!=40 or not sha.startswith(prefix):raise ValueError('Commit prefix did not resolve to expected revision')
    return sha


def export_report(root,plan,state):
    rows=[]
    for selected in plan['selected']:
        project,module=selected['project'],selected['module']
        path=root/'projects'/project/'report.json'
        report=json.loads(path.read_text()) if path.exists() else {}
        row=next((dict(r) for r in report.get('modules',[]) if r['module']==module),
            dict(project=project,module=module,status=state['projects'].get(project,{}).get('status','pending'),
                 passed=None,line_pct=None,branch_pct=None,mutation_score=None))
        row['reference_line_pct']=None;row['reference_branch_pct']=None
        reference=root/'upstream/ex-results/ex1/coverage_results'/project/'Test4DT_tests/coverage.json'
        if reference.exists():
            cov=json.loads(reference.read_text());relative=Path(*module.split('.')).with_suffix('.py')
            metrics=module_coverage(cov,relative)
            row.update(reference_line_pct=metrics.get('line_pct'),reference_branch_pct=metrics.get('branch_pct'))
        rows.append(row)
    columns=['project','module','status','passed','retained_files','line_pct','branch_pct','covered_lines','total_lines',
        'covered_branches','total_branches','reference_line_pct','reference_branch_pct','mutation_score','semantic_assertion_accuracy']
    with (root/'modules.csv').open('w') as stream:
        writer=csv.DictWriter(stream,fieldnames=columns,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
    eligible=[r for r in rows if r['status']=='scored']
    state['quality']=dict(planned_modules=len(rows),scored_modules=len(eligible),
        modules_with_passing_tests=sum(bool(r.get('passed')) for r in rows),
        passing_tests=sum(r.get('passed') or 0 for r in rows),
        independent_projects=len({r['project'] for r in rows}),
        mean_line_pct=sum(r['line_pct'] for r in eligible if r.get('line_pct') is not None)/sum(r.get('line_pct') is not None for r in eligible) if any(r.get('line_pct') is not None for r in eligible) else None,
        mean_branch_pct=sum(r['branch_pct'] for r in eligible if r.get('branch_pct') is not None)/sum(r.get('branch_pct') is not None for r in eligible) if any(r.get('branch_pct') is not None for r in eligible) else None,
        missing_not_zero=True,setup_extension_evaluated=False,mutation_score=None)
    write_json(root/'benchmark.json',state)
    lines=['# 19-module NA-subset Test4Py baseline','',
        '**19 of183 modules, sampled within NA58 with project-balanced selection. Not representative of all183.**',
        '**No general setup adapter: this batch evaluates baseline only. Mutation/semantic accuracy not measured.**',
        f"Scored modules: {len(eligible)}/{len(rows)}; modules with original-passing tests: {state['quality']['modules_with_passing_tests']}.",
        'Selected modules share project initialization; token/time costs are project-level. Do not assign full project cost to every module.',
        'Reference columns come from frozen upstream ex1 artifacts where matching module coverage is available; different model/runtime/protocol, descriptive only.',
        'Reported means condition on scored modules; failures remain visible and no missing outcome is imputed as zero. Report the denominator with every mean.',
        '', '| Project | Module | Status | Pass | Line % | Branch % |', '|---|---|---|---:|---:|---:|']
    lines += [f"| {r['project']} | {r['module']} | {r['status']} | {r.get('passed')} | {r.get('line_pct')} | {r.get('branch_pct')} |" for r in rows]
    (root/'report.md').write_text('\n'.join(lines)+'\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--action',choices=('plan','prepare','run'),default='plan')
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--resume',action='store_true',help='continue exactly the same selected plan/config; no successful project rerun')
    parser.add_argument('--rounds',type=int,default=3)
    parser.add_argument('--model',default=DEFAULT_MODEL)
    parser.add_argument('--model-revision')
    parser.add_argument('--embedding-revision')
    parser.add_argument('--max-new-tokens',type=int)
    parser.add_argument('--seed',type=int,default=42)
    parser.add_argument('--jobs',type=int,default=2)
    parser.add_argument('--gpus',default='auto')
    parser.add_argument('--worker-timeout',type=int,default=7200)
    parser.add_argument('--score-timeout',type=int,default=120)
    args=parser.parse_args()
    if min(args.rounds,args.jobs,args.worker_timeout,args.score_timeout)<1 or args.max_new_tokens is not None and args.max_new_tokens<1:parser.error('positive limits required')
    projects=json.loads((DATA/'projects-upstream.json').read_text());registry=json.loads((DATA/'na-projects.json').read_text())
    if sum(len(v) for v in projects.values())!=183 or sum(len(projects[p]) for p in registry)!=58:raise ValueError('Sampling frame mismatch')
    selected=select_modules(projects,registry,19,args.seed)
    settings=dict(model=args.model,model_revision=args.model_revision,embedding_revision=args.embedding_revision,
        rounds=args.rounds,max_new_tokens=args.max_new_tokens or profile(args.model)['max_new_tokens'],seed=args.seed,
        model_profile=profile(args.model),cpu_threads=1,generation=dict(do_sample=False,seed=args.seed),
        worker_timeout=args.worker_timeout,score_timeout=args.score_timeout,
        embedding='BAAI/bge-large-en-v1.5',prompt_policy='source-grounded-module-v1',code_extraction='single-complete-block-v2')
    plan=dict(selected=selected,settings=settings,upstream=UPSTREAM,sampling_frame='NA58 within183',
        selection='balanced cyclic project allocation; shuffled within project using seed; not uniform183',
        registry=registry,frame_hash=digest(projects),reference='https://arxiv.org/html/2503.14000v2#S4.T1',
        runner_source_hashes={str(p.relative_to(BASE)):digest(p.read_text()) for p in
            [BASE/'benchmark19.py',BASE/'benchmark_worker.py',BASE/'requirements-modern.txt',*sorted((BASE/'pilot').glob('*.py'))]})
    root=args.output.resolve()
    if args.resume:
        saved=json.loads((root/'plan.json').read_text())
        if digest(saved)!=digest(plan):parser.error('Resume plan/config/source mismatch; choose a new output directory')
        state=json.loads((root/'benchmark.json').read_text())
    else:
        root=reserve_output(root);write_json(root/'plan.json',plan)
        state=dict(status='planned',projects={},quality={},plan_hash=digest(plan),output=str(root))
    started=time.perf_counter();state['current_action']=args.action
    print(f'NA subset19/183 (19/58 NA),9 projects, baseline only. Output: {root}',flush=True)
    export_report(root,plan,state)
    if args.action=='plan':return 0
    console=Console('compact')
    try:
        upstream=root/'upstream'
        if not upstream.exists():checkout('https://github.com/Test4DT/Test4Py.git',UPSTREAM,upstream)
        if digest(json.loads((upstream/'projects.json').read_text()))!=plan['frame_hash']:raise ValueError('Frozen module frame differs from pinned upstream')
        from huggingface_hub import model_info,snapshot_download
        # Resolve once; preserve exact revisions when resuming a partially executed batch.
        revisions=state.setdefault('resolved_revisions',{})
        if args.action=='run':
            if not revisions.get('model'):revisions['model']=model_info(args.model,revision=args.model_revision).sha
            if not revisions.get('embedding'):revisions['embedding']=model_info(settings['embedding'],revision=args.embedding_revision).sha
            settings.update(model_revision=revisions['model'],embedding_revision=revisions['embedding'])
            embedding_path=snapshot_download(settings['embedding'],revision=revisions['embedding'],ignore_patterns=['*.onnx','onnx/*','*.h5','*.msgpack'])
            snapshot_download(args.model,revision=revisions['model'],ignore_patterns=['*.onnx','onnx/*','*.h5','*.msgpack'])
            state['resolved_revisions']=revisions;export_report(root,plan,state)
            slots=gpu_slots(args.jobs,args.gpus)
        else:embedding_path=None;slots=[None]
        groups={p:[r['module'] for r in selected if r['project']==p] for p in sorted(registry)}
        pending=[p for p in groups if state['projects'].get(p,{}).get('status')!='execution_complete']
        def run_project(project,gpu):
            work=root/'projects'/project
            previous=state['projects'].get(project,{})
            if work.exists() and previous.get('status') not in (None,'prepared'):
                # Never mix a failed generation attempt with its replacement.
                archive=root/'previous-attempts'/project/str(time.time_ns())
                archive.parent.mkdir(parents=True,exist_ok=True);work.rename(archive)
            work.mkdir(parents=True,exist_ok=True)
            item=dict(status='preparing',modules=groups[project],gpu=gpu);t=time.perf_counter()
            try:
                product=work/'source';spec=registry[project]
                version_path=work/'source_revision.json'
                if version_path.exists():revision=json.loads(version_path.read_text())['sha']
                else:
                    revision=resolve_revision(spec);write_json(version_path,dict(**spec,sha=revision,evidence=plan['reference']))
                if not product.exists():checkout(spec['repo'],revision,product)
                actual=command(['git','-C',product,'rev-parse','HEAD'])
                if actual['returncode'] or actual['stdout'].strip()!=revision:raise ValueError('Source commit mismatch')
                locations=[locate_module(product,m) for m in groups[project]]
                import_roots={str(x[1]) for x in locations};source_paths={str(x[2]) for x in locations}
                if len(import_roots)!=1 or len(source_paths)!=1:raise ValueError('Selected modules require different import roots; split project worker first')
                import_root=Path(next(iter(import_roots)));source_path=Path(next(iter(source_paths)))
                # ProjectMessage source_path is relative to its import root.
                source_path=str((product/source_path).relative_to(import_root))
                venv=work/'venv';python=venv/'bin/python'
                marker=work/'prepared.json'
                if not marker.exists():
                    bootstrap=command([sys.executable,BASE/'bootstrap_modern.py','--venv',venv],cwd=BASE,
                        timeout=1800,log_path=work/'bootstrap.log',stream=True,label=project,console=console)
                    if bootstrap['returncode'] or bootstrap['timeout']:raise RuntimeError('Runtime bootstrap failed; see bootstrap.log')
                    packaging=any((product/n).exists() for n in ('pyproject.toml','setup.py','setup.cfg'))
                    if packaging:install=[str(python),'-m','pip','install','-c',str(BASE/'requirements-modern.txt'),'-e',str(product)]
                    elif (product/'requirements.txt').exists():install=[str(python),'-m','pip','install','-c',str(BASE/'requirements-modern.txt'),'-r',str(product/'requirements.txt')]
                    else:install=None
                    if install:
                        proc=command(install,cwd=product,timeout=1200,log_path=work/'dependencies.log')
                        if proc['returncode'] or proc['timeout']:raise RuntimeError('Project dependencies failed; see dependencies.log')
                    check=command([python,'-c','import importlib,sys; [importlib.import_module(x) for x in sys.argv[1:]]',*groups[project]],
                        cwd=import_root,timeout=120,env=dict(os.environ,PYTHONPATH=str(import_root),PYTHONDONTWRITEBYTECODE='1',USE_TF='0',USE_FLAX='0'))
                    write_json(work/'import_check.json',check)
                    if check['returncode'] or check['timeout']:raise RuntimeError('Selected module import failed; see import_check.json')
                    write_json(marker,dict(revision=revision,modules=groups[project],python=str(python)))
                tracked=command(['git','-C',product,'diff','--exit-code','HEAD'],timeout=60)
                if tracked['returncode']:raise RuntimeError('Dependency installation modified tracked product source; not running altered benchmark')
                freeze=command([python,'-m','pip','freeze'],timeout=60)
                (work/'requirements-resolved.txt').write_text(freeze['stdout'])
                item['preparation_seconds']=time.perf_counter()-t
                if args.action=='prepare':item['status']='prepared';return item
                config=dict(settings,project=project,modules=groups[project],import_root=str(import_root),
                    source_path=source_path,target_commit=revision)
                write_json(work/'worker-settings.json',config)
                env=dict(os.environ,OPENAI_API_KEY='local-inference',USER_PYTHON_PATH=str(python),
                    PYTHONPATH=os.pathsep.join(map(str,(upstream,import_root,BASE))),TRANSFORMER_PATH=embedding_path,
                    USE_TF='0',USE_FLAX='0',PYTHONUNBUFFERED='1',PYTHONDONTWRITEBYTECODE='1',
                    PYTHONHASHSEED=str(args.seed),TOKENIZERS_PARALLELISM='false',
                    PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTEST_PLUGINS='pytest_jsonreport.plugin',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
                if gpu is not None:env['CUDA_VISIBLE_DEVICES']=str(gpu)
                proc=command([python,BASE/'benchmark_worker.py',work/'worker-settings.json'],cwd=import_root,env=env,
                    timeout=args.worker_timeout,stream=True,label=project,log_path=work/'worker.log',console=console)
                write_json(work/'process.json',proc)
                report=json.loads((work/'report.json').read_text()) if (work/'report.json').exists() else {}
                item['status']=report.get('status','failed') if proc['returncode']==0 and not proc['timeout'] else 'failed'
            except Exception as exc:item.update(status='preflight_failed',error=repr(exc),traceback=traceback.format_exc())
            finally:item['seconds']=time.perf_counter()-t
            return item
        for completed,(project,item) in enumerate(execute_modes(pending,slots,run_project),1):
            state['projects'][project]=item;export_report(root,plan,state)
            print(f"Projects ended this action {completed}/{len(pending)} | {project}: {item['status']} | scored modules {state['quality']['scored_modules']}/19",flush=True)
        wanted='prepared' if args.action=='prepare' else 'execution_complete'
        state['status']='complete' if all(x.get('status') in {wanted,'execution_complete'} for x in state['projects'].values()) and len(state['projects'])==9 else 'partial_failure'
    except Exception as exc:state.update(status='preflight_failed',error=repr(exc),traceback=traceback.format_exc())
    state.setdefault('action_history',[]).append(dict(action=args.action,seconds=time.perf_counter()-started,status=state['status']))
    export_report(root,plan,state)
    print(f"Status: {state['status']}; report: {root/'report.md'}",flush=True)
    return 0 if state['status']=='complete' else 1


if __name__=='__main__':raise SystemExit(main())
