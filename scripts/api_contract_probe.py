"""Paired mechanism diagnostic using fixed real upstream generation inputs.

This is not a new end-to-end Test4Py run or held-out confirmation. No repairs,
test pruning or outcome reuse. Source/model/calibration evidence is checked first.
"""
import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from pilot.common import write_json, command, digest
from pilot.api_contract import augment_prompt, build_api_contract
from pilot.quality import extract_code
from council.critic import audit_test_quality
from benchmark_worker import run_pytest
from pilot.benchmark import module_coverage
from pilot.module_mutation import verdict


def worker(args):
    from pilot.backend import TransformersBackend
    old_plan=json.loads((args.study/'plan.json').read_text())
    revisions=json.loads((args.study/'resolved_models.json').read_text())
    prepared_path=getattr(args,'prepared',None)
    prepared=json.loads(prepared_path.read_text()) if prepared_path else None
    if prepared is not None and not prepared['ready']:
        raise ValueError('All locked project imports must be prepared before inference')
    preflight=json.loads((args.study/'preflight.json').read_text())['genty'] if prepared is None else None
    manifest=json.loads(args.manifest.read_text())
    if manifest['model_revision']!=revisions['model']:
        raise ValueError('Diagnostic model revision changed')
    work=args.output/('gpu-'+args.gpu)
    work.mkdir(parents=True,exist_ok=False)
    cfg=dict(old_plan['settings'],model_revision=revisions['model'],seed=42)
    cfg.pop('test_output_contract',None)
    cfg.pop('mechanism',None)
    if cfg['max_input_tokens']!=4096 or cfg['max_new_tokens']!=512:
        raise ValueError('This diagnostic requires the locked 4096/512 calibration')
    model=TransformersBackend(cfg,work)
    measured=json.loads((args.study/('stress-gpu-'+args.gpu)/'probe.json').read_text())
    for k in ('torch','transformers','gpu','loaded_model_revision','quantization','attention_policy'):
        if model.versions.get(k)!=measured['versions'].get(k):
            raise ValueError('Model/runtime differs from real same-session calibration: '+k)
    results=[]
    jobs=[(target,arm) for index,target in enumerate(manifest['targets'])
          for ai,arm in enumerate(manifest['arms']) if (index+ai)%2==int(args.gpu)]
    for target,arm in jobs:
        case=work/(target['id']+'-'+arm);case.mkdir()
        row=dict(id=target['id'],project=target['project'],arm=arm,symbol=target['symbol'],module=target['module'],seed=target['seed'],
                 status='pending',first_pass=False,meaningful_target_test=False,source_review_required=True)
        try:
            if prepared is None:
                origin=Path(preflight['import_root']);test_python=None
                metadata=args.study/'prepared/genty'
            else:
                environment=prepared['projects'][target['project']]
                origin=Path(environment['source']);test_python=environment['interpreter']
                metadata=origin.parent
            hashes=json.loads((metadata/'source_hashes.json').read_text())
            pool=json.loads((metadata/'mutant-pools.json').read_text())
            if target.get('source_sha256') and hashes.get(target['file'])!=target['source_sha256']:
                raise ValueError('Target module differs from locked held-out frame')
            row['mutant_pool_sha256']=hashlib.sha256((metadata/'mutant-pools.json').read_bytes()).hexdigest()
            package=target['module'].split('.')[0]
            product=case/'product'
            shutil.copytree(origin,product,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc','Test4DT_tests','build','dist'))
            for relative,sha in hashes.items():
                if hashlib.sha256((product/relative).read_bytes()).hexdigest()!=sha:
                    raise ValueError('Pinned production source hash mismatch')
            messages=target['messages']
            if hashlib.sha256(json.dumps(messages,sort_keys=True).encode()).hexdigest()!=target['prompt_sha256']:
                raise ValueError('Fixed initial-generation prompt changed')
            if manifest.get('context_policy')=='source-first-v2' and arm!='baseline':
                from pilot.source_prompt import source_first_prompt
                if arm not in ('source_only','api_contract'):
                    raise ValueError('Unknown source-first ablation arm')
                system,user,evidence=source_first_prompt(messages[0]['content'],product,
                    target['file'],target['symbol'],target['module'],include_contract=arm=='api_contract')
            else:
                system,user,evidence=augment_prompt(messages[0]['content'],messages[1]['content'],
                    product,target['file'],target['symbol'],enabled=arm=='api_contract')
            write_json(case/'prompt.json',dict(system=system,user=user,evidence=evidence,
                base_prompt_sha256=target['prompt_sha256'],source='Fixed initial real upstream prompt; no outcome feedback'))
            model.phase=target['id']+'-'+arm
            model.torch.manual_seed(target['seed'])
            # Preserve upstream operation attribution for backend auditing.
            namespace={'__name__':'test4dt.api_contract_diagnostic','system':system,'user':user}
            exec('async def generate_test_case_normal(model):\n return await model.ask(system,user)',namespace)
            raw=asyncio.run(namespace['generate_test_case_normal'](model))
            (case/'raw.txt').write_text(raw)
            call=json.loads((work/'model_calls.jsonl').read_text().splitlines()[-1])
            row.update(input_tokens=call['input_tokens'],output_tokens=call['output_tokens'],
                       inference_seconds=call['seconds'],truncated=call['truncated'])
            if call['truncated']:
                row['status']='capped_output';continue
            code=extract_code(raw);compile(code,'<candidate>','exec')
            quality=audit_test_quality(code);row['quality']=quality
            path=product/'Test4DT_tests/test_generated.py';path.parent.mkdir(exist_ok=True);path.write_text(code)
            if not quality['valid_ast'] or quality['test_functions']==0 or quality['is_hollow'] or quality['tautological_assertions']:
                row['status']='quality_rejected';continue
            proc,report,_=run_pytest(product,case,'original',['Test4DT_tests/test_generated.py'],package,60,python=test_python)
            tests=report.get('tests',[])
            nodes=[t['nodeid'] for t in tests if t['outcome']=='passed']
            row.update(collected=len(tests),passed=len(nodes),first_pass=bool(proc['returncode']==0 and not proc['timeout'] and tests and len(nodes)==len(tests)))
            if not row['first_pass']:
                row['status']='pytest_failed';continue
            replay,replayed,cov=run_pytest(product,case,'replay',nodes,package,60,coverage=True,python=test_python)
            row['replay_stable']=bool(replay['returncode']==0 and not replay['timeout'] and
                set(t['nodeid'] for t in replayed.get('tests',[]) if t['outcome']=='passed')==set(nodes))
            row.update(module_coverage(cov,Path(target['file'])))
            facts=build_api_contract(product,target['file'],target['symbol'])
            entries=[v for k,v in cov.get('files',{}).items() if k.replace('\\','/').endswith(target['file'])]
            function=entries[0].get('functions',{}).get(facts['target']['symbol']) if len(entries)==1 else None
            row['target_covered_lines']=function.get('summary',{}).get('covered_lines') if function else None
            row['meaningful_target_test']=bool(row['first_pass'] and row['replay_stable'] and row.get('target_covered_lines',0))
            row['status']='scored' if row['replay_stable'] else 'replay_failed'
            row['mutants']=[]
            for mutant in pool[target['module']]['mutants']:
                mutated=case/('mutant-'+mutant['id'])/'product'
                shutil.copytree(product,mutated,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
                (mutated/target['file']).write_text(mutant['source'])
                mp,mr,_=run_pytest(mutated,case,'mutant-'+mutant['id']+'-evaluation',nodes,package,60,python=test_python)
                row['mutants'].append(dict(id=mutant['id'],verdict=verdict(mp,mr,nodes)))
            for relative,sha in hashes.items():
                if hashlib.sha256((product/relative).read_bytes()).hexdigest()!=sha:
                    raise ValueError('Production source changed during evaluation')
        except Exception as exc:
            row.update(status='error',error=repr(exc),traceback=traceback.format_exc())
        finally:
            if (case/'product').exists():
                try:source_ok=all(hashlib.sha256((case/'product'/p).read_bytes()).hexdigest()==sha for p,sha in hashes.items())
                except OSError:source_ok=False
                row['source_integrity']=source_ok
                if not source_ok:row.update(status='source_modified',first_pass=False,meaningful_target_test=False)
            write_json(case/'result.json',row);results.append(row)
            write_json(work/'results.json',results)
            print('PROBE_RESULT '+json.dumps({k:row.get(k) for k in ('id','arm','symbol','status','first_pass','meaningful_target_test','input_tokens','output_tokens')}),flush=True)
    return 0


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study',type=Path,required=True)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--gpu',choices=['0','1'])
    parser.add_argument('--prepared',type=Path,help='CPU-prepared held-out environments; test interpreters may differ from model interpreter')
    args=parser.parse_args()
    if args.gpu is not None:return worker(args)
    args.output.mkdir(parents=True,exist_ok=False)
    manifest=json.loads(args.manifest.read_text());write_json(args.output/'plan.json',manifest)
    old=json.loads((args.study/'plan.json').read_text())
    calibration=json.loads((args.study/'stress.json').read_text())
    if calibration['plan_hash']!=digest(old) or calibration['config_hash']!=digest(old['settings']):
        raise ValueError('Original integrated stress binding changed')
    for gpu in ('0','1'):
        record=calibration['gpus'][gpu]
        probe=json.loads((args.study/('stress-gpu-'+gpu)/'probe.json').read_text())
        if record['status']!='passed' or record['process']['returncode'] or record['process']['timeout'] or probe['status']!='passed':
            raise ValueError('Both original same-session stress processes must pass')
        largest=[r for r in probe['tests'] if r['input_tokens']==4096 and r['output_tokens']==512]
        if len(largest)<2 or any(not r['passed'] or r['conservative_headroom_gib']<1.5 for r in largest):
            raise ValueError('Missing repeated full-capacity memory evidence')
    write_json(args.output/'calibration-binding.json',dict(origin=str(args.study),stress_sha256=hashlib.sha256((args.study/'stress.json').read_bytes()).hexdigest(),
        scope='Same-session actual 14B/4096/512 memory evidence; not a new end-to-end pipeline run'))
    from pilot.gpu_lease import gpu_lease
    from paired_study import environment,make_bundle
    processes=[]
    try:
        with gpu_lease(args.output,['0','1'],'api-probe'):
            for gpu in ('0','1'):
                log=args.output/('gpu-'+gpu+'.log');stream=log.open('w')
                argv=[sys.executable,__file__,'--study',str(args.study),'--manifest',str(args.manifest),
                    '--output',str(args.output),'--gpu',gpu]
                if args.prepared:argv+=['--prepared',str(args.prepared)]
                proc=subprocess.Popen(argv,cwd=BASE,env=environment(gpu),stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
                processes.append((gpu,proc,stream))
            deadline=time.monotonic()+manifest.get('worker_timeout_seconds',1800)
            for gpu,proc,stream in processes:
                try:code=proc.wait(timeout=max(1,deadline-time.monotonic()))
                except subprocess.TimeoutExpired:
                    import signal
                    os.killpg(proc.pid,signal.SIGKILL);code=proc.wait()
                stream.close();write_json(args.output/('gpu-'+gpu+'-process.json'),dict(returncode=code))
            rows=[]
            for gpu,_,_ in processes:
                path=args.output/('gpu-'+gpu)/'results.json'
                if path.exists():rows.extend(json.loads(path.read_text()))
            planned=[dict(id=t['id'],project=t['project'],module=t['module'],symbol=t['symbol'],seed=t['seed'],arm=arm,status='not_completed',first_pass=None,meaningful_target_test=None)
                     for t in manifest['targets'] for arm in manifest['arms']]
            observed={(r['id'],r['arm']):r for r in rows}
            rows=[observed.get((r['id'],r['arm']),r) for r in planned]
            write_json(args.output/'summary.json',dict(stage=manifest.get('stage','development-only'),planned=len(planned),rows=rows,
                held_out_from_mechanism_development=bool(manifest.get('heldout',False)),
                source_review_required=True,full_pipeline_efficacy=False,heldout_confirmation=False))
    finally:make_bundle(args.output)
    return 0 if all(p.returncode==0 for _,p,_ in processes) else 2


if __name__=='__main__':sys.exit(main())
