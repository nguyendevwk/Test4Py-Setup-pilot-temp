import base64
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

base = Path(__file__).resolve().parents[1]
revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=base, text=True).strip()
paths = ['council_multitarget.py', 'council/generator.py', 'pilot/multitarget.py', 'pilot/grounding.py', 'pilot/api_contract.py', 'pilot/source_prompt.py', 'tests/test_multitarget.py', 'notebooks/kaggle_multitarget_smoke_v4.ipynb']
hashes = {name: hashlib.sha256((base/name).read_bytes()).hexdigest() for name in paths}
buffer = io.BytesIO()
with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
    for name in paths:
        archive.writestr(name, (base/name).read_bytes())
payload = base64.b64encode(buffer.getvalue()).decode()
notebook = json.loads((base/'notebooks/kaggle_multitarget_smoke_v4.ipynb').read_text())
notebook['cells'][0]['source'] = '''# Test4Py Council — Git clone + engineering screen v4
Upload this notebook to Kaggle, enable **Internet** and **GPU T4 x2**, then Run All.
No source ZIP or API key is required for these public model/repository downloads.

This notebook clones a pinned base commit and applies an **embedded, SHA-256-checked
source overlay** containing the local runner fixes, helper and regression tests.
The overlay has not been pushed to GitHub. Both base commit and overlay hashes are
saved; this is a new development cohort, not an unchanged upstream checkout.

Fixed plan: 2 targets × 4 arms × 1 attempt = **8 planned outcomes**. No pruning,
no automatic full run, no claim of improvement over the paper. Failed outcomes
and raw evidence remain in the output ZIP. Runtime depends on model download and
inference; no fixed completion time is promised.
'''.splitlines(keepends=True)
setup = '''from pathlib import Path
from datetime import datetime, timezone
import base64, hashlib, io, json, os, subprocess, sys, zipfile

REPO_URL = 'https://github.com/nguyendevwk/Test4Py-Setup-pilot-temp.git'
BASE_COMMIT = BASE_REVISION
STAMP = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
WORKDIR = Path('/kaggle/working') / ('Test4Py_screen_' + STAMP)
PREP = Path('/kaggle/working') / ('SCREEN_PREFLIGHT_' + STAMP)
OUTPUT = Path('/kaggle/working') / ('SCREEN_V4_' + STAMP)
subprocess.run(['git', 'clone', '--depth', '1', REPO_URL, str(WORKDIR)], check=True)
actual = subprocess.check_output(['git', '-C', str(WORKDIR), 'rev-parse', 'HEAD'], text=True).strip()
if actual != BASE_COMMIT:
    subprocess.run(['git', '-C', str(WORKDIR), 'fetch', '--depth', '1', 'origin', BASE_COMMIT], check=True)
    subprocess.run(['git', '-C', str(WORKDIR), 'checkout', '--detach', 'FETCH_HEAD'], check=True)
assert subprocess.check_output(['git', '-C', str(WORKDIR), 'rev-parse', 'HEAD'], text=True).strip() == BASE_COMMIT

# Transparent source snapshot, not model outputs or research measurements.
OVERLAY_SHA256 = OVERLAY_HASHES
OVERLAY_ZIP_B64 = OVERLAY_PAYLOAD
with zipfile.ZipFile(io.BytesIO(base64.b64decode(OVERLAY_ZIP_B64))) as archive:
    assert set(archive.namelist()) == set(OVERLAY_SHA256)
    for name, expected in OVERLAY_SHA256.items():
        data = archive.read(name)
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError('Overlay integrity error: ' + name)
        destination = WORKDIR / name
        if not destination.resolve().is_relative_to(WORKDIR.resolve()):
            raise ValueError('Unsafe overlay path')
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
provenance = dict(repository=REPO_URL, base_commit=BASE_COMMIT,
                  source_kind='pinned Git base plus embedded local v4 overlay',
                  overlay_sha256=OVERLAY_SHA256)
(WORKDIR/'notebook-source.json').write_text(json.dumps(provenance, indent=2))
os.chdir(WORKDIR)
print(json.dumps(provenance, indent=2))
print('Source:', WORKDIR, 'Output:', OUTPUT)
'''.replace('BASE_REVISION', repr(revision)).replace('OVERLAY_HASHES', repr(hashes)).replace('OVERLAY_PAYLOAD', repr(payload))
notebook['cells'][1]['source'] = setup.splitlines(keepends=True)
# Preserve source provenance and run log outside result path, including early failure.
for cell in notebook['cells']:
    if cell['cell_type'] != 'code':
        continue
    source = ''.join(cell['source'])
    if 'run = subprocess.run(cmd, cwd=WORKDIR)' in source:
        source = source.replace('run = subprocess.run(cmd, cwd=WORKDIR)', '''# Tee bounded progress to notebook and preserve the complete launcher log.
launcher_log = Path('/kaggle/working') / ('SCREEN_LAUNCHER_' + STAMP + '.log')
with launcher_log.open('w') as stream:
    proc = subprocess.Popen(cmd, cwd=WORKDIR, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, bufsize=1)
    try:
        for line in proc.stdout:
            stream.write(line)
            stream.flush()
            print(line, end='', flush=True)
        returncode = proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        raise
run = subprocess.CompletedProcess(cmd, returncode)
if OUTPUT.exists():
    import shutil
    shutil.copy2(WORKDIR/'notebook-source.json', OUTPUT/'notebook-source.json')
    shutil.copy2(launcher_log, OUTPUT/'launcher.log')
    shutil.make_archive(str(OUTPUT), 'zip', OUTPUT)''')
    cell['source'] = source.splitlines(keepends=True)
# Stable IDs are required by the notebook 4.5 schema.
for i, cell in enumerate(notebook['cells']):
    cell['id'] = f'council-git-screen-{i:02d}'
    if cell['cell_type'] == 'code':
        compile(''.join(cell['source']), f'cell-{i}', 'exec')
notebook['metadata'].update(kaggle=dict(isInternetEnabled=True),
                            test4py_source=dict(base_commit=revision, overlay_sha256=hashes))
out = base/'notebooks/kaggle_git_clone_smoke_v4.ipynb'
out.write_text(json.dumps(notebook, indent=2)+'\n')
# Decode the exact shipped overlay and validate every member.
source = ''.join(notebook['cells'][1]['source'])
import ast
values = {}
for node in ast.parse(source).body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
        if node.targets[0].id in ('OVERLAY_SHA256', 'OVERLAY_ZIP_B64'):
            values[node.targets[0].id] = ast.literal_eval(node.value)
with zipfile.ZipFile(io.BytesIO(base64.b64decode(values['OVERLAY_ZIP_B64']))) as archive:
    for name, expected in values['OVERLAY_SHA256'].items():
        assert archive.read(name) == (base/name).read_bytes()
        assert hashlib.sha256(archive.read(name)).hexdigest() == expected
print(out)
print('Base:', revision)
print('Overlay verified; all notebook cells compile; bytes:', out.stat().st_size)
