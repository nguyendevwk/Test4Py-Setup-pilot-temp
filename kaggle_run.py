"""Kaggle entrypoint: bootstrap -> validate -> compare, stopping on any failure."""
import argparse
from pathlib import Path
import shutil
import sys

from pilot.common import BASE, command, reserve_output, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('/kaggle/working/test4py-pilot'))
    parser.add_argument('--runtime', choices=('modern', 'legacy'), default='modern')
    parser.add_argument('--rounds', type=int, default=1)
    parser.add_argument('--model', default='Qwen/Qwen2.5-Coder-1.5B-Instruct')
    parser.add_argument('--venv', type=Path)
    args = parser.parse_args()
    if args.rounds < 1:
        parser.error('rounds must be positive')
    output = reserve_output(args.output)
    venv = args.venv or Path('/tmp/test4py-modern' if args.runtime == 'modern' else '/tmp/test4py-venv')
    python = venv / 'bin/python'
    bootstrap = 'bootstrap_modern.py' if args.runtime == 'modern' else 'bootstrap_kaggle.py'
    steps = []
    if not shutil.which('uv'):
        steps.append(('install_uv', [sys.executable, '-m', 'pip', 'install', 'uv==0.6.17'], 600))
    steps += [
        ('bootstrap', [sys.executable, BASE / bootstrap, '--venv', venv,
                       '--report-dir', output / 'environment'], 3600),
        ('validation', [python, BASE / 'run.py', '--runtime', args.runtime,
                        '--validate-only', '--output', output / 'validation'], 1800),
        ('comparison', [python, BASE / 'run.py', '--runtime', args.runtime,
                        '--mode', 'compare', '--rounds', str(args.rounds), '--model', args.model,
                        '--output', output / 'comparison'], 60000),
    ]
    report = dict(status='running', output=str(output), runtime=args.runtime, steps=[])
    write_json(output / 'notebook-run.json', report)
    for label, cmd, timeout in steps:
        print(f'Starting {label}; log: {output / (label + ".log")}', flush=True)
        try:
            result = command(cmd, cwd=BASE, timeout=timeout, log_path=output / (label + '.log'))
        except OSError as exc:
            result = dict(returncode=-1, timeout=False, stdout='', stderr=str(exc))
        write_json(output / (label + '-process.json'), result)
        report['steps'].append(dict(name=label, returncode=result['returncode'], timeout=result['timeout']))
        if result['returncode'] != 0 or result['timeout']:
            report.update(status='failed', failed_step=label)
            write_json(output / 'notebook-run.json', report)
            print(f'Stopped at {label}. Reports: {output}\n{(result["stdout"] + result["stderr"])[-3000:]}', flush=True)
            return 1
        write_json(output / 'notebook-run.json', report)
    report['status'] = 'complete'
    write_json(output / 'notebook-run.json', report)
    print(f'Complete. Comparison: {output / "comparison/comparison.json"}', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
