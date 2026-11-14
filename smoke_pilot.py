"""Bounded, source-grounded PyCG integration screen BEFORE full Test4Py.

No upstream initialization/repair; not a replacement for the four-arm experiment.
"""
import argparse
import asyncio
import csv
import json
import os
from pathlib import Path
import shutil
import sys
import time
import traceback

from pilot.common import BASE, PYCG, checkout, command, digest, reserve_output, write_json, append_json, package_versions
from pilot.model_profiles import DEFAULT_MODEL, profile
from pilot.prescreen import sample_ids, summarize
from pilot.quality import source_context, extract_code, code_quality
from pilot.scoring import score, pytest_run, passed_nodes, classify
from pilot.setup import extract, select


def save_summary(output, rows, planned):
    summary = summarize(rows,planned)
    write_json(output/'summary.json', summary)
    fields=['sample_id','seed','status','ast_parse','assertions','passed','stable','loader_init_calls',
        'passing_target_reaching_nodeids','passing_source_ready_scenarios','target_branch_pct',
        'input_tokens','output_tokens','truncated_calls','seconds','failure_stage','failure_category','error']
    with (output/'samples.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
    lines=['# Small integration-screen report','',
        '**Not the upstream Test4Py experiment. No upstream initialization or repair.**',
        f"Finished: {summary['finished_candidates']}/{planned}; original-passing candidates: {summary['original_passing_candidates']}; passing rate: {summary['original_passing_candidate_rate']}.",
        f"Passing tests: {summary['original_passing_tests']}; AST valid candidates: {summary['ast_valid_candidates']}.",
        'One target; samples are stochastic generation attempts, not independent functions. No superiority/significance claim.',
        'Semantic assertion accuracy remains NA until independent review. Probe acceptance is not test success.',
        'Coverage and mutant results for each candidate are in sample score.json; never average missing coverage as zero.',
        '', '| Sample | Status | AST parse | Original pass count | Stable replay |', '|---|---|---|---:|---|']
    lines += [f"| {r['sample_id']} | {r['status']} | {r.get('ast_parse')} | {r.get('passed',0)} | {r.get('stable')} |" for r in rows]
    (output/'report.md').write_text('\n'.join(lines)+'\n')
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--population',type=int,default=100,help='planned generation attempts of the SAME target')
    parser.add_argument('--fraction',type=float,default=.1,help='deterministic fraction of planned attempt IDs; default 10/100')
    parser.add_argument('--samples',type=int,help='explicit number overrides fraction, e.g.100')
    parser.add_argument('--seed',type=int,default=42)
    parser.add_argument('--mode',choices=('baseline','caller','extracted','verified'),default='verified')
    parser.add_argument('--model',default=DEFAULT_MODEL)
    parser.add_argument('--model-revision')
    parser.add_argument('--max-new-tokens',type=int)
    parser.add_argument('--replays',type=int,default=3,help='additional clean-process replays of original-passing nodes')
    parser.add_argument('--plan-only',action='store_true',help='offline: write sampling plan only; no results generated')
    parser.add_argument('--output',type=Path,default=BASE/'runs'/'prescreen')
    args=parser.parse_args()
    try:
        ids=sample_ids(args.population,args.fraction,args.samples,args.seed)
        selected=profile(args.model)
        if args.replays<1 or args.max_new_tokens is not None and args.max_new_tokens<1:raise ValueError('replays and token cap must be positive')
    except ValueError as exc:parser.error(str(exc))
    output=reserve_output(args.output);started=time.perf_counter()
    settings=json.loads((BASE/'pilot.json').read_text())
    settings.update(model=args.model, model_revision=args.model_revision,model_profile=selected,
        max_new_tokens=args.max_new_tokens or selected['max_new_tokens'],seed=args.seed,cpu_threads=1,
        generation=dict(do_sample=True,temperature=.6,top_p=.95),
        prompt_policy='source-grounded-prescreen-v1',target_commit=PYCG)
    manifest=dict(kind='integration_screen_not_full_test4py',population=args.population,selected_ids=ids,
        settings=settings,mode=args.mode,replays=args.replays,
        status='plan_only' if args.plan_only else 'running',
        source_hashes={str(p.relative_to(BASE)):digest(p.read_text()) for p in
            [BASE/'smoke_pilot.py',*sorted((BASE/'pilot').glob('*.py'))]})
    write_json(output/'screen.json',manifest)
    print(f'Plan: {len(ids)}/{args.population} generation attempts; one target; mode={args.mode}; output={output}',flush=True)
    if args.plan_only:return 0
    rows=[]
    try:
        os.environ.setdefault('USE_TF','0');os.environ.setdefault('USE_FLAX','0')
        os.environ.setdefault('TOKENIZERS_PARALLELISM','false')
        for module in ('torch','transformers','pytest','pytest_jsonreport','coverage'):
            __import__(module)
        from huggingface_hub import model_info, snapshot_download
        settings['model_revision']=model_info(args.model,revision=args.model_revision).sha
        snapshot_download(args.model,revision=settings['model_revision'],ignore_patterns=['*.onnx','onnx/*','*.h5','*.msgpack'])
        manifest['settings']=settings;manifest['packages']=package_versions();write_json(output/'screen.json',manifest)
        product=output/'product'
        checkout('https://github.com/vitsalis/PyCG.git',PYCG,product)
        from pilot.backend import TransformersBackend
        backend=TransformersBackend(settings,output)
        for index,sample_id in enumerate(ids):
            work=output/'samples'/f'{sample_id:04d}';work.mkdir(parents=True)
            sample_started=time.perf_counter()
            row=dict(sample_id=sample_id,seed=args.seed+sample_id,status='running',passed=0,ast_parse=False,stable=None)
            try:
                # Copy a pristine pinned checkout for every attempt. Scoring always starts fresh processes.
                root=work/'PyCG'
                shutil.copytree(product,root,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc','Test4DT_tests'))
                context=''
                if args.mode!='baseline':
                    extraction=extract(root);write_json(work/'candidates.json',extraction)
                    context,selection=select(root,extraction,args.mode,work,settings)
                prompt=source_context(root)+'\n\n'+settings['scenario_prompt']+'\n\n'+context
                (work/'prompt.txt').write_text(prompt)
                backend.work=work;backend.phase='prescreen_generation';backend.torch.manual_seed(row['seed'])
                try:
                    raw=asyncio.run(backend.ask('Generate a complete pytest file using real product imports. Return one Python code block. Do not reimplement production code.',prompt))
                except Exception:
                    row['status']='generation_error';raise
                try:code=extract_code(raw)
                except Exception:
                    row['status']='extraction_error';raise
                (work/'generated.py').write_text(code);row.update(code_quality(code))
                testdir=root/'Test4DT_tests';testdir.mkdir();(testdir/'test_generated.py').write_text(code)
                shutil.copyfile(BASE/'pilot/screen_trace.py',testdir/'conftest.py')
                row['score']=score(root,work,settings)
                row.update(status='evaluated',passed=row['score'].get('passed',0),mutants=row['score'].get('mutants',[]))
                from analyze import scoped_coverage
                row['target_branch_pct']=scoped_coverage(row['score'],settings['target_function']).get('target_branch_pct')
                if row['score']['status'] not in {'scored','no_generated_tests'}:
                    proc=row['score'].get('original_process',{})
                    diagnostic=proc.get('stdout','')+'\n'+proc.get('stderr','')
                    row['failure_category']=classify(diagnostic)
                    # Collection errors in model code are an unsuccessful candidate, not automatically infrastructure failure.
                    if proc.get('returncode')==2 and not proc.get('timeout'):
                        row['failure_stage']='pytest_collection'
                    else:row['status']='environment_error'
                eligible=row['score'].get('eligible_nodeids',[])
                trace_path=work/'original/receiver_trace.json'
                traces=json.loads(trace_path.read_text()) if trace_path.exists() else []
                row['loader_init_calls']=len(traces)
                row['passing_target_reaching_nodeids']=sorted({t.get('nodeid') for t in traces if t.get('nodeid') in eligible})
                row['passing_source_ready_scenarios']=sorted({
                    'existing_target' if t['destination_existed'] else 'new_target'
                    for t in traces if t.get('nodeid') in eligible and t.get('source_ready')
                    and t.get('fullname')=='pkg.dep' and t.get('path')=='new.py'})
                if eligible:
                    replay_results=[]
                    for replay in range(args.replays):
                        proc,data,_=pytest_run(root,work,f'replay_{replay+1}',eligible,settings['score_timeout'])
                        replay_results.append(dict(passed=passed_nodes(data),process=proc))
                    row['stable']=all(not x['process']['timeout'] and x['process']['returncode']==0 and set(x['passed'])==set(eligible) for x in replay_results)
                    write_json(work/'replays.json',replay_results)
            except Exception as exc:
                if row['status']=='running':row['status']='environment_error'
                row.update(error=repr(exc),traceback=traceback.format_exc())
            calls_path=work/'model_calls.jsonl'
            calls=[json.loads(line) for line in calls_path.read_text().splitlines()] if calls_path.exists() else []
            row['input_tokens']=sum(c.get('input_tokens',0) for c in calls)
            row['output_tokens']=sum(c.get('output_tokens',0) for c in calls)
            row['truncated_calls']=sum(bool(c.get('truncated')) for c in calls)
            row['seconds']=time.perf_counter()-sample_started
            write_json(work/'sample.json',row);append_json(output/'samples.jsonl',row);rows.append(row)
            summary=save_summary(output,rows,len(ids))
            print(f"Progress {index+1}/{len(ids)} | status={row['status']} | original-pass={row['passed']} | passing candidates={summary['original_passing_candidates']}/{index+1}",flush=True)
        manifest['status']='screen_finished_review_quality'
    except Exception as exc:
        manifest.update(status='preflight_failed',error=repr(exc),traceback=traceback.format_exc())
    manifest['seconds']=time.perf_counter()-started
    manifest['quality']=save_summary(output,rows,len(ids))
    write_json(output/'screen.json',manifest)
    print(f"Screen status: {manifest['status']}; report: {output/'report.md'}",flush=True)
    return 0 if manifest['status']=='screen_finished_review_quality' else 1


if __name__=='__main__':raise SystemExit(main())
