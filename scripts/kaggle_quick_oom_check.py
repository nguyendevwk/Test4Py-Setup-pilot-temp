"""Paste this complete file into ONE Code cell in the existing Kaggle session.

Reuse the already validated environment/weights. No installs, source edits,
benchmark generation or readiness overrides. Memory diagnostic only.
"""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
import sys
import zipfile

OLD_ROOT=Path('/kaggle/working/UPSTREAM_NF4_20261116T170358791891Z')
SOURCE=Path('/kaggle/working/Test4Py_upstream_20261116T170358791891Z')
PYTHON='/tmp/test4py-modern/bin/python'
assert OLD_ROOT.is_dir() and SOURCE.is_dir() and Path(PYTHON).exists(), (
    'Use the existing Kaggle session. This quick check requires its prepared environment and cached weights.')
sys.path.insert(0,str(SOURCE))
from pilot.common import command
from pilot.console import Console
from pilot.scheduling import gpu_slots

slots=gpu_slots(2,'0,1')
assert len(slots)==2,'This diagnostic expects the same two visible T4s.'
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
DIAGNOSTIC=Path('/kaggle/working')/('NF4_14B_OOM_CHECK_'+stamp)
DIAGNOSTIC.mkdir(exist_ok=False)
config=json.loads((OLD_ROOT/'stress-settings.json').read_text())
assert config['model']=='Qwen/Qwen2.5-Coder-14B-Instruct' and config['quantization']=='nf4'
assert config['max_input_tokens']==4096 and config['max_new_tokens']==512
config['attention_policy']='t4-efficient-sdpa-v1'
(DIAGNOSTIC/'settings.json').write_text(json.dumps(config,indent=2))

# Adapter exists only inside each temporary diagnostic process. Original study
# source, frozen plan, GPU margin and failed evidence remain untouched.
wrapper='''import runpy,sys
from transformers import AutoModelForCausalLM
from transformers.integrations import sdpa_attention
from torch.nn.attention import SDPBackend,sdpa_kernel
sdpa_attention.use_gqa_in_sdpa=lambda attention_mask,key:False
original=AutoModelForCausalLM.from_pretrained
def load(*args,**kwargs):
    kwargs['attn_implementation']='sdpa'
    return original(*args,**kwargs)
AutoModelForCausalLM.from_pretrained=staticmethod(load)
script=sys.argv[1]
sys.argv=sys.argv[1:]
with sdpa_kernel(backends=[SDPBackend.EFFICIENT_ATTENTION]):
    runpy.run_path(script,run_name='__main__')
'''
(DIAGNOSTIC/'attention-wrapper.py').write_text(wrapper)
(DIAGNOSTIC/'provenance.json').write_text(json.dumps(dict(
    kind='memory diagnostic only; not efficacy or larger-run gate evidence',
    previous_study=str(OLD_ROOT),source=str(SOURCE),settings=config,
    wrapper_sha256=hashlib.sha256(wrapper.encode()).hexdigest(),
    probe_sha256=hashlib.sha256((SOURCE/'gpu_context_probe.py').read_bytes()).hexdigest(),
    skipped='unit tests, dependency installation, prepare, CPU fixtures and benchmark generation',
    per_gpu_timeout_seconds=900),indent=2))

def check(gpu):
    env=dict(os.environ,CUDA_VISIBLE_DEVICES=str(gpu),USE_TF='0',USE_FLAX='0',
             PYTHONPATH=str(SOURCE),PYTHONUNBUFFERED='1',TOKENIZERS_PARALLELISM='false')
    result=command([PYTHON,DIAGNOSTIC/'attention-wrapper.py',SOURCE/'gpu_context_probe.py',
        '--settings',DIAGNOSTIC/'settings.json','--output',DIAGNOSTIC/('gpu-'+str(gpu)),
        '--inputs','4096','--output-tokens','512','--headroom-gib','1.5'],
        cwd=SOURCE,env=env,timeout=900,log_path=DIAGNOSTIC/('gpu-'+str(gpu)+'.log'),
        stream=True,label='quick-'+str(gpu),console=Console('compact'))
    probe=DIAGNOSTIC/('gpu-'+str(gpu))/'probe.json'
    data=json.loads(probe.read_text()) if probe.exists() else {}
    return dict(gpu=gpu,process=result,probe=data,
                passed=result['returncode']==0 and not result['timeout'] and data.get('status')=='passed')

results=[]
with ThreadPoolExecutor(max_workers=2) as executor:
    futures=[executor.submit(check,gpu) for gpu in slots]
    for future in as_completed(futures):
        try:record=future.result()
        except Exception as exc:record=dict(passed=False,error=repr(exc))
        results.append(record)
        print('GPU:',record.get('gpu'),'PASS:',record['passed'],flush=True)
        for test in record.get('probe',{}).get('tests',[]):print(test,flush=True)
        if not record['passed']:
            print('ERROR:',record.get('probe',{}).get('error',record.get('error')),flush=True)
            print('Log tail:',record.get('process',{}).get('stdout','')[-5000:],flush=True)
        (DIAGNOSTIC/'summary.json').write_text(json.dumps(dict(
            kind='memory diagnostic only',results=results,
            passed=len(results)==2 and all(r['passed'] for r in results)),indent=2))

archive=Path(str(DIAGNOSTIC)+'.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as bundle:
    for path in DIAGNOSTIC.rglob('*'):
        if path.is_file():bundle.write(path,str(path.relative_to(DIAGNOSTIC)))
from IPython.display import display,FileLink
display(FileLink(str(archive)))
print('Both GPUs passed:',len(results)==2 and all(r['passed'] for r in results))
print('No benchmark or larger experiment launched. Original failed study retained.')
