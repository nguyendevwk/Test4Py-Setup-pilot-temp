#!/usr/bin/env python3
"""Supplementary exploratory integration/usability audit, added after generation began.

Assemble every accepted suite without editing bytes. Never replace primary
inference. Requires the complete 3870-outcome study; no API calls.
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
import signal
import subprocess
import time

DEFAULT = Path(__file__).resolve().parents[1] / 'research/groq_full_scope_20261119'
ARMS = ('source', 'verified_setup', 'context_setup')
TERMINAL = {'completed', 'quality_gate_failed', 'extraction_failure', 'test_failure',
            'target_not_reached', 'replay_failure', 'execution_timeout', 'execution_error'}
ROLE = ('Supplementary exploratory integration/usability audit; protocol added AFTER '
        'generation started. Uses all accepted suites across both seeds, without '
        'selection or edits. Never replaces primary inference or acceptance.')

# Run pytest and export locked-file coverage in the SAME fresh subprocess. The
# export deliberately analyzes every eligible file, even when it was never run.
HARNESS = r'''
import json, pathlib, sys, traceback
import coverage
import pytest
config = json.loads(pathlib.Path(sys.argv[1]).read_bytes())
cov = coverage.Coverage(data_file='.coverage', branch=True, include=config['source_files'])
cov.start()
exitcode = None
try:
    exitcode = int(pytest.main(['-q', '-o', 'addopts=', '--confcutdir='+config['cwd'],
        '-p', 'pytest_jsonreport.plugin', '--json-report',
        '--json-report-file=pytest.json', config['tests']]))
except BaseException:
    traceback.print_exc()
finally:
    cov.stop()
    cov.save()
    files = {}
    errors = {}
    data = cov.get_data()
    measured = {str(pathlib.Path(p).resolve()) for p in data.measured_files()}
    actual_data = any(data.lines(p) for p in data.measured_files())
    for file in config['source_files']:
        try:
            filename, statements, excluded, missing, formatted = cov.analysis2(file)
            files[file] = dict(statements=sorted(statements), missing=sorted(missing),
                excluded=sorted(excluded), measured_file=str(pathlib.Path(file).resolve()) in measured)
        except BaseException as exc:
            errors[file] = type(exc).__name__+': '+str(exc)
    pathlib.Path('locked_coverage.json').write_text(json.dumps(dict(
        actual_data=bool(actual_data), files=files, errors=errors), indent=2))
sys.exit(exitcode if exitcode is not None else 2)
'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def verify_sources(sources):
    for path, expected in sources.items():
        if sha(Path(path)) != expected:
            raise ValueError('Locked source changed: ' + path)


def load_plan(study):
    manifest = read(study / 'manifest.json')
    lock = read(study / 'execution_manifest.json')
    if lock['manifest_sha256'] != sha(study / 'manifest.json'):
        raise ValueError('Manifest differs from execution lock')
    completion = read(study / 'completion.json')
    if (completion.get('complete') is not True or completion.get('completed') != 3870
            or completion.get('planned') != 3870 or manifest['planned'] != 3870):
        raise ValueError('Refusing packs until all 3870 primary outcomes are complete')
    targets = {t['id']: t for t in manifest['targets']}
    projects = sorted({t['project'] for t in targets.values()})
    if (len(targets) != 645 or len(targets) != len(manifest['targets']) or len(projects) != 21
            or set(manifest['arms']) != set(ARMS) or len(manifest['arms']) != 3
            or manifest['seed_values'] != [71, 72]):
        raise ValueError('Unexpected full-scope design')
    expected = {(tid, seed, arm) for tid in targets for seed in [71, 72] for arm in ARMS}
    packs = {}
    for project in projects:
        selected = [t for t in targets.values() if t['project'] == project]
        environments = {(t['python'], t['root']) for t in selected}
        if len(environments) != 1:
            raise ValueError('Inconsistent recorded project environment: ' + project)
        python, site = environments.pop()
        sources, modules = {}, {}
        for target in selected:
            path = str(Path(target['source_file_absolute']).resolve())
            if path in sources and sources[path] != target['source_bytes_sha256']:
                raise ValueError('Conflicting locked source hashes')
            sources[path] = target['source_bytes_sha256']
            modules.setdefault(target['module'], set()).add(path)
        verify_sources(sources)
        for arm in ARMS:
            key = hashlib.sha256(json.dumps([project, arm]).encode()).hexdigest()
            packs[project, arm] = dict(pack_id=key, project=project, arm=arm,
                python=python, site=site, source_sha256=sources,
                eligible_modules={k: sorted(v) for k, v in sorted(modules.items())}, suites=[])
    seen, outcomes = set(), {}
    for path in sorted((study / 'attempts').glob('*/outcome.json')):
        row = read(path)
        key = row['target_id'], row['seed'], row['arm']
        if type(row['seed']) is not int or key not in expected or key in seen:
            raise ValueError('Unexpected/duplicate primary outcome')
        seen.add(key)
        target = targets[row['target_id']]
        if any(row[k] != target[k] for k in ('project', 'module')):
            raise ValueError('Outcome/manifest identity mismatch')
        if type(row.get('accepted')) is not bool or row.get('status') not in TERMINAL:
            raise ValueError('Invalid or nonterminal primary outcome')
        outcome_hash = sha(path)
        outcomes[str(path.relative_to(study))] = outcome_hash
        if not row['accepted']:
            continue
        if row['status'] != 'completed' or type(row.get('test_nodes')) is not int or row['test_nodes'] < 3:
            raise ValueError('Accepted outcome lacks valid original test nodes')
        codepath = path.parent / 'v0.py'
        if Path(row['final_code']).resolve() != codepath.resolve():
            raise ValueError('Recorded accepted code path mismatch')
        codehash = sha(codepath)
        for prefix in ('eval0', 'replay'):
            evidence = list(path.parent.glob(prefix + '/test_generated.py')) + list(path.parent.glob(prefix + '_resume_*/test_generated.py'))
            if not evidence or any(sha(p) != codehash for p in evidence):
                raise ValueError('Recorded code differs from primary execution evidence')
        # Include identity in the digest: identical suites from different seeds
        # remain separate test files and each contributes its original node count.
        filename = 'test_' + hashlib.sha256(json.dumps([key, codehash]).encode()).hexdigest() + '.py'
        packs[target['project'], row['arm']]['suites'].append(dict(
            target_id=key[0], seed=key[1], arm=key[2], module=row['module'],
            code_path=str(codepath.resolve()), code_sha256=codehash, filename=filename,
            original_test_nodes=row['test_nodes'], outcome_sha256=outcome_hash,
            outcome_path=str(path.relative_to(study))))
    if seen != expected:
        raise ValueError('Exact 3870-outcome Cartesian product is required')
    plan = dict(schema=1, role=ROLE, study=str(study), planned=3870, projects=projects,
                manifest_sha256=sha(study / 'manifest.json'),
                execution_manifest_sha256=sha(study / 'execution_manifest.json'),
                completion_sha256=sha(study / 'completion.json'),
                assembler_sha256=sha(Path(__file__)), outcome_sha256=outcomes,
                packs=list(packs.values()), timeout_seconds=120)
    return plan


def evidence_hashes(work):
    names = ('harness.py', 'config.json', 'stdout.txt', 'stderr.txt', 'pytest.json',
             '.coverage', 'locked_coverage.json')
    paths = [work / name for name in names if (work / name).is_file()]
    paths += sorted((work / 'tests').glob('test_*.py'))
    return {str(path.relative_to(work)): sha(path) for path in paths}


def run_pack(root, pack):
    sources = pack['source_sha256']
    verify_sources(sources)
    for suite in pack['suites']:
        if sha(Path(suite['code_path'])) != suite['code_sha256']:
            raise ValueError('Accepted code changed before pack assembly')
    dest = root / 'packs' / pack['pack_id']
    resultpath = dest / 'pack_result.json'
    if resultpath.exists():
        result = read(resultpath)
        if result['identity'] != pack:
            raise ValueError('Completed pack identity differs; refusing reuse')
        work = dest / result['execution_directory']
        if work.parent != dest or evidence_hashes(work) != result['evidence_sha256']:
            raise ValueError('Completed pack evidence changed')
        # Completed failures are preserved, never retried.
        return result
    dest.mkdir(parents=True, exist_ok=True)
    receipt = dest / 'pack_identity.json'
    if receipt.exists():
        if read(receipt) != pack:
            raise ValueError('Pack identity changed')
    else:
        create(receipt, pack)
    attempt = 1
    while (dest / f'execution_{attempt:04d}').exists():
        attempt += 1
    work = dest / f'execution_{attempt:04d}'
    work.mkdir()
    for name in ('home', 'tmp', 'tests'):
        (work / name).mkdir()
    expected = sum(s['original_test_nodes'] for s in pack['suites'])
    result = dict(identity=pack, role=ROLE, execution_directory=work.name,
        status='empty' if not pack['suites'] else 'infrastructure_error',
        empty=not pack['suites'], expected_nodes=expected, collected_nodes=None if pack['suites'] else 0,
        node_count_matches=not pack['suites'], suite_pass=False, pack_pass=False,
        measured_coverage_pct=None, validated_pack_coverage_pct=0,
        statements=None, missing=None, timeout=False)
    for suite in pack['suites']:
        raw = Path(suite['code_path']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != suite['code_sha256']:
            raise ValueError('Code changed during assembly')
        with (work / 'tests' / suite['filename']).open('xb') as stream:
            stream.write(raw)
    if pack['suites']:
        try:
            (work / 'harness.py').write_text(HARNESS)
            create(work / 'config.json', dict(cwd=str(work), tests=str(work / 'tests'),
                source_files=sorted(sources)))
            env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'),
                   'HOME': str(work / 'home'), 'TMPDIR': str(work / 'tmp'),
                   'LANG': 'C.UTF-8', 'PYTHONPATH': pack['site'],
                   'PYTHONHASHSEED': '0', 'PYTHONDONTWRITEBYTECODE': '1',
                   'PYTEST_DISABLE_PLUGIN_AUTOLOAD': '1', 'COVERAGE_FILE': str(work / '.coverage')}
            start = time.monotonic()
            # File-backed output avoids unbounded in-memory subprocess buffers.
            with (work / 'stdout.txt').open('xb') as stdout, (work / 'stderr.txt').open('xb') as stderr:
                process = subprocess.Popen([pack['python'], str(work / 'harness.py'), str(work / 'config.json')],
                    cwd=work, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
                try:
                    process.wait(timeout=120)
                except subprocess.TimeoutExpired:
                    result['timeout'] = True
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
            result.update(returncode=process.returncode, seconds=time.monotonic()-start,
                          status='timeout' if result['timeout'] else 'completed')
            report = read(work / 'pytest.json') if (work / 'pytest.json').exists() else {}
            tests = report.get('tests', [])
            # pytest's collected total also counts deselected/skipped-at-collection
            # items that might be absent from individual execution records.
            collected = report.get('summary', {}).get('collected')
            if type(collected) is not int:
                collected = len(tests) if report else None
            count_match = collected == expected and len(tests) == expected
            passed = bool(not result['timeout'] and process.returncode == 0 and tests
                          and all(t.get('outcome') == 'passed' for t in tests))
            result.update(collected_nodes=collected, execution_records=len(tests),
                          node_count_matches=count_match, suite_pass=passed, pack_pass=passed and count_match)
            coveragepath = work / 'locked_coverage.json'
            if coveragepath.exists():
                coverage = read(coveragepath)
                result['locked_file_coverage'] = coverage
                # Timeout/no-data/partial analysis are NA, never fabricated zero.
                if (not result['timeout'] and coverage['actual_data'] and not coverage['errors']
                        and set(coverage['files']) == set(sources)):
                    statements = sum(len(f['statements']) for f in coverage['files'].values())
                    missing = sum(len(f['missing']) for f in coverage['files'].values())
                    result.update(statements=statements, missing=missing,
                                  measured_coverage_pct=100*(statements-missing)/statements if statements else None)
            if result['pack_pass'] and result['measured_coverage_pct'] is not None:
                result['validated_pack_coverage_pct'] = result['measured_coverage_pct']
        except Exception as exc:
            result.update(status='infrastructure_error', pack_pass=False,
                          validated_pack_coverage_pct=0, error_type=type(exc).__name__, error=str(exc)[:1000])
    changed = {p: sha(Path(p)) if Path(p).is_file() else None for p in sources}
    result['source_after_sha256'] = changed
    if changed != sources:
        result.update(status='integrity_failure', pack_pass=False, validated_pack_coverage_pct=0)
    if any(sha(Path(s['code_path'])) != s['code_sha256'] for s in pack['suites']):
        result.update(status='integrity_failure', pack_pass=False, validated_pack_coverage_pct=0)
    result['evidence_sha256'] = evidence_hashes(work)
    create(resultpath, result)
    return result


def summarize(plan, results):
    arms = {}
    for arm in ARMS:
        selected = [r for r in results if r['identity']['arm'] == arm]
        measured = [r['measured_coverage_pct'] for r in selected if r['measured_coverage_pct'] is not None]
        arms[arm] = dict(packs_pass=sum(r['pack_pass'] for r in selected), denominator=21,
            expected_nodes=sum(r['expected_nodes'] for r in selected),
            collected_nodes=sum(r['collected_nodes'] or 0 for r in selected),
            collected_nodes_unavailable=sum(r['collected_nodes'] is None for r in selected),
            measured_coverage_pct_by_project={r['identity']['project']: r['measured_coverage_pct'] for r in selected},
            measured_available_projects=len(measured),
            mean_measured_coverage_pct_available_projects=sum(measured)/len(measured) if measured else None,
            validated_pack_coverage_pct_by_project={r['identity']['project']: r['validated_pack_coverage_pct'] for r in selected},
            equal_project_validated_pack_coverage_pct=sum(r['validated_pack_coverage_pct'] for r in selected)/21)
    return dict(role=ROLE, primary_outcomes_unchanged=True, complete=len(results) == 63,
                projects=21, planned_packs=63, completed_packs=len(results), arms=arms,
                coverage_note='Measured coverage is NA for empty, timeout, no-data or incomplete analysis. Validated coverage penalizes every nonpassing/unvalidated pack to zero; measured available-case means use a different denominator.',
                manifest_sha256=plan['manifest_sha256'], outcome_sha256=plan['outcome_sha256'], results=results)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study', type=Path, default=DEFAULT)
    parser.add_argument('--output-root', type=Path, help='Fresh output root or resume a matching pack audit')
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args(argv)
    if args.workers < 1:
        parser.error('--workers must be positive')
    study = args.study.resolve()
    try:
        with ExitStack() as stack:
            generation_lock = stack.enter_context((study / '.runner.lock').open('rb'))
            fcntl.flock(generation_lock, fcntl.LOCK_SH | fcntl.LOCK_NB)
            plan = load_plan(study)
            root = args.output_root.resolve() if args.output_root else study / 'joint_packs' / 'main'
            allowed = study / 'joint_packs'
            if root == study or root in study.parents or (study in root.parents and allowed not in root.parents):
                raise ValueError('Outputs must be outside study or under study/joint_packs')
            if root.exists():
                if not (root / 'pack_manifest.json').is_file():
                    raise ValueError('Existing output root is not a pack audit')
            else:
                root.mkdir(parents=True, exist_ok=False)
                create(root / 'pack_manifest.json', plan)
            lock = stack.enter_context((root / '.packs.lock').open('a'))
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            if read(root / 'pack_manifest.json') != plan:
                raise ValueError('Pack audit inputs changed; use a fresh output root')
            results = []
            with ThreadPoolExecutor(max_workers=args.workers) as pool:
                for result in pool.map(lambda pack: run_pack(root, pack), plan['packs']):
                    results.append(result)
            summary = summarize(plan, results)
            summarypath = root / 'summary.json'
            if summarypath.exists():
                if read(summarypath) != summary:
                    raise ValueError('Existing immutable summary differs')
            else:
                create(summarypath, summary)
            print(f'Supplementary pack audit: {summarypath}')
            return 0 if all(r['pack_pass'] or r['empty'] for r in results) else 1
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as exc:
        parser.exit(2, f'Pack audit refused/interrupted; existing evidence retained: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
