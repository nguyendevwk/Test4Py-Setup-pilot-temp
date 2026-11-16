"""Package the current experiment source into one Git-clone Kaggle notebook."""
import base64
import hashlib
import io
import json
from pathlib import Path
import zipfile

BASE=Path(__file__).resolve().parents[1]
import subprocess
BASE_COMMIT=subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip()
patterns=['*.py','pilot/*.py','council/*.py','tests/test*.py','requirements*.txt','pytest.ini','pilot.json',
          'research/benchmark/*.json','notebooks/kaggle_multitarget_smoke_v4.ipynb','scripts/check_upstream_fixture.py','scripts/check_upstream_initialization.py']
files=sorted({p for pattern in patterns for p in BASE.glob(pattern) if p.is_file()})
hashes={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
buffer=io.BytesIO()
with zipfile.ZipFile(buffer,'w',zipfile.ZIP_DEFLATED) as archive:
    for p in files:archive.write(p,str(p.relative_to(BASE)))
payload=base64.b64encode(buffer.getvalue()).decode()
cells=[]
def cell(kind,text):
    entry=dict(cell_type=kind,id=f'paired-{len(cells):02d}',metadata={},source=text.splitlines(keepends=True))
    if kind=='code':entry.update(execution_count=None,outputs=[]);compile(text,entry['id'],'exec')
    cells.append(entry)
cell('markdown','''# Upstream Test4Py × Qwen Coder 14B NF4 — gated paired pilot
Enable **Internet** and **T4 x2**. Upload this notebook and Run All.

Both baseline and improved run pinned upstream call graph, summaries, type inference,
RAG, test generation and adaptive repair using the SAME 14B NF4 model. No 4B Critic.
Greedy initialization has an exact-prompt shared cache; sampled seeds vary generation/repair.
Compare generation costs separately from cache-dependent initialization costs.
Shared runtime adapters: CPU embedding, deterministic complete-block extraction and
empty-candidate retrieval handling. Improved adds verified type context/imports and
assertion-preserving acceptance. This is a small adapted reproduction, not the paper's
GPT-4o result or a held-out generalization study.

Order: source tests → prepare → CPU fixture through real upstream → forced-decode
VRAM stress on each GPU → small A/B run. It stops after small for artifact review.
Larger run is an explicit optional cell and refuses incomplete small/stress evidence.
Runtime is measured, not promised. All failed outcomes are retained.
''')
cell('code','''from pathlib import Path
from datetime import datetime, timezone
import base64, hashlib, io, json, os, shutil, subprocess, sys, zipfile
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
WORKDIR=Path('/kaggle/working')/('Test4Py_upstream_'+STAMP)
ROOT=Path('/kaggle/working')/('UPSTREAM_NF4_'+STAMP)
subprocess.run(['git','clone','--depth','1','https://github.com/nguyendevwk/Test4Py-Setup-pilot-temp.git',str(WORKDIR)],check=True)
BASE_COMMIT=BASE_SHA
if subprocess.check_output(['git','-C',str(WORKDIR),'rev-parse','HEAD'],text=True).strip()!=BASE_COMMIT:
    subprocess.run(['git','-C',str(WORKDIR),'fetch','--depth','1','origin',BASE_COMMIT],check=True)
    subprocess.run(['git','-C',str(WORKDIR),'checkout','--detach','FETCH_HEAD'],check=True)
assert subprocess.check_output(['git','-C',str(WORKDIR),'rev-parse','HEAD'],text=True).strip()==BASE_COMMIT
HASHES=SOURCE_HASHES
PAYLOAD=SOURCE_PAYLOAD
with zipfile.ZipFile(io.BytesIO(base64.b64decode(PAYLOAD))) as archive:
    assert set(archive.namelist())==set(HASHES)
    for name,expected in HASHES.items():
        data=archive.read(name)
        assert hashlib.sha256(data).hexdigest()==expected,name
        path=(WORKDIR/name).resolve()
        assert path.is_relative_to(WORKDIR.resolve())
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
os.chdir(WORKDIR)
sys.path.insert(0,str(WORKDIR))
PROVENANCE=dict(base_commit=BASE_COMMIT,overlay_sha256=HASHES,source_kind='Git base plus embedded local changes; not claimed pushed')
print('Source:',WORKDIR,'Study:',ROOT)
'''.replace('BASE_SHA',repr(BASE_COMMIT)).replace('SOURCE_HASHES',repr(hashes)).replace('SOURCE_PAYLOAD',repr(payload)))
cell('code','''# Hardware detection precedes downloads. GPU count alone does not prove context fit.
import torch
assert torch.cuda.is_available() and torch.cuda.device_count()==2, 'Enable T4 x2 in Kaggle Settings'
print([(torch.cuda.get_device_name(i), round(torch.cuda.get_device_properties(i).total_memory/1024**3,2)) for i in range(2)])
subprocess.run([sys.executable,'-m','pip','install','uv==0.6.17'],check=True)
subprocess.run([sys.executable,'bootstrap_modern.py'],check=True,cwd=WORKDIR)
PYTHON='/tmp/test4py-modern/bin/python'
subprocess.run([PYTHON,'-m','pip','install','-r','requirements-paired.txt'],check=True,cwd=WORKDIR)
LOG=Path('/kaggle/working')/('UPSTREAM_LAUNCHER_'+STAMP+'.log')
def run_step(arguments, env=None):
    with LOG.open('a') as log:
        proc=subprocess.Popen([PYTHON,*arguments],cwd=WORKDIR,env=env,stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,text=True,bufsize=1)
        for line in proc.stdout:
            print(line,end='',flush=True);log.write(line);log.flush()
        code=proc.wait()
    if ROOT.exists():
        shutil.copy2(LOG,ROOT/'notebook-launcher.log')
    if code:
        if ROOT.exists():
            from paired_study import make_bundle
            bundle=make_bundle(ROOT)
            from IPython.display import display,FileLink
            display(FileLink(str(bundle)))
        raise RuntimeError(f'Step exited {code}; retained artifacts at {ROOT}. Do not proceed to larger run.')
''')
cell('code','''# Offline code checks: hide GPUs to prevent accidental model inference in tests.
run_step(['-m','unittest','discover','-s','tests','-v'], env=dict(os.environ,CUDA_VISIBLE_DEVICES=''))
# Freeze budgets BEFORE inference. If stress later fails, use a new plan/output;
# never lower budgets for only one arm or silently retry another model.
run_step(['paired_study.py','--action','plan','--output',str(ROOT),
          '--max-input-tokens','4096','--max-new-tokens','512'])
(ROOT/'notebook-source.json').write_text(json.dumps(PROVENANCE,indent=2))
run_step(['paired_study.py','--action','prepare','--output',str(ROOT)])
''')
cell('code','''# Engineering fixtures: real upstream orchestration, SCRIPTED model/embedding.
# Their coverage/mutation numbers are not benchmark measurements.
preflight=json.loads((ROOT/'preflight.json').read_text())
for name,item in preflight.items():
    run_step(['scripts/check_upstream_initialization.py','--upstream',str(ROOT/'upstream'),
              '--source',item['import_root'],'--source-path',item['source_path'],
              '--output',str(ROOT/'engineering_fixture'/('init-'+name))],
             env=dict(os.environ,CUDA_VISIBLE_DEVICES=''))
for arm in ['baseline','improved']:
    run_step(['scripts/check_upstream_fixture.py','--upstream',str(ROOT/'upstream'),
              '--output',str(ROOT/'engineering_fixture'/arm),'--arm',arm],
             env=dict(os.environ,CUDA_VISIBLE_DEVICES=''))
''')
cell('code','''# Synthetic prefill + FORCED full-length decode at 2K/4K + 512 output.
# Repeat the largest case, require 1.5 GiB conservative memory headroom per GPU.
# This tests more than model loading; real upstream prompts remain budget-checked.
run_step(['paired_study.py','--action','stress','--output',str(ROOT),'--jobs','2'])
''')
cell('code','''# Small: genty.genty_repeat, one seed, one round, both arms; full package analyzed.
run_step(['paired_study.py','--action','small','--output',str(ROOT),'--jobs','2'])
from IPython.display import display,Markdown,FileLink
summary=json.loads((ROOT/'small-summary.json').read_text())
display(Markdown((ROOT/'small-report.md').read_text()))
print('Execution ready:',summary['execution_ready'],'Semantic review required:',summary['semantic_review_required'])
from paired_study import make_bundle
shutil.copy2(LOG,ROOT/'notebook-launcher.log')
display(FileLink(str(make_bundle(ROOT))))
print('Review raw tests, generation errors, resource budgets and locked fault pools before a larger run.')
''')
cell('markdown','''## Optional larger paired pilot — not started by Run All
The locked larger plan has 3 modules in 2 projects (genty repeat/args and woa
whale_optimization), 2 seeds, 3 rounds, 2 arms: **12 module trials**. It is a
purpose-selected pilot, not representative of the 183-module paper benchmark.
The small module is development data. No significance/generalization claim.
Baseline failures are valid outcomes; engineering readiness is not all-suite pass.
Set the flag in the following cell only after reviewing the small archive.
''')
cell('code','''RUN_LARGER=True
if RUN_LARGER:
    small=json.loads((ROOT/'small-summary.json').read_text())
    assert small['execution_ready'], 'Small worker/hardware check incomplete'
    run_step(['paired_study.py','--action','run','--output',str(ROOT),'--jobs','2'])
    display(Markdown((ROOT/'main-report.md').read_text()))
    display(FileLink(str(make_bundle(ROOT))))
else:
    print('Larger run not launched. Small-run archive:',str(ROOT)+'.zip')
''')
notebook=dict(cells=cells,metadata=dict(language_info=dict(name='python'),accelerator='GPU',
                  kaggle=dict(isInternetEnabled=True),test4py_source=dict(base_commit=BASE_COMMIT,overlay_sha256=hashes)),nbformat=4,nbformat_minor=5)
out=BASE/'notebooks/kaggle_upstream_nf4_paired.ipynb';out.write_text(json.dumps(notebook,indent=2)+'\n')
with zipfile.ZipFile(io.BytesIO(base64.b64decode(payload))) as archive:
    for name,expected in hashes.items():
        assert hashlib.sha256(archive.read(name)).hexdigest()==expected
print(out, 'bytes=',out.stat().st_size,'files=',len(hashes))
