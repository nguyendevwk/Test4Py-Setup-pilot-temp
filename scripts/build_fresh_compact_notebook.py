"""Package a fresh-session two-module screen with audited real initialization."""
import argparse
import base64
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SHA = '603266e8f6360ae0fc86d93d2bed7edc131db23a81448017a80202518d566b3a'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--initialization-archive', type=Path, default=BASE/
    'kaggle-output/remote-20261117/UPSTREAM_NF4_RESUME_20261116T174754946339Z.zip')
args = parser.parse_args()
evidence = args.initialization_archive.read_bytes()
if hashlib.sha256(evidence).hexdigest() != SHA:
    raise ValueError('Expected the audited real initialization archive; no substituted evidence')
standard = json.loads((BASE/'notebooks/kaggle_upstream_nf4_paired.ipynb').read_text())
driver = (BASE/'scripts/kaggle_fresh_compact.py').read_text()
cells = []

def cell(kind, text):
    item = dict(cell_type=kind, id=f'fresh-{len(cells)}', metadata={}, source=text.splitlines(keepends=True))
    if kind == 'code':
        try:
            compile(text, item['id'], 'exec')
        except SyntaxError as exc:
            raise ValueError(f"{item['id']} syntax at line {exc.lineno}: {exc.msg}") from None
        item.update(execution_count=None, outputs=[])
    cells.append(item)

cell('markdown', '''# Historical development screen: single-test-v1
**Not the recommended application workflow.** The real screen was stopped
after repeated rejection of complete multi-test outputs by the one-test rule.
It did not establish an efficacy result. The reviewed working application
subset is documented in `research/application/14b_genty_curated_20261117/README.md`.
This notebook is retained to reproduce the experimental configuration.

Enable Internet and T4 x2. This runs only two genty modules, both arms, seed42,
one round (four module trials). It never launches the larger pilot.

The notebook ships the source snapshot and audited real greedy initialization
evidence. It prepares new environments, pins the original real model revisions,
checks production/model/runtime identity before initialization-only reuse, and
requires **fresh GPU calibration**. Generated tests/repairs/outcomes are never
imported for scoring. Earlier cold costs remain separate. Old summaries can be
wrong or truncated; reusing them does not verify their semantics.

Both arms use the shared single-test-v1 output contract. This is an adapted
upstream baseline, not identical raw upstream prompting. A 60-minute shared
stress+small deadline includes weights/embedding downloads and model loads;
CPU bootstrap/preparation is separate. All failures and missing values remain.
This last cell waits for completion so Run All/Save Version can retain outputs.
''')
source = ''.join(standard['cells'][1]['source']).replace(
    "('UPSTREAM_NF4_'+STAMP)", "('UPSTREAM_NF4_FRESH_COMPACT_'+STAMP)")
cell('code', source)
cell('code', '''# Immutable initialization evidence and an explicitly hashed launcher.
archive=Path('/kaggle/working/PRIOR_14B_INITIALIZATION_EVIDENCE.zip')
data=base64.b64decode(__INIT_PAYLOAD__)
assert hashlib.sha256(data).hexdigest()==__INIT_SHA__
if archive.exists():
    assert archive.read_bytes()==data, 'Different previous evidence exists; preserve it.'
else:
    archive.write_bytes(data)
driver=WORKDIR/'scripts/kaggle_fresh_compact.py'
driver.write_text(__DRIVER_TEXT__)
PROVENANCE.update(fresh_driver_sha256=hashlib.sha256(driver.read_bytes()).hexdigest(),
                  initialization_archive_sha256=__INIT_SHA__)
(WORKDIR/'notebook-source.json').write_text(json.dumps(PROVENANCE,indent=2))
BOOTLOG=Path('/kaggle/working')/('FRESH_COMPACT_'+ROOT.name+'.log')
print('Fresh study:',ROOT)
'''.replace('__INIT_SHA__', repr(SHA)).replace('__INIT_PAYLOAD__', repr(base64.b64encode(evidence).decode()))
       .replace('__DRIVER_TEXT__', repr(driver)))
cell('code', '''# Blocking, bounded job; no detached Run-All output loss.
with BOOTLOG.open('x') as log:
    proc=subprocess.Popen([sys.executable,str(driver),str(WORKDIR),str(ROOT)],
        cwd=WORKDIR,env=dict(os.environ,PYTHONUNBUFFERED='1'),stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,text=True,bufsize=1)
    for line in proc.stdout:
        log.write(line);log.flush()
        if line.startswith(('STEP','FINAL','[progress:','[stress','Project ','Reports:',
                            'Verified','DRIVER ERROR')):
            print(line,end='',flush=True)
    code=proc.wait()
status=json.loads(Path('/kaggle/working/TEST4PY_FRESH_STATUS.json').read_text())
print('Execution status:',status['status'])
from IPython.display import display,FileLink,Markdown
if (ROOT/'small-report.md').exists():display(Markdown((ROOT/'small-report.md').read_text()))
if Path(str(ROOT)+'.zip').exists():display(FileLink(str(ROOT)+'.zip'))
assert code==0 and status['status']=='completed', 'Failed step; inspect preserved log/archive.'
print('Review tests, assertion edits, coverage/fault evidence and costs. Larger pilot not launched.')
''')
path = BASE/'notebooks/kaggle_14b_fresh_compact.ipynb'
path.write_text(json.dumps(dict(nbformat=4, nbformat_minor=5, metadata=standard['metadata'], cells=cells), indent=2)+'\n')
print(path, 'bytes', path.stat().st_size)
