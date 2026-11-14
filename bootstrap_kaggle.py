"""Create an isolated Python 3.11/CUDA environment even from a Python 3.13 notebook."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

BASE = Path(__file__).resolve().parent
PYTHON_VERSION = '3.11.11'
TORCH_VERSION = '2.5.1'
TORCH_INDEX = 'https://download.pytorch.org/whl/cu121'


def plan(uv, environment):
    python = environment / 'bin/python'
    return [
        [uv, 'venv', '--seed', '--python', PYTHON_VERSION, str(environment)],
        [uv, 'pip', 'install', '--python', str(python), f'torch=={TORCH_VERSION}',
         '--index-url', TORCH_INDEX],
        [uv, 'pip', 'install', '--python', str(python), '--only-binary', 'numpy', '--only-binary', 'tokenizers', '--only-binary', 'chroma-hnswlib', '--only-binary', 'onnxruntime',
         '-r', str(BASE / 'requirements-notebook.txt')],
        [str(python), '-m', 'pip', 'check'],
        [str(python), str(BASE / 'check_environment.py'), '--report', str(environment / 'environment.json')],
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--venv', type=Path, default=BASE / '.venv-kaggle')
    parser.add_argument('--report-dir', type=Path, help='save resolved packages outside the temporary venv')
    parser.add_argument('--dry-run', action='store_true', help='print commands without downloading')
    args = parser.parse_args()
    environment = args.venv.resolve()
    uv = shutil.which('uv')
    if not uv and not args.dry_run:
        parser.error('Install uv first: python -m pip install uv==0.6.17')
    commands = plan(uv or 'uv', environment)
    python = environment / 'bin/python'
    if python.exists():
        # Reuse a successful/partial setup; never clear an existing environment.
        version = subprocess.check_output([str(python), '-c',
                    'import platform; print(platform.python_version())'], text=True).strip()
        if version != PYTHON_VERSION:
            parser.error(f'{environment} uses Python {version}; select a new --venv directory')
        commands = commands[1:]
    for cmd in commands:
        print('+ ' + ' '.join(cmd), flush=True)
        if not args.dry_run:
            subprocess.run(cmd, check=True, cwd=BASE)
    if not args.dry_run:
        freeze = subprocess.check_output([str(python), '-m', 'pip', 'freeze'], text=True)
        (environment / 'requirements-resolved.txt').write_text(freeze)
        if args.report_dir:
            args.report_dir.mkdir(parents=True, exist_ok=True)
            (args.report_dir / 'requirements-resolved.txt').write_text(freeze)
            if (environment / 'environment.json').exists() and args.report_dir.resolve() != environment:
                shutil.copy2(environment / 'environment.json', args.report_dir / 'environment.json')
        print(f'Environment ready: {python}\nResolved versions: {environment / "requirements-resolved.txt"}')
        print(f'{python} run.py --validate-only --output /kaggle/working/validate-real')
    return 0


if __name__ == '__main__':
    sys.exit(main())
