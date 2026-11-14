"""Create real pilot data, analyze it, and bundle artifacts; no existing input required."""
import argparse
import os
from pathlib import Path
import sys
import zipfile

from pilot.common import BASE, command, reserve_output, write_json
from pilot.console import Console


def bundle_artifacts(root, exclude=()):
    """Keep measurements and generated tests, excluding rebuildable code/model caches."""
    destination = root / 'results.zip'
    with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for current, directories, files in os.walk(root):
            current = Path(current)
            directories[:] = sorted(name for name in directories if name not in
                {'.git','__pycache__','upstream','mutants','node_modules'} and not name.startswith('.venv'))
            if current.name == 'PyCG':
                directories[:] = [name for name in directories if name == 'Test4DT_tests']
                files = [name for name in files if name == 'pytest_report.json']
            for name in sorted(files):
                path = current / name
                if path == destination or str(path.relative_to(root)) in exclude or path.suffix in {'.tmp','.zip','.pyc','.safetensors','.bin'}:
                    continue
                archive.write(path, str(Path('test4py-results') / path.relative_to(root)))
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('/kaggle/working/test4py-research'))
    parser.add_argument('--runtime', choices=('modern','legacy'), default='modern')
    parser.add_argument('--jobs', type=int, default=2)
    parser.add_argument('--gpus', default='auto')
    parser.add_argument('--rounds', type=int, default=1)
    parser.add_argument('--model', default='Qwen/Qwen3-4B-Instruct-2507')
    parser.add_argument('--venv', type=Path)
    parser.add_argument('--console', choices=('compact','quiet','full'), default='compact')
    args = parser.parse_args()
    if min(args.jobs,args.rounds) < 1:
        parser.error('jobs and rounds must be positive')
    root = reserve_output(args.output)
    venv = args.venv or Path('/tmp/test4py-modern' if args.runtime=='modern' else '/tmp/test4py-venv')
    python = venv / 'bin/python'
    import json
    write_json(root/'input-specification.json', json.loads((BASE/'research/pilot-data.json').read_text()))
    steps = [
        ('experiment', [sys.executable, '-u', BASE/'kaggle_run.py', '--runtime', args.runtime,
            '--jobs', str(args.jobs), '--gpus', args.gpus, '--rounds', str(args.rounds), '--model', args.model,
            '--venv', venv, '--console', 'full', '--output', root/'experiment'], 70000),
        ('report_dependencies', [python, '-m', 'pip', 'install', '--disable-pip-version-check',
            '-r', BASE/'requirements-analysis.txt'], 1200),
        ('analysis', [python, BASE/'analyze.py', '--input', root/'experiment/comparison',
            '--output', root/'report', '--plots'], 1800),
    ]
    state = dict(status='running',output=str(root),current_step='starting',steps_completed=0,
                 steps_total=4,steps=[],input_kind='real_execution',quality_claim='no_superiority_claim')
    write_json(root/'research-run.json',state)
    console = Console(args.console)
    print(f'Creating real experiment data. Output: {root}',flush=True)
    failure = False
    try:
        for name,cmd,timeout in steps:
            state['current_step'] = name
            write_json(root/'research-run.json',state)
            print(f'[{name}] starting; log: {root / (name+".log")}',flush=True)
            try:
                result = command(cmd,cwd=BASE,timeout=timeout,log_path=root/(name+'.log'),
                                 stream=True,label=name,console=console)
            except OSError as exc:
                result = dict(returncode=-1,timeout=False,stdout='',stderr=str(exc))
            write_json(root/(name+'-process.json'),result)
            state['steps'].append(dict(name=name,returncode=result['returncode'],timeout=result['timeout']))
            state['steps_completed'] += 1
            if result['returncode'] != 0 or result['timeout']:
                failure = True
                state.update(status='failed',failed_step=name)
                data = root/'experiment/comparison'
                has_arm_artifacts = any((data/mode/'report.json').exists() for mode in
                                        ('baseline','caller','extracted','verified'))
                if name == 'experiment' and has_arm_artifacts:
                    state['status'] = 'running_with_failures'
                    print('Experiment has failed arms; analyzing the real partial artifacts with failures retained.',flush=True)
                    continue
                print(f'Stopped at {name}; results are not fabricated. Inspect {root/(name+".log")}',flush=True)
                break
    except BaseException as exc:
        failure = True
        state.update(status='failed',error=repr(exc))
        raise
    finally:
        state['current_step'] = 'archive'
        write_json(root/'research-run.json',state)
        # Even failed runs retain a downloadable bundle with the actual failure evidence.
        bundle = bundle_artifacts(root, exclude=('research-run.json',))
        state['steps_completed'] += 1
        state.update(status='failed' if failure else 'complete',current_step='finished',bundle=str(bundle))
        write_json(root/'research-run.json',state)
        # Append final status once, after packing, without a stale duplicate entry.
        with zipfile.ZipFile(bundle,'a',compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(root/'research-run.json','test4py-results/research-run.json')
    print(f'Artifacts: {root}\nBundle: {bundle}',flush=True)
    if (root/'report/report.md').exists():
        print(f'Report: {root/"report/report.md"}',flush=True)
    return 1 if failure else 0


if __name__=='__main__':
    raise SystemExit(main())
