"""CPU dependency/import preparation for the locked frame; never runs inference.

Each project has an isolated interpreter. Source/import failures remain recorded;
no replacement targets or production patches are permitted by this entrypoint.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from pilot.common import checkout, command, reserve_output, write_json
from pilot.module_mutation import pool

# Compatibility constraints are identical across arms and frozen before inference.
# These older projects use NumPy/Pandas APIs removed in more recent releases.
CONSTRAINTS = """numpy==1.26.4
pandas==1.5.3
scipy==1.11.4
numba==0.59.1
matplotlib==3.8.4
"""
TOOLS = ['pytest==8.3.5', 'pytest-json-report==1.5.0', 'coverage==7.6.1',
         'setuptools==75.8.2', 'pip==25.0.1', 'wheel==0.45.1']
PYTHON = {'dfsql': '3.9', 'kafka-shell': '3.11', 'pymssa': '3.11', 'pypykatz_server': '3.11'}
EXTRA_REQUIREMENTS = {'pymssa': ['scikit-learn==1.3.2']}


def source_hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*.py'))
            if '.git' not in p.parts and '__pycache__' not in p.parts
            and p.relative_to(root).parts[0] not in ('build', 'dist')}


def prepare(frame, output, uv='uv', resolved=None):
    output = reserve_output(output)
    write_json(output/'frame.json', frame)
    constraint = output/'constraints.txt'
    constraint.write_text(CONSTRAINTS)
    result = dict(stage='import-preparation-only', model_inference_run=False,
                  python_requested=PYTHON, constraints_sha256=hashlib.sha256(constraint.read_bytes()).hexdigest(),
                  tools=TOOLS, projects={}, targets=[])
    for project in sorted({t['project'] for t in frame['targets']}):
        targets = [t for t in frame['targets'] if t['project'] == project]
        spec = targets[0]
        work = output/project
        work.mkdir()
        root, venv = work/'source', work/'venv'
        row = dict(status='preparing', source=str(root), interpreter=str(venv/'bin/python'),
                   commit=spec['commit'], python_requested=PYTHON[project], imports=[])
        result['projects'][project] = row
        before = None
        try:
            checkout(spec['repo_url'], spec['commit'], root)
            before = source_hashes(root)
            for target in targets:
                if before.get(target['file']) != target['source_sha256']:
                    raise ValueError('Locked module source hash changed: '+target['file'])
            write_json(work/'mutant-pools.json', {t['module']:pool((root/t['file']).read_text(),limit=4) for t in targets})
            project_constraint=constraint
            if resolved is not None:
                locked=resolved['preflight']['projects'][project]
                if locked['commit']!=spec['commit'] or locked['python_requested']!=PYTHON[project]:
                    raise ValueError('Resolved dependency lock does not match project/runtime')
                lines=[line for line in locked['requirements_resolved'].splitlines()
                       if line.strip() and ' @ file:' not in line]
                project_constraint=work/'constraints-resolved.txt'
                project_constraint.write_text(CONSTRAINTS+'\n'+'\n'.join(lines)+'\n')
            steps = [('python', [uv, 'python', 'install', PYTHON[project], '--no-bin']),
                     ('venv', [uv, 'venv', '--python', PYTHON[project], venv]),
                     ('tools', [uv, 'pip', 'install', '--python', venv/'bin/python', *TOOLS]),
                     ('project', [uv, 'pip', 'install', '--python', venv/'bin/python',
                                  '--constraint', project_constraint, '--no-build-isolation', str(root)]
                      if (root/'setup.py').exists() or (root/'pyproject.toml').exists() else
                      [uv, 'pip', 'install', '--python', venv/'bin/python',
                       '--constraint', project_constraint, 'pypykatz'])]
            if project in EXTRA_REQUIREMENTS:
                steps.append(('source-dependencies', [uv, 'pip', 'install', '--python', venv/'bin/python',
                              '--constraint', project_constraint, *EXTRA_REQUIREMENTS[project]]))
            for label, args in steps:
                proc = command(args, cwd=work, timeout=600, log_path=work/(label+'.log'))
                write_json(work/(label+'-process.json'), proc)
                if proc['returncode'] or proc['timeout']:
                    raise RuntimeError('Preparation step failed: '+label)
            freeze = command([uv, 'pip', 'freeze', '--python', venv/'bin/python'], timeout=60)
            write_json(work/'freeze-process.json', freeze)
            if freeze['returncode'] or freeze['timeout']:
                raise RuntimeError('Unable to freeze project environment')
            (work/'requirements-resolved.txt').write_text(freeze['stdout'])
            row['requirements_sha256'] = hashlib.sha256(freeze['stdout'].encode()).hexdigest()
            for target in targets:
                # Import without invoking a target or creating a network service.
                code = ('import importlib,json,pathlib,sys; '
                        'm=importlib.import_module(sys.argv[1]); '
                        'p=pathlib.Path(m.__file__).resolve(); '
                        'assert p==pathlib.Path(sys.argv[2]).resolve(),str(p); '
                        'print(json.dumps(dict(module=m.__name__,origin=str(p),python=sys.version)))')
                proc = command([venv/'bin/python', '-c', code, target['module'], root/target['file']],
                               cwd=root, timeout=60,
                               env=dict(os.environ, PYTHONPATH=str(root), PYTHONDONTWRITEBYTECODE='1'))
                write_json(work/(target['id']+'-import.json'), proc)
                entry = dict(id=target['id'], project=project, module=target['module'],
                             status='import_ready' if not proc['returncode'] and not proc['timeout'] else 'import_failed')
                row['imports'].append(entry)
            row['status'] = 'ready' if all(r['status']=='import_ready' for r in row['imports']) else 'import_failed'
        except Exception as exc:
            row.update(status='preparation_failed', error=repr(exc))
        finally:
            if before is not None:
                row['source_integrity'] = source_hashes(root) == before
                write_json(work/'source_hashes.json', before)
                if not row['source_integrity']:
                    row['status'] = 'source_modified'
            observed = {r['id']: r for r in row['imports']}
            result['targets'].extend(observed.get(t['id'], dict(id=t['id'], project=project,
                module=t['module'], status='preparation_failed')) for t in targets)
            write_json(output/'preflight.json', result)
            print('PREFLIGHT', project, row['status'], flush=True)
    result['ready'] = all(p['status']=='ready' for p in result['projects'].values())
    result['planned_arm_trials'] = frame['planned_arm_trials']
    write_json(output/'preflight.json', result)
    print('Reports:', output, flush=True)
    return result['ready']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frame', type=Path, default=BASE/'research/benchmark/api_contract_heldout_frame.json')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--uv', default='uv')
    parser.add_argument('--resolved',type=Path,help='Audited environment lock JSON, relocated without local project file URLs')
    args = parser.parse_args()
    resolved=json.loads(args.resolved.read_text()) if args.resolved else None
    return 0 if prepare(json.loads(args.frame.read_text()), args.output, args.uv, resolved) else 2


if __name__ == '__main__':
    sys.exit(main())
