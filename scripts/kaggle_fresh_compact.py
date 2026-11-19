"""Fresh-session compact small screen; no larger inference stage."""
import hashlib
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback
import zipfile

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('source',type=Path)
parser.add_argument('root',type=Path)
parser.add_argument('--mechanism',choices=['api-contract-v1'])
parser.add_argument('--action',choices=['small','probe'],default='small')
arguments=parser.parse_args()
if arguments.action=='probe' and not arguments.mechanism:
    parser.error('The mechanism diagnostic requires --mechanism api-contract-v1')
source,root=arguments.source,arguments.root
status_path = Path('/kaggle/working/TEST4PY_FRESH_STATUS.json')
state = dict(status='running', source=str(source), root=str(root), started_epoch=time.time(),
             scope='API mechanism diagnostic only; no larger campaign' if arguments.action=='probe'
                   else 'Two-module compact engineering screen only; no larger campaign')
log = Path('/kaggle/working') / ('FRESH_COMPACT_'+root.name+'.log')
env = dict(os.environ, PYTHONUNBUFFERED='1', USE_TF='0', USE_FLAX='0', TOKENIZERS_PARALLELISM='false')
python = '/tmp/test4py-modern/bin/python'

def save(phase):
    state['phase'] = phase
    state['updated_epoch'] = time.time()
    status_path.write_text(json.dumps(state, indent=2))
    if root.exists():
        (root/'remote-execution.json').write_text(json.dumps(state, indent=2))
        if not (root/'remote-small.log').exists():
            (root/'remote-small.log').symlink_to(log)

def run(phase, args, timeout=1800):
    save(phase)
    print('STEP',phase,flush=True)
    result=subprocess.run(list(map(str,args)),cwd=source,env=env,check=False,timeout=timeout)
    if result.returncode:
        raise RuntimeError('Step '+phase+' exited '+str(result.returncode))

try:
    tools = Path('/tmp')/('test4py-tools-'+root.name)
    run('bootstrap-tools', [sys.executable,'-m','venv','--without-pip',tools], timeout=120)
    run('install-uv', [sys.executable,'-m','pip','--python',tools/'bin/python','install','uv==0.6.17'], timeout=300)
    env['PATH']=str(tools/'bin')+os.pathsep+env['PATH']
    run('bootstrap-runtime',[sys.executable,source/'bootstrap_modern.py'])
    run('paired-dependencies',[python,'-m','pip','install','-r',source/'requirements-paired.txt'])
    policy=['--mechanism',arguments.mechanism] if arguments.mechanism else ['--test-output-contract','single-test-v1']
    run('freeze-plan',[python,source/'paired_study.py','--action','plan','--output',root,
                       '--max-input-tokens','4096','--max-new-tokens','512',*policy],timeout=90)
    shutil.copy2(source/'notebook-source.json',root/'notebook-source.json')
    archive=Path('/kaggle/working/PRIOR_14B_INITIALIZATION_EVIDENCE.zip')
    original_sha='603266e8f6360ae0fc86d93d2bed7edc131db23a81448017a80202518d566b3a'
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=original_sha:
        raise ValueError('Prior evidence archive hash mismatch')
    previous=root/'imported-prior-evidence'
    previous.mkdir(exist_ok=False)
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            target=(previous/info.filename).resolve()
            if not target.is_relative_to(previous.resolve()):
                raise ValueError('Unsafe prior archive member')
            if info.is_dir():
                target.mkdir(parents=True,exist_ok=True)
            else:
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(z.read(info))
    # Pin the same immutable real model/embedding before new preparation.
    shutil.copy2(previous/'resolved_models.json',root/'resolved_models.json')
    run('prepare-fresh-projects',[python,source/'paired_study.py','--action','prepare','--output',root])
    importer = '''import json, subprocess, sys
from pathlib import Path
from paired_study import build_plan,validate_plan
from pilot.reuse import import_initialization_prefix
from pilot.common import write_json
root,previous=map(Path,sys.argv[1:])
saved=json.loads((root/'plan.json').read_text())
plan=build_plan(saved['settings']['max_input_tokens'],saved['settings']['max_new_tokens'],saved['settings'].get('test_output_contract'),saved['settings'].get('mechanism'))
validate_plan(root,plan)
prepared=json.loads((root/'preflight.json').read_text())
runtime=json.loads(subprocess.check_output([prepared[plan['small']['project']]['python'],'-c',
 'import json,torch,transformers; print(json.dumps(dict(torch=torch.__version__,transformers=transformers.__version__,gpu=torch.cuda.get_device_name(0),device_count=torch.cuda.device_count())))'],text=True).splitlines()[-1])
import_initialization_prefix(root,previous,plan,runtime)
write_json(root/'initialization-import-provenance.json',dict(origin='Prior real greedy initialization from an earlier Kaggle session',original_archive_sha256='603266e8f6360ae0fc86d93d2bed7edc131db23a81448017a80202518d566b3a',fresh_preparation=True,calibration='Must run fresh two-GPU stress next; earlier-session calibration is not reused',runtime=runtime,exclusions='No test generation, repair, pytest, coverage or mutant outcomes imported'))
print('Verified cross-session initialization outputs only; fresh hardware calibration still required.',flush=True)
'''
    run('verify-initialization-only',[python,'-c',importer,root,previous],timeout=180)
    run('fresh-gpu-calibration',[python,source/'paired_study.py','--action','stress','--output',root,'--jobs','2'],timeout=3700)
    if arguments.action=='probe':
        run('real-api-contract-probe',[python,source/'scripts/api_contract_probe.py','--study',root,
            '--manifest',source/'research/benchmark/api_contract_development_probe.json','--output',root/'diagnostic'],timeout=3700)
    else:
        run('real-compact-small',[python,source/'paired_study.py','--action','small','--output',root,'--jobs','2'],timeout=3700)
    state.update(status='completed',returncode=0)
except BaseException as exc:
    state.update(status='failed',error=repr(exc),traceback=traceback.format_exc())
    print('DRIVER ERROR',repr(exc),flush=True)
finally:
    state['ended_epoch']=time.time()
    state['seconds']=state['ended_epoch']-state['started_epoch']
    save('finished')
    if root.exists():
        sys.path.insert(0,str(source))
        from paired_study import make_bundle
        make_bundle(root)
    print('FINAL',json.dumps(state),flush=True)

raise SystemExit(0 if state["status"] == "completed" else 2)
