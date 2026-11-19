"""Validated reuse of preparation and real GPU calibration in the same session.

Original diagnostic files remain unchanged. A derived calibration record states
its origin; it never certifies generation quality or replaces the small stage.
"""
import hashlib
import json
from pathlib import Path
import shutil
import time

from pilot.common import UPSTREAM, checked, command, digest, write_json
from pilot.attention import POLICY
from pilot.initialization_cache import cache_key

WRAPPER_SHA256='d9c922febd0de435ae4d1f35e5a673b05968104881f11eb9093985b4a46e296a'


def read(path):
    return json.loads(Path(path).read_text())


def initialization_settings(settings):
    """Only the declared generation-only output contract may differ on reuse.

    The backend must leave initialization messages/sampling unchanged. Exact
    prompt/runtime keys are still checked against every imported raw call.
    """
    comparable = dict(settings)
    contract = comparable.pop('test_output_contract', None)
    if contract not in (None, 'single-test-v1'):
        raise ValueError('Unrecognized generation-only output contract')
    mechanism = comparable.pop('mechanism', None)
    if mechanism not in (None, 'api-contract-v1'):
        raise ValueError('Unrecognized generation-only mechanism')
    if mechanism:
        if comparable.pop('acceptance_policy', None) != 'preserve-assertions-v1':
            raise ValueError('Mechanism requires the declared shared acceptance policy')
        if comparable.pop('api_contract_max_chars', None) != 2500:
            raise ValueError('Unrecognized API evidence budget')
    return comparable


def import_initialization_prefix(root,previous,plan,runtime):
    """Replay only verified greedy initialization outputs, never tests/outcomes.

    Re-key exact prompts after observational instrumentation changes. Full code
    fingerprints remain in the plan/receipt; input prompts and runtime must match.
    """
    root,previous=Path(root),Path(previous)
    prior_plan=read(previous/'plan.json')
    if (initialization_settings(prior_plan['settings'])!=initialization_settings(plan['settings'])
            or prior_plan['frame']!=plan['frame']):
        raise ValueError('Initialization reuse requires identical settings and source frame')
    if not plan['settings'].get('initialization_greedy'):
        raise ValueError('Only deterministic initialization may be imported')
    revisions=read(root/'resolved_models.json');entries={};logical_calls=0;fresh_calls=0;fresh_tokens=0
    versions=dict(quantization='nf4',torch=runtime['torch'],transformers=runtime['transformers'],
                  gpu=runtime['gpu'],loaded_model_revision=revisions['model'],attention_policy=POLICY)
    project=plan['small']['project']
    workers=[p.parent for p in (previous/'small').glob(project+'-*/worker-settings.json')]
    if len(workers)!=len(plan['arms']):raise ValueError('Missing prior initialization workers')
    for worker in workers:
        settings=read(worker/'worker-settings.json')
        if settings.get('fixture_mode') or any(settings.get(k)!=v for k,v in initialization_settings(plan['settings']).items()):
            raise ValueError('Prior worker does not have the same real model/settings')
        if settings['model_revision']!=revisions['model'] or settings['embedding_revision']!=revisions['embedding']:
            raise ValueError('Initialization model/embedding revision changed')
        if settings.get('adapter_source_hash')!=digest(prior_plan['source_sha256']):
            raise ValueError('Prior initialization source fingerprint disagrees with its plan')
        scope=read(worker/'analysis_scope.json')
        if scope.get('selected_generation_modules')!=plan['small']['modules']:
            raise ValueError('Prior analysis was not completed for the locked small frame')
        for relative,sha in read(root/'prepared'/project/'source_hashes.json').items():
            if hashlib.sha256((worker/'product'/relative).read_bytes()).hexdigest()!=sha:
                raise ValueError('Prior worker production source changed')
        calls=[json.loads(line) for line in (worker/'model_calls.jsonl').read_text().splitlines()]
        for call in calls:
            if call.get('phase')!='initialization':continue
            if call.get('error') or call.get('input_tokens',0)>plan['settings']['max_input_tokens']:
                raise ValueError('Invalid initialization call in prior evidence')
            old_key=cache_key(settings,versions,call['messages'])
            if old_key!=call.get('cache_key'):raise ValueError('Prior prompt/runtime cache key mismatch')
            cached=read(previous/'initialization-cache'/(old_key+'.json'))
            if cached.get('key')!=old_key or any(cached.get(k)!=call.get(k) for k in ('output','output_tokens','truncated')):
                raise ValueError('Prior cache output disagrees with raw model log')
            current=dict(settings,adapter_source_hash=digest(plan['source_sha256']))
            key=cache_key(current,versions,call['messages'])
            payload={k:cached[k] for k in ('output','output_tokens','truncated')};payload['key']=key
            if key in entries and entries[key]['payload']!=payload:raise ValueError('Conflicting greedy prefix outputs')
            entries[key]=dict(payload=payload,old_key=old_key,messages_sha256=digest(call['messages']))
            logical_calls+=1;fresh_calls+=bool(call.get('inference_started'))
            if call.get('inference_started'):fresh_tokens+=call['output_tokens']
    if not entries:raise ValueError('No initialization prefix to reuse')
    destination=root/'initialization-cache';destination.mkdir(exist_ok=False)
    for key,item in entries.items():write_json(destination/(key+'.json'),item['payload'])
    write_json(root/'initialization-reuse.json',dict(previous=str(previous),unique_prompts=len(entries),
        prior_logical_calls=logical_calls,prior_fresh_calls=fresh_calls,prior_fresh_output_tokens=fresh_tokens,
        truncated_prompts=sum(e['payload']['truncated'] for e in entries.values()),
        policy='exact prompt + same real model/runtime + greedy initialization only; source re-key documented',
        exclusions='No generation, repair, pytest, coverage or mutant outcomes imported',
        generation_output_contract=dict(previous=prior_plan['settings'].get('test_output_contract'),
                                        current=plan['settings'].get('test_output_contract'),
                                        scope='Generation/repair only; initialization prompts are unchanged'),
        cost='Original cold initialization cost remains in prior run; imported calls get cache_hit=true and zero fresh decode cost',
        keys={key:dict(old_key=v['old_key'],messages_sha256=v['messages_sha256']) for key,v in entries.items()}))


def verify_calibration(diagnostic,settings,revisions,runtime,previous):
    diagnostic=Path(diagnostic)
    provenance=read(diagnostic/'provenance.json')
    wrapper=(diagnostic/'attention-wrapper.py').read_bytes()
    if hashlib.sha256(wrapper).hexdigest()!=WRAPPER_SHA256 or provenance.get('wrapper_sha256')!=WRAPPER_SHA256:
        raise ValueError('Calibration wrapper differs from the audited efficient-SDPA adapter')
    if provenance.get('previous_study')!=str(Path(previous).resolve()):
        raise ValueError('Calibration belongs to a different previous study')
    expected=dict(initialization_settings(settings),model_revision=revisions['model'],seed=42)
    if settings.get('attention_policy')!=POLICY or read(diagnostic/'settings.json')!=expected or provenance.get('settings')!=expected:
        raise ValueError('Calibration configuration differs; no model/context/budget substitution')
    summary=read(diagnostic/'summary.json')
    if not summary.get('passed') or len(summary.get('results',[]))!=2:
        raise ValueError('Both real diagnostic processes must pass')
    if set(str(r.get('gpu')) for r in summary['results'])!={'0','1'}:
        raise ValueError('Calibration must cover the two visible GPU slots')
    accepted={}
    for record in summary['results']:
        gpu=str(record['gpu']);probe=read(diagnostic/('gpu-'+gpu)/'probe.json')
        proc=record['process'];versions=probe.get('versions',{})
        if not record.get('passed') or proc.get('returncode')!=0 or proc.get('timeout') or probe.get('status')!='passed':
            raise ValueError('Failed/timed-out calibration process')
        if record.get('probe')!=probe or probe.get('settings')!=expected:
            raise ValueError('Probe and process evidence disagree')
        if versions.get('loaded_model_revision')!=revisions['model'] or versions.get('quantization')!='nf4':
            raise ValueError('Calibration model revision/quantization mismatch')
        if any(versions.get(k)!=runtime.get(k) for k in ('torch','transformers','gpu')) or runtime.get('device_count')!=2:
            raise ValueError('Runtime/GPU profile changed; re-run calibration')
        tests=probe.get('tests',[])
        if len(tests)!=2 or probe.get('margin_gib')!=1.5 or any(
            not t.get('passed') or t.get('input_tokens')!=settings['max_input_tokens']
            or t.get('output_tokens')!=settings['max_new_tokens'] or t.get('conservative_headroom_gib',0)<1.5
            for t in tests):
            raise ValueError('Missing repeated maximum-context/full-decode/headroom evidence')
        accepted[gpu]=dict(status='passed',origin='validated_existing_session_diagnostic',process=proc,probe=probe)
    return accepted


def reuse_preparation(root,previous,diagnostic,plan):
    root,previous,diagnostic=map(lambda p:Path(p).resolve(),(root,previous,diagnostic))
    if any((root/name).exists() for name in ('preflight.json','stress.json','small','main')):
        raise ValueError('Resume output already attempted; keep evidence and use a fresh path')
    old_plan=read(previous/'plan.json');preflight=read(previous/'preflight.json')
    revisions=read(previous/'resolved_models.json')
    for key in ('upstream','frame','small','main','arms','mutation_limit'):
        if old_plan.get(key)!=plan.get(key):raise ValueError('Locked design changed: '+key)
    old_settings=dict(old_plan['settings']);old_settings['attention_policy']=POLICY
    if initialization_settings(old_settings)!=initialization_settings(plan['settings']):
        raise ValueError('Settings changed beyond audited attention/generation-only corrections')
    if set(preflight)!=set(plan['frame']) or any(p.get('status')!='prepared' for p in preflight.values()):
        raise ValueError('Previous preparation was not complete for every planned project')
    if checked(['git','-C',previous/'upstream','rev-parse','HEAD'])!=UPSTREAM:
        raise ValueError('Previous upstream revision changed')
    checked(['git','-C',previous/'upstream','diff','--exit-code','HEAD'])
    receipts={}
    for name,item in preflight.items():
        old_work=previous/'prepared'/name;spec=plan['frame'][name]
        if item.get('commit')!=spec['sha'] or not Path(item['python']).is_file():
            raise ValueError('Missing pinned project/environment: '+name)
        if checked(['git','-C',item['product'],'rev-parse','HEAD'])!=spec['sha']:
            raise ValueError('Project commit changed: '+name)
        hashes=read(old_work/'source_hashes.json')
        import_root=Path(item['import_root'])
        current={str(p.relative_to(import_root)):hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in (import_root/item['source_path']).rglob('*.py')
                 if not any(n in p.parts for n in ('tests','test','__pycache__'))}
        if current!=hashes:raise ValueError('Prepared production source changed: '+name)
        checked(['git','-C',item['product'],'diff','--exit-code','HEAD'])
        freeze=checked([item['python'],'-m','pip','freeze'],timeout=60)
        saved=(old_work/'requirements-resolved.txt').read_text()
        if sorted(freeze.splitlines())!=sorted(saved.strip().splitlines()):
            raise ValueError('Environment changed since preparation: '+name)
        destination=root/'prepared'/name;destination.mkdir(parents=True)
        for filename in ('source_hashes.json','mutant-pools.json','requirements-resolved.txt','import_check.json'):
            shutil.copy2(old_work/filename,destination/filename)
        receipts[name]=dict(python=item['python'],source_hashes=digest(hashes),freeze_sha256=hashlib.sha256(saved.encode()).hexdigest())
    # This short query loads no model. The inherited prepared venv must match the
    # actual successful diagnostic's Torch/Transformers and two-T4 profile.
    python=preflight[plan['small']['project']]['python']
    runtime=json.loads(checked([python,'-c',
        'import json,torch,transformers; print(json.dumps(dict(torch=torch.__version__,transformers=transformers.__version__,gpu=torch.cuda.get_device_name(0),device_count=torch.cuda.device_count())))'],timeout=60).splitlines()[-1])
    calibrated=verify_calibration(diagnostic,plan['settings'],revisions,runtime,previous)
    source=Path(read(diagnostic/'provenance.json')['source'])
    if hashlib.sha256((source/'gpu_context_probe.py').read_bytes()).hexdigest()!=read(diagnostic/'provenance.json')['probe_sha256']:
        raise ValueError('Original diagnostic probe source changed')
    shutil.copytree(diagnostic,root/'imported-calibration')
    write_json(root/'resolved_models.json',revisions)
    write_json(root/'preflight.json',preflight)
    (root/'upstream').symlink_to(previous/'upstream',target_is_directory=True)
    write_json(root/'stress.json',dict(config_hash=digest(plan['settings']),plan_hash=digest(plan),
        model_revision=revisions['model'],gpus=calibrated,
        origin='derived calibration binding; original diagnostic files are unchanged',
        source_evidence=str(diagnostic),source_summary_sha256=hashlib.sha256((diagnostic/'summary.json').read_bytes()).hexdigest()))
    started=time.time()
    write_json(root/'screen-clock.json',dict(started_epoch=started,deadline_epoch=started+plan['screen_budget_seconds'],
        budget_seconds=plan['screen_budget_seconds'],scope='small only; prior GPU calibration reused and cost reported separately'))
    write_json(root/'resume-provenance.json',dict(previous=str(previous),diagnostic=str(diagnostic),runtime=runtime,projects=receipts,
        settings_correction='common explicit KV repetition + efficient CUDA SDPA; model and budgets unchanged',
        test_output_contract=plan['settings'].get('test_output_contract'),
        skipped='installation, unit/CPU fixtures, preparation and repeated GPU calibration',
        limitation='same-session two-T4 profile; original diagnostic has no GPU UUID; not a generation-quality approval',
        source_changes=dict(previous=old_plan['source_sha256'],current=plan['source_sha256'])))
