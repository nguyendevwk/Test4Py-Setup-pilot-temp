"""Opt-in modern dependencies with Kaggle's existing Python and CUDA Torch."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

BASE = Path(__file__).resolve().parent


def plan(uv, environment, interpreter):
    python = environment / 'bin/python'
    return [
        [uv, 'venv', '--seed', '--system-site-packages', '--python', interpreter, str(environment)],
        [uv, 'pip', 'install', '--python', str(python), '--upgrade',
         '--only-binary', 'numpy', '--only-binary', 'tokenizers', '--only-binary', 'chromadb', '--only-binary', 'onnxruntime',
         '-r', str(BASE / 'requirements-modern.txt')],
        [str(python), str(BASE / 'check_environment.py'), '--runtime', 'modern'],
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--venv', type=Path, default=Path('/tmp/test4py-modern'))
    parser.add_argument('--report-dir', type=Path)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if not args.dry_run and not (3, 11) <= sys.version_info[:2] <= (3, 13):
        parser.error('Modern profile supports Python 3.11–3.13; run with the Kaggle notebook interpreter')
    uv = shutil.which('uv')
    if not uv and not args.dry_run:
        parser.error('Install uv first: python -m pip install uv==0.6.17')
    environment = args.venv.resolve()
    python = environment / 'bin/python'
    marker = environment / 'test4py-modern-profile'
    if environment.exists() and not marker.exists():
        parser.error('Use a fresh --venv path for modern dependencies; keep the legacy venv separate')
    commands = plan(uv or 'uv', environment, sys.executable)
    if python.exists():
        commands = commands[1:]
    env = dict(os.environ, UV_SYSTEM_PYTHON='false', USE_TF='0', USE_FLAX='0')
    if not args.dry_run:
        subprocess.run([sys.executable, '-c',
            'import torch; print("Reusing Torch", torch.__version__, torch.version.cuda); '
            'assert torch.cuda.is_available(), "Enable GPU in Kaggle Settings"'], check=True, env=env)
    for index, cmd in enumerate(commands):
        print('+ ' + ' '.join(cmd), flush=True)
        if not args.dry_run:
            subprocess.run(cmd, check=True, cwd=BASE, env=env)
            if index == 0 and cmd[1] == 'venv':
                marker.write_text('modern\n')
    if not args.dry_run:
        target = args.report_dir or environment
        target.mkdir(parents=True, exist_ok=True)
        freeze = subprocess.check_output([str(python), '-m', 'pip', 'freeze'], text=True, env=env)
        (target / 'requirements-resolved.txt').write_text(freeze)
        # Global Kaggle packages may already have unrelated inconsistencies.
        # Retain pip check for audit; targeted smoke checks above are mandatory.
        check = subprocess.run([str(python), '-m', 'pip', 'check'], capture_output=True, text=True, env=env)
        (target / 'pip-check.txt').write_text(check.stdout + check.stderr)
        if check.returncode:
            print('pip check reported inherited environment conflicts; inspect pip-check.txt')
        print(f'Environment ready: {python}')
        print(f'{python} run.py --runtime modern --validate-only --output /kaggle/working/validate-modern')
    return 0


if __name__ == '__main__':
    sys.exit(main())
