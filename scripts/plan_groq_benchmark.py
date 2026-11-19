#!/usr/bin/env python3
"""Build an offline candidate inventory; never imports subjects or calls an API."""
import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build_plan():
    frame_path = ROOT / 'research/benchmark/projects-upstream.json'
    frame = json.loads(frame_path.read_text())
    local = ROOT / 'local_benchmark_repos'
    # Conservatively treat all existing local subjects as development exposure.
    exposed = {p.name for p in local.iterdir() if p.is_dir()}
    for path in (ROOT / 'research/benchmark').glob('api*.json'):
        data = json.loads(path.read_text())
        for target in data.get('targets', []):
            if isinstance(target, dict) and target.get('project'):
                exposed.add(target['project'])
    known = {'docstring_parser', 'genty', 'PyCG', 'python-string-utils',
             'typesystem', 'codetiming', 'superstring.py', 'woa'}
    exposed.update(known)
    candidates, errors = [], []
    for repo in sorted(local.iterdir()):
        if not repo.is_dir():
            continue
        rev = subprocess.run(['git', '-C', str(repo), 'rev-parse', 'HEAD'],
                             capture_output=True, text=True, check=False)
        status = subprocess.run(['git', '-C', str(repo), 'status', '--porcelain',
                                 '--untracked-files=no'], capture_output=True,
                                text=True, check=False)
        for path in sorted(repo.rglob('*.py')):
            rel = path.relative_to(repo)
            if any(x.startswith('.') or x in {'tests', 'test', '__pycache__',
                   'build', 'dist', 'venv', 'site-packages'} for x in rel.parts):
                continue
            if path.name.startswith('test_') or path.name.endswith('_test.py'):
                continue
            try:
                source = path.read_bytes()
                tree = ast.parse(source)
            except (OSError, SyntaxError, ValueError) as exc:
                errors.append({'project': repo.name, 'file': str(rel),
                               'error_type': type(exc).__name__})
                continue
            for node in tree.body:
                if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    continue
                if node.name.startswith('_'):
                    continue
                candidates.append({'project': repo.name, 'file': str(rel),
                    'symbol': node.name, 'kind': type(node).__name__,
                    'line': node.lineno, 'end_line': node.end_lineno,
                    'source_sha256': digest(source),
                    'revision': rev.stdout.strip() if rev.returncode == 0 else None,
                    'tracked_source_dirty': bool(status.stdout) if status.returncode == 0 else None,
                    'split': 'development', 'runtime_preflight': 'not_run'})
    fresh = [{'project': project, 'module': module,
              'split': 'heldout_candidate_not_locked', 'source_verified': False,
              'runtime_preflight': 'not_run'}
             for project, modules in sorted(frame.items()) if project not in exposed
             for module in sorted(modules)]
    return {'schema_version': 1, 'status': 'offline_inventory_not_efficacy_evidence',
            'provider_budget_usd': 2.0, 'api_calls': 0,
            'source_frame_sha256': digest(frame_path.read_bytes()),
            'exposure_policy': 'existing local repos and previous API manifests are development',
            'exposed_projects': sorted(exposed),
            'development_candidates': candidates, 'parse_errors': errors,
            'heldout_candidates': fresh,
            'heldout_warning': 'Candidate status only; audit prior exposure and pin source/license before locking.',
            'selection_policy': 'No quality outcomes read; no replacement based on model scores.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    plan = build_plan()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as stream:
        json.dump(plan, stream, indent=2, ensure_ascii=False)
        stream.write('\n')
    print(json.dumps({'development_candidates': len(plan['development_candidates']),
                      'heldout_candidate_modules': len(plan['heldout_candidates']),
                      'heldout_candidate_projects': len({x['project'] for x in plan['heldout_candidates']}),
                      'parse_errors': len(plan['parse_errors']), 'api_calls': 0}))


if __name__ == '__main__':
    main()
