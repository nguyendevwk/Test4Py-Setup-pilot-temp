#!/usr/bin/env python3
"""Offline, secondary replay audit of a completed full-scope study.

No provider calls and no changes to primary outcomes. An explicit --output-root
may resume an audit created by this script; otherwise a fresh audit is created
under STUDY/independent_replays. Recorded failures are never retried or replaced.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import uuid

from run_groq_full_scope import execute, witness
import run_groq_full_scope as runner

DEFAULT = Path(__file__).resolve().parents[1] / 'research/groq_full_scope_20261119'
ARMS = {'source', 'verified_setup', 'context_setup'}
TERMINAL = {'completed', 'quality_gate_failed', 'extraction_failure', 'test_failure',
            'target_not_reached', 'replay_failure', 'execution_timeout', 'execution_error'}
ROLE = 'Secondary independent replay audit; flakiness never changes primary acceptance or inference.'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return digest(path.read_bytes())


def read(path):
    return json.loads(path.read_bytes())


def create_json(path, value):
    """Exclusive creation: immutable receipts/results cannot silently be replaced."""
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def interpreter_path(value):
    located = shutil.which(str(value))
    if located is None:
        raise ValueError('Replay interpreter is not executable: ' + str(value))
    # Preserve venv symlinks: resolving bin/python to the base binary loses the venv.
    return os.path.abspath(located)


def relocated_module(python, module):
    """Locate installed source using the override, without inheriting credentials."""
    script = ("import importlib.util,json,sys,sysconfig;"
              "s=importlib.util.find_spec(sys.argv[1]);"
              "print('REPLAY_MODULE='+json.dumps({'source':s.origin if s else None,"
              "'root':sysconfig.get_path('purelib')}))")
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'),
           'LANG': 'C.UTF-8', 'PYTHONDONTWRITEBYTECODE': '1'}
    cp = subprocess.run([python, '-I', '-B', '-c', script, module], env=env,
                        cwd=Path(python).parent, capture_output=True, text=True, timeout=20)
    records = [line.removeprefix('REPLAY_MODULE=') for line in cp.stdout.splitlines()
               if line.startswith('REPLAY_MODULE=')]
    if cp.returncode or len(records) != 1:
        raise ValueError('Cannot locate pinned source with replay interpreter: ' + module)
    located = json.loads(records[0])
    if not located['source'] or not located['source'].endswith('.py'):
        raise ValueError('Replay interpreter must import Python source: ' + module)
    return located


def load_cases(study, project, python=None):
    manifest_bytes = (study / 'manifest.json').read_bytes()
    m = json.loads(manifest_bytes)
    lock = read(study / 'execution_manifest.json')
    if lock['manifest_sha256'] != digest(manifest_bytes):
        raise ValueError('Manifest differs from execution lock')
    runner_key = 'scripts/run_groq_full_scope.py'
    if sha(Path(runner.__file__)) != lock['implementation_sha256'][runner_key]:
        raise ValueError('Imported runner differs from frozen implementation')
    if len(m['arms']) != 3 or set(m['arms']) != ARMS or m['seed_values'] != [71, 72]:
        raise ValueError('Unexpected study design')
    targets = {t['id']: t for t in m['targets']}
    if len(targets) != len(m['targets']) or len(targets) != 645:
        raise ValueError('Expected 645 unique full-scope targets')
    expected = {(tid, seed, arm) for tid in targets for seed in [71, 72] for arm in ARMS}
    if m['planned'] != 3870 or len(expected) != 3870:
        raise ValueError('Official study requires all 3870 attempts')
    completion = read(study / 'completion.json')
    if completion.get('complete') is not True or completion.get('completed') != 3870 or completion.get('planned') != 3870:
        raise ValueError('Study is not complete; no interim replay audit')
    seen, selected, bindings, locations = set(), [], {}, {}
    for path in sorted((study / 'attempts').glob('*/outcome.json')):
        raw = path.read_bytes()
        row = json.loads(raw)
        key = row['target_id'], row['seed'], row['arm']
        if type(row['seed']) is not int or key not in expected or key in seen:
            raise ValueError('Duplicate/unexpected primary outcome')
        seen.add(key)
        target = targets[row['target_id']]
        if any(row[k] != target[k] for k in ('project', 'module')):
            raise ValueError('Primary outcome target identity mismatch')
        if type(row.get('accepted')) is not bool or row.get('status') not in TERMINAL:
            raise ValueError('Nonterminal or invalid primary outcome')
        bindings[str(path.relative_to(study))] = digest(raw)
        if not row['accepted'] or (project is not None and row['project'] != project):
            continue
        if row['status'] != 'completed':
            raise ValueError('Accepted primary outcome is not completed')
        recorded_codepath = Path(row['final_code'])
        codepath = (path.parent / 'v0.py').resolve()
        if recorded_codepath.parts[-3:] != ('attempts', path.parent.name, 'v0.py'):
            raise ValueError('Recorded code path escapes its original attempt')
        code = codepath.read_bytes()
        # Corroborate saved code against original execution and replay artifacts.
        for prefix in ('eval0', 'replay'):
            originals = list(path.parent.glob(prefix + '/test_generated.py')) + list(path.parent.glob(prefix + '_resume_*/test_generated.py'))
            if not originals or any(p.read_bytes() != code for p in originals):
                raise ValueError('Original executed bytes differ from recorded code')
        execution_target = dict(target)
        if python is not None:
            if target['module'] not in locations:
                locations[target['module']] = relocated_module(python, target['module'])
            located = locations[target['module']]
            execution_target.update(python=python, root=located['root'],
                                    source_file_absolute=located['source'])
        sourcepath = Path(execution_target['source_file_absolute']).resolve()
        if sha(sourcepath) != target['source_bytes_sha256']:
            raise ValueError('Pinned production source changed: ' + target['id'])
        # Full digest names avoid lossy sanitization collisions and unsafe target IDs.
        case_id = digest(json.dumps(key, separators=(',', ':')).encode())
        identity = dict(case_id=case_id, target_id=key[0], seed=key[1], arm=key[2],
                        project=row['project'], module=row['module'],
                        outcome_sha256=digest(raw), code_sha256=digest(code),
                        source_sha256=target['source_bytes_sha256'], source_path=str(sourcepath),
                        recorded_source_path=target['source_file_absolute'],
                        recorded_python=target['python'], execution_python=execution_target['python'],
                        interpreter_override=python,
                        original_line_pct=row['line_pct'], original_nodes=row['test_nodes'])
        if row.get('code_sha256', identity['code_sha256']) != identity['code_sha256']:
            raise ValueError('Recorded code hash mismatch')
        selected.append((identity, execution_target, codepath, code))
    if seen != expected:
        raise ValueError('Missing primary outcomes; all 3870 required before replay')
    if project is not None and project not in {t['project'] for t in targets.values()}:
        raise ValueError('Unknown selected project')
    scope = 'official all-study replay audit' if project is None else 'explicitly selected project subset: ' + project
    receipt = dict(schema=1, role=ROLE, scope=scope, selected_project=project,
                   interpreter_override=python,
                   study=str(study), primary_planned=3870,
                   planned=sum(t['project'] == project for t in targets.values()) * 6 if project else 3870,
                   accepted_count=len(selected), manifest_sha256=digest(manifest_bytes),
                   execution_manifest_sha256=sha(study / 'execution_manifest.json'),
                   runner_sha256=sha(Path(runner.__file__)), replay_script_sha256=sha(Path(__file__)),
                   primary_outcome_sha256=bindings, cases=[c[0] for c in selected])
    return receipt, selected


def evidence_hashes(directory):
    # Bind all durable execution evidence, excluding scratch files under tmp/.
    return {str(p.relative_to(directory)): sha(p) for p in sorted(directory.rglob('*'))
            if p.is_file() and 'tmp' not in p.relative_to(directory).parts}


def replay_case(root, case):
    identity, target, codepath, raw_code = case
    if sha(codepath) != identity['code_sha256'] or sha(Path(identity['source_path'])) != identity['source_sha256']:
        raise ValueError('Code/source changed before replay or resume: ' + identity['case_id'])
    dest = root / 'cases' / identity['case_id']
    resultpath = dest / 'replay_result.json'
    if resultpath.exists():
        result = read(resultpath)
        if result['identity'] != identity:
            raise ValueError('Independent result identity/hash mismatch')
        evdir = dest / result['evidence_directory']
        if evdir.parent != dest or evidence_hashes(evdir) != result['evidence_sha256']:
            raise ValueError('Independent replay evidence changed')
        if result['source_after_sha256'] != identity['source_sha256']:
            raise ValueError('Recorded replay changed source; requires review')
        return result
    dest.mkdir(parents=True, exist_ok=True)
    receiptpath = dest / 'case.json'
    if receiptpath.exists():
        if read(receiptpath) != identity:
            raise ValueError('Independent case identity mismatch')
    else:
        create_json(receiptpath, identity)
    # Never reuse incomplete execution artifacts; preserve them for investigation.
    index = 1
    while (dest / f'execution_{index:04d}').exists():
        index += 1
    evdir = dest / f'execution_{index:04d}'
    result = dict(identity=identity, role=ROLE, evidence_directory=evdir.name,
                  replayed=True, suite_pass=False, passed=False, exact_coverage_match=False,
                  body_witness=False, node_counts=dict(original=identity['original_nodes'], replay=None, matches=False),
                  status='infrastructure_error')
    try:
        evaluation = execute(target, raw_code.decode('utf-8'), evdir)
        if (evdir / 'test_generated.py').read_bytes() != raw_code:
            raise ValueError('Independent execution did not preserve raw generated code bytes')
        body = witness(target, evdir) if (evdir / 'coverage.json').exists() else {'reached': False}
        match = evaluation['line_pct'] is not None and evaluation['line_pct'] == identity['original_line_pct']
        nodes = evaluation['nodes']
        result.update(evaluation=evaluation, target_witness=body, suite_pass=evaluation['suite_pass'],
                      exact_coverage_match=match, body_witness=body['reached'],
                      node_counts=dict(original=identity['original_nodes'], replay=nodes, matches=nodes == identity['original_nodes']),
                      status='replayed', passed=bool(evaluation['suite_pass'] and match and body['reached']))
    except Exception as exc:
        result.update(error_type=type(exc).__name__, error=str(exc)[:1000])
    result['source_after_sha256'] = sha(Path(identity['source_path']))
    if result['source_after_sha256'] != identity['source_sha256'] or sha(codepath) != identity['code_sha256']:
        result.update(passed=False, status='integrity_failure')
    result['evidence_sha256'] = evidence_hashes(evdir)
    create_json(resultpath, result)
    return result


def summarize(receipt, results):
    return dict(role=ROLE, scope=receipt['scope'], planned=receipt['planned'],
                interpreter_override=receipt['interpreter_override'],
                primary_planned=3870, accepted_count=receipt['accepted_count'],
                replayed=len(results), complete=len(results) == receipt['accepted_count'],
                pass_count=sum(r['passed'] for r in results),
                exact_coverage_matches=sum(r['exact_coverage_match'] for r in results),
                body_witness=sum(r['body_witness'] for r in results),
                node_counts=dict(recorded_total=sum(r['node_counts']['original'] for r in results),
                                 replay_total=sum(r['node_counts']['replay'] or 0 for r in results),
                                 matching_cases=sum(r['node_counts']['matches'] for r in results)),
                failures=[r for r in results if not r['passed']], results=results)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study', type=Path, default=DEFAULT)
    parser.add_argument('--output-root', type=Path, help='Fresh directory, or resume a matching independent audit')
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--project', help='Explicit subset; never an official all-study report')
    parser.add_argument('--python', help='Optional pinned replay interpreter; installed source must match original raw hash')
    args = parser.parse_args(argv)
    if args.workers < 1:
        parser.error('--workers must be positive')
    study = args.study.resolve()
    try:
        python = interpreter_path(args.python) if args.python else None
        with ExitStack() as stack:
            # Read-only shared lock refuses overlap with the active generation runner.
            generation_lock = stack.enter_context((study / '.runner.lock').open('rb'))
            fcntl.flock(generation_lock, fcntl.LOCK_SH | fcntl.LOCK_NB)
            receipt, cases = load_cases(study, args.project, python)
            root = args.output_root.resolve() if args.output_root else study / 'independent_replays' / (time.strftime('%Y%m%dT%H%M%S') + '_' + uuid.uuid4().hex)
            if root == study or root in study.parents or (study in root.parents and study / 'independent_replays' not in root.parents):
                raise ValueError('Output must be outside study or below study/independent_replays')
            if root.exists():
                if not (root / 'replay_manifest.json').is_file():
                    raise ValueError('Existing output root is not an independent replay audit')
            else:
                root.mkdir(parents=True, exist_ok=False)
                create_json(root / 'replay_manifest.json', receipt)
            audit_lock = stack.enter_context((root / '.replay.lock').open('a'))
            fcntl.flock(audit_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            if read(root / 'replay_manifest.json') != receipt:
                raise ValueError('Audit inputs/scope changed; use a fresh output root')
            results = []
            with ThreadPoolExecutor(max_workers=args.workers) as pool:
                for result in pool.map(lambda case: replay_case(root, case), cases):
                    results.append(result)
            summary = summarize(receipt, results)
            # Immutable versioned summaries preserve failures and previous audit reports.
            summarypath = root / ('replay_summary_' + uuid.uuid4().hex + '.json')
            create_json(summarypath, summary)
            print(f'Independent replay report: {summarypath}')
            return 0 if all(r['passed'] for r in results) else 1
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.TimeoutExpired) as exc:
        parser.exit(2, f'Replay refused/interrupted; existing evidence retained: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
