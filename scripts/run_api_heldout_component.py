"""Explicit bounded held-out component run; not the full upstream/paper campaign."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
from pilot.common import reserve_output,write_json
from paired_study import make_bundle
from scripts.prepare_api_contract_heldout import prepare


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study',type=Path,required=True,help='Same-session calibrated 14B study')
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--uv',required=True)
    parser.add_argument('--resolved',type=Path,default=BASE/'research/artifacts/api_contract_heldout_preflight_20261117.json')
    args=parser.parse_args()
    root=reserve_output(args.output)
    frame_path=BASE/'research/benchmark/api_contract_heldout_frame.json'
    manifest_path=BASE/'research/benchmark/api_source_heldout_component_v2.json'
    frame=json.loads(frame_path.read_text());manifest=json.loads(manifest_path.read_text())
    if hashlib.sha256(frame_path.read_bytes()).hexdigest()!=manifest['source_frame_sha256']:
        raise ValueError('Held-out selection frame changed')
    expected={(t['id'],seed) for t in frame['targets'] for seed in frame['seeds']}
    observed={(t['target_id'],t['seed']) for t in manifest['targets']}
    if expected!=observed or len(manifest['targets'])!=len(expected) or manifest['planned_arm_trials']!=len(expected)*len(manifest['arms']):
        raise ValueError('Held-out planned denominator changed')
    write_json(root/'locked-manifest.json',manifest)
    write_json(root/'source-freeze.json',{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in BASE.rglob('*.py') if not any(x in p.relative_to(BASE).parts for x in ('.git','venv','.venv','__pycache__'))})
    started=time.time()
    state=dict(status='running',root=str(root),source=str(BASE),phase='heldout-import-preparation',started_epoch=started,
               scope='72 fixed component trials; source-only vs source+facts; no original-paper/full-pipeline claim')
    def save(**changes):
        state.update(changes,updated_epoch=time.time());write_json(root/'remote-execution.json',state)
        print('HELDOUT_STATUS',state['status'],state['phase'],flush=True)
    try:
        save()
        ready=prepare(frame,root/'prepared-environments',args.uv,json.loads(args.resolved.read_text()))
        if not ready:
            planned=[dict(id=t['id'],project=t['project'],module=t['module'],seed=t['seed'],arm=arm,
                          status='preparation_failed',first_pass=None,meaningful_target_test=None)
                     for t in manifest['targets'] for arm in manifest['arms']]
            write_json(root/'diagnostic/summary.json',dict(planned=len(planned),rows=planned,full_pipeline_efficacy=False,
                source_review_required=True,note='No model inference launched because the locked import preflight was not ready.'))
            save(status='failed',phase='heldout-import-preparation',model_inference_run=False)
            return 2
        save(phase='heldout-component-inference',model_inference_run=True)
        result=subprocess.run([sys.executable,str(BASE/'scripts/api_contract_probe.py'),'--study',str(args.study),
            '--manifest',str(manifest_path),'--output',str(root/'diagnostic'),
            '--prepared',str(root/'prepared-environments/preflight.json')],cwd=BASE,check=False)
        save(status='completed' if result.returncode==0 else 'failed',phase='finished',returncode=result.returncode)
        return result.returncode
    except Exception as exc:
        save(status='failed',error=repr(exc))
        raise
    finally:
        save(ended_epoch=time.time(),seconds=time.time()-started)
        make_bundle(root)


if __name__=='__main__':sys.exit(main())
