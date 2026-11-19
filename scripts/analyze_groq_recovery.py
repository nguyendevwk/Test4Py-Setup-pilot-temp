#!/usr/bin/env python3
"""Secondary, descriptive v0 recovery analysis; never changes primary outcomes.

Only eval0 nodes passing setup, call and teardown are selected. The complete v0
module is copied byte-for-byte; pytest node IDs select tests without rewriting
code. Two fresh processes/directories replay that selection. Coverage describes
that selected suite (not an isolated stable subset if another selected test fails).
Generated tests execute local code; the minimal environment is not a sandbox.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import time
import tokenize

REPO = Path(__file__).resolve().parents[1]
DEFAULT_STUDY = REPO / 'research/groq_study_20261118_v2'


def read_json(path):
    return json.loads(path.read_text())


def write_json(path, value):
    # Atomic summaries/completion markers; replay evidence is never overwritten.
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False) as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write('\n')
        name = f.name
    os.replace(name, path)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def passed_nodes(report):
    return {t['nodeid'].split('::', 1)[1] for t in report.get('tests', [])
            if '::' in t.get('nodeid', '') and t.get('outcome') == 'passed'
            and all(t.get(p, {}).get('outcome') == 'passed'
                    for p in ('setup', 'call', 'teardown'))}


def body_lines(source, symbol):
    """Statement start lines in bodies; exclude docstrings and def/class headers.

    Using statement starts rather than entire compound-statement spans prevents
    nested definitions and their decorators from becoming import-only witnesses.
    Nested executable bodies are included, as are all methods for a class target.
    """
    tree = ast.parse(source)
    node = tree
    for part in symbol.split('.'):
        node = next(n for n in node.body if isinstance(
            n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == part)
    funcs = ((ast.FunctionDef, ast.AsyncFunctionDef))
    if isinstance(node, ast.ClassDef):
        roots = [n for n in ast.walk(node) if isinstance(n, funcs)]
    elif isinstance(node, funcs):
        roots = [node]
    else:
        raise ValueError('Target must be a function, method or class')
    lines = set()
    for fn in roots:
        for stmt in fn.body:
            for n in ast.walk(stmt):
                if not isinstance(n, ast.stmt) or isinstance(n, (*funcs, ast.ClassDef)):
                    continue
                if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str):
                    continue
                lines.add(n.lineno)
    return lines


def run_command(cmd, work, env, prefix, timeout):
    started = time.monotonic()
    with (work / (prefix + '.stdout.txt')).open('wb') as out, (work / (prefix + '.stderr.txt')).open('wb') as err:
        proc = subprocess.Popen(cmd, cwd=work, env=env, stdout=out, stderr=err,
                                start_new_session=True)
        timed_out = False
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
    result = dict(command=cmd, returncode=proc.returncode, timeout=timed_out,
                  seconds=time.monotonic() - started)
    write_json(work / (prefix + '.process.json'), result)
    return result


def replay(dest, code, selected, target, executable, timeout, witness_lines):
    work = Path(tempfile.mkdtemp(prefix='replay-', dir=dest))
    (work / 'test_generated.py').write_bytes(code)
    env = {'PATH': '/usr/bin:/bin', 'HOME': str(work), 'TMPDIR': str(work),
           'LANG': 'C.UTF-8', 'PYTHONPATH': str(Path(target['root']).resolve()),
           'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONHASHSEED': '0',
           'PYTEST_DISABLE_PLUGIN_AUTOLOAD': '1', 'COVERAGE_FILE': str(work / '.coverage'),
           'COVERAGE_RCFILE': os.devnull}
    cmd = [str(executable), '-m', 'coverage', 'run', '--rcfile=' + os.devnull,
           '--branch', '--source=' + target['module'], '-m', 'pytest',
           '-q', '-c', os.devnull, '-o', 'addopts=', '-p', 'no:cacheprovider',
           '--rootdir=' + str(work), '--confcutdir=' + str(work),
           '-p', 'pytest_jsonreport.plugin', '--json-report',
           '--json-report-file=' + str(work / 'pytest.json')]
    cmd += ['test_generated.py::' + n for n in sorted(selected)]
    process = run_command(cmd, work, env, 'pytest', timeout)
    cov_process = run_command([str(executable), '-m', 'coverage', 'json',
                               '--rcfile=' + os.devnull, '-o', str(work / 'coverage.json')],
                              work, env, 'coverage', timeout)
    report = read_json(work / 'pytest.json') if (work / 'pytest.json').exists() else {}
    passed = passed_nodes(report) & selected
    coverage = read_json(work / 'coverage.json') if (work / 'coverage.json').exists() else {}
    source_path = (Path(target['root']) / target['file']).resolve()
    module_files = [v for k, v in coverage.get('files', {}).items()
                    if (work / k).resolve() == source_path]
    executed = set().union(*(set(v.get('executed_lines', [])) for v in module_files))
    valid = not process['timeout'] and process['returncode'] in (0, 1)
    result = dict(directory=work.name, process=process, coverage_process=cov_process,
                  passed_nodes=sorted(passed if valid else set()),
                  suite_pass=process['returncode'] == 0 and passed == selected,
                  module_coverage_counts=module_files[0].get('summary') if module_files else None,
                  module_executed_lines=sorted(executed),
                  target_body_executed_lines=sorted(executed & witness_lines),
                  target_reached=bool(executed & witness_lines),
                  coverage_available=cov_process['returncode'] == 0 and bool(module_files))
    write_json(work / 'result.json', result)
    return result


def analyze_attempt(study, dest, target, arm, seed, executable, timeout):
    original = study / 'attempts' / dest.name
    report_path = original / 'eval0/pytest.json'
    code_path = original / 'v0.py'
    if not report_path.exists() or not code_path.exists():
        return None, 'pending_eval0'
    try:
        report_bytes = report_path.read_bytes()
        report = json.loads(report_bytes)
    except (ValueError, OSError):
        return None, 'pending_eval0'
    # A running pytest report must not be frozen as completed recovery evidence.
    if 'exitcode' not in report or 'summary' not in report:
        return None, 'pending_eval0'
    code = code_path.read_bytes()
    evaluated = original / 'eval0/test_generated.py'
    if not evaluated.exists() or evaluated.read_bytes() != code:
        return None, 'v0_eval0_mismatch'
    source_path = Path(target['root']) / target['file']
    source_bytes = source_path.read_bytes()
    if digest(source_bytes) != target['source_sha256']:
        return None, 'source_hash_mismatch'
    with tokenize.open(source_path) as f:
        witness = body_lines(f.read(), target['symbol'])
    selected = passed_nodes(report)
    dest.mkdir(exist_ok=False)
    (dest / 'v0.py').write_bytes(code)
    (dest / 'original_pytest.json').write_bytes(report_bytes)
    tests = report.get('tests', [])
    collected = {r['nodeid'] for c in report.get('collectors', [])
                 for r in c.get('result', []) if r.get('type') in ('Function', 'TestCaseFunction')}
    generated_count = max(len(collected), report['summary'].get('collected', 0), len(tests))
    row = dict(target_id=target['id'], arm=arm, seed=seed,
               v0_sha256=digest(code), eval0_sha256=digest(report_bytes),
               source_sha256=digest(source_bytes), original_generated_nodes=generated_count,
               original_reported_nodes=len(tests), original_summary=report['summary'],
               original_suite_pass=report['exitcode'] == 0 and bool(tests) and len(selected) == len(tests),
               eligible_nodes=sorted(selected), eligible_count=len(selected),
               target_body_statement_lines=sorted(witness))
    write_json(dest / 'selection.json', row)
    runs = [replay(dest, code, selected, target, executable, timeout, witness)
            for _ in range(2)] if selected else []
    stable = selected.intersection(*(set(r['passed_nodes']) for r in runs)) if runs else set()
    row.update(replays=runs, stable_nodes=sorted(stable), stable_count=len(stable),
               recovery_has_stable_nonempty_tests=bool(stable),
               target_reached_both_replays=bool(runs) and all(r['target_reached'] for r in runs),
               stable_suite_target_reached=bool(stable) and stable == selected
               and all(r['suite_pass'] and r['coverage_available'] and r['target_reached'] for r in runs),
               status='completed')
    write_json(dest / 'result.json', row)
    return row, 'completed'


def aggregate(rows, planned, statuses):
    generated = sum(r['original_generated_nodes'] for r in rows)
    eligible = sum(r['eligible_count'] for r in rows)
    stable = sum(r['stable_count'] for r in rows)
    return dict(planned_attempts=planned, completed_recovery_attempts=len(rows),
                unavailable_or_preserved_attempts=statuses,
                original_generated_nodes=generated, eligible_nodes=eligible, stable_nodes=stable,
                eligible_retention=dict(numerator=eligible, denominator=generated,
                                        fraction=eligible / generated if generated else None),
                stable_retention=dict(numerator=stable, denominator=generated,
                                      fraction=stable / generated if generated else None),
                stable_of_eligible=dict(numerator=stable, denominator=eligible,
                                       fraction=stable / eligible if eligible else None),
                recovery_has_stable_nonempty_tests=sum(r['recovery_has_stable_nonempty_tests'] for r in rows),
                target_reached_both_replays=sum(r['target_reached_both_replays'] for r in rows),
                stable_suite_target_reached=sum(r['stable_suite_target_reached'] for r in rows),
                original_suite_pass=sum(r['original_suite_pass'] for r in rows))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study', type=Path, default=DEFAULT_STUDY)
    parser.add_argument('--timeout', type=float, default=30)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    study = args.study.resolve()
    manifest = read_json(study / 'manifest.json')
    executable = REPO / '.venv/bin/python'
    if not executable.is_file():
        parser.error('Missing repository .venv/bin/python')
    recovery = study / 'recovery'
    recovery.mkdir(exist_ok=True)
    rows, states = [], []
    for target in manifest['targets']:
        for seed in manifest['seed_values']:
            for arm in manifest['arms']:
                label = f"{target['id']}__{seed}__{arm}"
                dest = recovery / label
                if dest.exists():
                    if (dest / 'result.json').exists():
                        row = read_json(dest / 'result.json')
                        status = 'completed'
                    else:
                        row, status = None, 'preserved_incomplete_recovery'
                else:
                    try:
                        row, status = analyze_attempt(study, dest, target, arm, seed, executable, args.timeout)
                    except Exception as exc:
                        row, status = None, 'error:' + type(exc).__name__
                if row is not None:
                    rows.append(row)
                states.append(dict(attempt=label, target_id=target['id'], arm=arm, status=status))
    def group(arm, target_id=None):
        relevant = [s for s in states if s['arm'] == arm and
                    (target_id is None or s['target_id'] == target_id)]
        subset = [r for r in rows if r['arm'] == arm and
                  (target_id is None or r['target_id'] == target_id)]
        return aggregate(subset, len(relevant), [s for s in relevant if s['status'] != 'completed'])
    summary = dict(analysis='secondary_descriptive_v0_recovery_not_primary_efficacy',
                   caveats=['Primary study outcomes are unchanged.',
                            'Retention denominators include only attempts with completed recovery evidence.',
                            'Missing eval0 evidence is pending; rerun to fill remaining attempts.',
                            'Coverage is for the selected suite, not individual stable nodes.',
                            'Dependency imports and target definition-only lines are not target witnesses.',
                            'Existing incomplete recovery directories are preserved without retry.'],
                   planned_attempts=len(states), completed_recovery_attempts=len(rows),
                   arms={arm: group(arm) for arm in manifest['arms']},
                   target_level={t['id']: {arm: group(arm, t['id']) for arm in manifest['arms']}
                                 for t in manifest['targets']}, attempts=rows, attempt_statuses=states)
    write_json(study / 'recovery_summary.json', summary)
    print(json.dumps(dict(summary=str(study / 'recovery_summary.json'),
                          completed=len(rows), planned=len(states))))


if __name__ == '__main__':
    main()
