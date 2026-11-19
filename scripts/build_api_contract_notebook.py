"""Build the new API-mechanism development diagnostic, not the failed count gate."""
import json
from pathlib import Path
import subprocess
import sys

BASE=Path(__file__).resolve().parents[1]
# Both builders preserve explicit hashes for source and prior initialization.
subprocess.run([sys.executable,str(BASE/'scripts/build_paired_notebook.py')],cwd=BASE,check=True)
subprocess.run([sys.executable,str(BASE/'scripts/build_fresh_compact_notebook.py')],cwd=BASE,check=True)
notebook=json.loads((BASE/'notebooks/kaggle_14b_fresh_compact.ipynb').read_text())
notebook['cells'][0]['source']='''# API contract mechanism: paired development diagnostic
Enable Internet and T4 x2. This tests five development targets using ten real
14B generations, one generation/target/arm, no repairs or pruning. Both arms
use the same concise-file instruction, seed, budgets and pytest/coverage gates.
Only the API-contract arm receives static descriptor/lexical-ownership facts.
There is no exact-one-test-function restriction; complete multiple-test files
are allowed in both arms.

The generation inputs are fixed initial prompts from a previous real upstream
run. This is a mechanism diagnostic, not a new full upstream run or a held-out
confirmation. The separately locked held-out frame contains twelve targets in
four projects, seeds42/43/44 (72 arm trials); this notebook does not automatically
launch that larger phase. Source review and independent-project evidence remain
required before making quality/superiority claims.

On a fresh session the notebook prepares isolated environments and new GPU
calibration. Audited initialization evidence is embedded and never used as
generated-test/outcome cache. The final cell waits and saves the raw ZIP.
'''.splitlines(keepends=True)
source=''.join(notebook['cells'][1]['source']).replace("('UPSTREAM_NF4_FRESH_COMPACT_'+STAMP)","('API_CONTRACT_DEV_'+STAMP)")
notebook['cells'][1]['source']=source.splitlines(keepends=True)
run=''.join(notebook['cells'][3]['source'])
run=run.replace('[sys.executable,str(driver),str(WORKDIR),str(ROOT)],',
    "[sys.executable,str(driver),str(WORKDIR),str(ROOT),'--mechanism','api-contract-v1','--action','probe'],")
run=run.replace("if (ROOT/'small-report.md').exists():display(Markdown((ROOT/'small-report.md').read_text()))",
    "if (ROOT/'diagnostic/summary.json').exists():print(json.loads((ROOT/'diagnostic/summary.json').read_text()))")
run=run.replace("'STEP','FINAL','[progress:','[stress','Project ','Reports:',", "'STEP','FINAL','PROBE_RESULT','[progress:','[stress','Project ','Reports:',")
notebook['cells'][3]['source']=run.splitlines(keepends=True)
for index,cell in enumerate(notebook['cells']):
    if cell['cell_type']=='code':
        try:compile(''.join(cell['source']),f'api-cell-{index}','exec')
        except SyntaxError as exc:raise ValueError(f'Notebook syntax at cell {index}, line {exc.lineno}: {exc.msg}') from None
path=BASE/'notebooks/kaggle_api_contract_probe.ipynb'
path.write_text(json.dumps(notebook,indent=2)+'\n')
print(path,'bytes',path.stat().st_size)
