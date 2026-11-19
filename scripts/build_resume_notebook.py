"""Reuse the shipped source overlay but skip already validated Kaggle stages."""
import ast
import argparse
import json
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--reuse-initialization')
parser.add_argument('--test-output-contract',choices=['single-test-v1'])
args=parser.parse_args()
standard=json.loads((BASE/'notebooks/kaggle_upstream_nf4_paired.ipynb').read_text())
source=''.join(standard['cells'][1]['source'])
clone="subprocess.run(['git','clone','--depth','1','https://github.com/nguyendevwk/Test4Py-Setup-pilot-temp.git',str(WORKDIR)],check=True)"
assert clone in source
source=source.replace(clone,"""OLD_SOURCE=Path('/kaggle/working/Test4Py_upstream_20261116T170358791891Z')
assert OLD_SOURCE.is_dir(), 'Copy these cells into the existing Kaggle session; no reinstall is needed.'
subprocess.run(['git','clone','--no-hardlinks',str(OLD_SOURCE),str(WORKDIR)],check=True)""")
source=source.replace("('UPSTREAM_NF4_'+STAMP)","('UPSTREAM_NF4_RESUME_'+STAMP)")
if args.reuse_initialization:source=source.replace("('UPSTREAM_NF4_RESUME_'+STAMP)","('UPSTREAM_NF4_RETRY_'+STAMP)")
hardware=''.join(standard['cells'][2]['source'])
fn=next(n for n in ast.parse(hardware).body if isinstance(n,ast.FunctionDef) and n.name=='run_step')
runner=ast.get_source_segment(hardware,fn)
setup="""# Reuse successful preparation and calibrated memory; no installs/unit/CPU fixtures.
PYTHON='/tmp/test4py-modern/bin/python'
assert Path(PYTHON).is_file(), 'Prepared interpreter missing; use the same Kaggle session.'
LOG=Path('/kaggle/working')/('UPSTREAM_RESUME_'+STAMP+'.log')
FAILED_STEP=None
"""+runner+"""
run_step(['paired_study.py','--action','plan','--output',str(ROOT),
          '--max-input-tokens','4096','--max-new-tokens','512'])
(ROOT/'notebook-source.json').write_text(json.dumps(PROVENANCE,indent=2))
run_step(['resume_paired.py','--previous','/kaggle/working/UPSTREAM_NF4_20261116T170358791891Z',
          '--diagnostic','/kaggle/working/NF4_14B_OOM_CHECK_20261116T172805400121Z',
          '--output',str(ROOT)])
"""
if args.reuse_initialization:
    needle="'--output',str(ROOT)])\n"
    # Add only to resume_paired, not the plan command above.
    position=setup.rfind(needle)
    assert position>=0
    setup=setup[:position]+"'--initialization-from',"+repr(args.reuse_initialization)+",\n          "+setup[position:]
if args.test_output_contract:
    assert args.reuse_initialization, 'Compact retry must retain the initialization-reuse provenance'
    source=source.replace("('UPSTREAM_NF4_RETRY_'+STAMP)","('UPSTREAM_NF4_COMPACT_'+STAMP)")
    setup=setup.replace("'--max-input-tokens','4096','--max-new-tokens','512'])",
                        "'--max-input-tokens','4096','--max-new-tokens','512',\n          '--test-output-contract','single-test-v1'])")
small="""# REAL 14B inference. Two genty modules x baseline/improved, seed 42, one round.
# 60 minutes includes the embedding download and model loads. All outcomes retained.
run_step(['paired_study.py','--action','small','--output',str(ROOT),'--jobs','2'])
from IPython.display import display,FileLink,Markdown
display(Markdown((ROOT/'small-report.md').read_text()))
print(json.loads((ROOT/'small-measurement-summary.json').read_text()))
display(FileLink(str(ROOT)+'.zip'))
print('Larger experiment NOT launched. Send this archive for review.')
"""
texts=[('markdown',"""# Resume small A/B — Qwen 14B NF4
Copy these three Code cells **in order into the existing Kaggle session**.
This creates a fresh source snapshot and result directory. No pip, unit tests,
CPU fixtures, model substitution, or repeated GPU stress.
Previously successful source/environment preparation and the real 4K+512 GPU
diagnostic are validated before reuse. Their original files remain unchanged.
Calibration reuse is recorded explicitly and does not approve generator quality.
Two genty modules, one seed, one round, both arms: 4 module trials.
Real upstream initialization still runs; no scripted model outputs or oracle copying.
The 60-minute budget can expire with failures; that is retained as evidence.
This notebook stops after small; it never launches the larger experiment.
"""),('code',source),('code',setup),('code',small)]
cells=[]
for i,(kind,text) in enumerate(texts):
    item=dict(cell_type=kind,id=f'resume-{i}',metadata={},source=text.splitlines(keepends=True))
    if kind=='code':compile(text,f'cell-{i}','exec');item.update(execution_count=None,outputs=[])
    cells.append(item)
out=BASE/'notebooks/kaggle_14b_small_resume.ipynb'
if args.reuse_initialization:
    cells[0]['source']+=['\nWarm-prefix engineering retry: exact greedy initialization outputs are verified and imported.\n',
                         'Earlier timeout and cold initialization cost remain evidence. No generated tests or scoring outcomes are reused.\n']
    out=BASE/'notebooks/kaggle_14b_small_retry.ipynb'
if args.test_output_contract:
    cells[0]['source'] += ['\nNew development cohort: shared single-test-v1 output contract for both arms.\n',
                            'Initialization unchanged; all test generation and scoring are fresh.\n']
    out=BASE/'notebooks/kaggle_14b_compact_retry.ipynb'
out.write_text(json.dumps(dict(nbformat=4,nbformat_minor=5,metadata=standard['metadata'],cells=cells),indent=2)+'\n')
print(out)
