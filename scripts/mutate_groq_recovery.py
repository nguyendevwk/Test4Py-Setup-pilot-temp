#!/usr/bin/env python3
"""Offline, selected-successful-subset mutation screen (never a generation-wide score).

Consumes recovery_summary.json from analyze_groq_recovery.py. Each eligible row
must identify target_id, arm, seed, and stable_nodes (unchanged pytest node suffixes).
Only exact v0.py bytes are replayed. No equivalence or representativeness claims.
Generated tests execute as local code, with a credential-free environment, not an
OS security sandbox. No API client, dependency installation, or coverage is used.
"""
from __future__ import annotations

import argparse
import ast
import collections
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time


LIMITATIONS = [
    'selected-successful-subset: lowest seed with nonempty stable recovered nodes per target/arm; not all generation outputs',
    'At most five syntactic mutants per target, shared across arms; no equivalence claims',
    'Survival does not establish equivalence or correctness; small nonrandom exploratory screen',
    'Collection, import, setup, teardown, timeout, missing nodes and non-assertion failures are inconclusive',
    'Credential-free subprocess environment is not a security sandbox or network isolation',
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write('\n')


def mutants(source, symbol):
    """Single expression edits; leave every other source byte unchanged.

    Definition headers/decorators/defaults are excluded, including nested ones.
    A class target includes method bodies and executable class body statements.
    """
    tree = ast.parse(source)
    matches = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name == symbol]
    if len(matches) != 1:
        raise ValueError(f'Expected one top-level target {symbol!r}')
    lines = source.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line.encode('utf-8')))
    raw = source.encode('utf-8')
    found = []
    compare = {ast.Eq: '!=', ast.NotEq: '==', ast.Lt: '>=', ast.LtE: '>',
               ast.Gt: '<=', ast.GtE: '<', ast.Is: 'is not', ast.IsNot: 'is',
               ast.In: 'not in', ast.NotIn: 'in'}

    def add(node, kind, replacement):
        start = offsets[node.lineno - 1] + node.col_offset
        end = offsets[node.end_lineno - 1] + node.end_col_offset
        changed = raw[:start] + replacement.encode() + raw[end:]
        ast.parse(changed)
        if changed != raw:
            found.append(dict(line=node.lineno, column=node.col_offset, type=kind,
                              replacement=replacement, source=changed.decode('utf-8')))

    def visit(node):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for child in node.body:
                visit(child)
            return
        if isinstance(node, ast.Compare):
            # One operator per mutant, preserving operands and chained semantics.
            for index, op in enumerate(node.ops):
                if type(op) in compare:
                    import copy
                    clone = copy.deepcopy(node)
                    inverse = {ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.Lt: ast.GtE,
                               ast.LtE: ast.Gt, ast.Gt: ast.LtE, ast.GtE: ast.Lt,
                               ast.Is: ast.IsNot, ast.IsNot: ast.Is, ast.In: ast.NotIn, ast.NotIn: ast.In}
                    clone.ops[index] = inverse[type(op)]()
                    add(node, f'comparison_invert_{index}', ast.unparse(clone))
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub)):
            import copy
            clone = copy.deepcopy(node)
            clone.op = ast.Sub() if isinstance(node.op, ast.Add) else ast.Add()
            add(node, 'arithmetic_flip', ast.unparse(clone))
        if isinstance(node, ast.Constant) and type(node.value) is bool:
            add(node, 'bool_flip', repr(not node.value))
        if isinstance(node, ast.Return) and isinstance(node.value, ast.Constant) and type(node.value.value) is not bool:
            value = node.value.value
            replacement = (1 if value == 0 else 0) if type(value) in (int, float) else ('mutation' if value == '' else '') if isinstance(value, str) else False
            add(node.value, 'return_constant_change', repr(replacement))
        for child in ast.iter_child_nodes(node):
            visit(child)

    visit(matches[0])
    return sorted(found, key=lambda m: (m['line'], m['type'], m['column'], m['replacement']))[:5]


def recovery_rows(data):
    """Fail closed on unknown schemas; do not infer recovery from pass counts."""
    rows = data if isinstance(data, list) else data.get('results', data.get('rows', data.get('attempts')))
    if not isinstance(rows, list):
        raise ValueError('Recovery summary must expose results/rows/attempts list')
    for row in rows:
        nodes = row.get('stable_nodes', [])
        if not isinstance(nodes, list) or any(not isinstance(n, str) or not n or n.startswith('::') for n in nodes):
            raise ValueError('stable_nodes must be nonempty pytest node suffixes')
        if nodes:
            yield dict(target_id=row.get('target_id', row.get('target')), arm=row['arm'],
                       seed=int(row['seed']), nodes=['test_generated.py::' + n for n in sorted(set(nodes))],
                       v0_sha256=row['v0_sha256'], source_sha256=row['source_sha256'])


def classify(result, nodes):
    if result['timeout'] or result['returncode'] not in (0, 1):
        return 'inconclusive'
    report = result.get('report', {})
    if any(c.get('outcome') == 'failed' for c in report.get('collectors', [])):
        return 'inconclusive'
    tests = report.get('tests', [])
    if collections.Counter(t.get('nodeid') for t in tests) != collections.Counter(nodes):
        return 'inconclusive'
    killed = False
    for test in tests:
        for phase in ('setup', 'teardown'):
            if test.get(phase, {}).get('outcome') != 'passed':
                return 'inconclusive'
        call = test.get('call', {})
        if call.get('outcome') == 'failed':
            crash = call.get('crash', {}).get('message', '')
            # Only the terminal exception identity, never assertions in source/traceback.
            trace = call.get('traceback', [])
            terminal = trace[-1].get('message', '') if trace else ''
            if not any(re.match(r'^(?:E\s+)?(?:AssertionError|Failed|pytest\.Failed)(?::|$)', message)
                       for message in (crash, terminal)):
                return 'inconclusive'
            killed = True
        elif call.get('outcome') != 'passed' or test.get('outcome') != 'passed':
            return 'inconclusive'
    if killed and result['returncode'] == 1:
        return 'killed'
    return 'survived' if not killed and result['returncode'] == 0 else 'inconclusive'


def execute(root, code, nodes, artifact):
    """Each invocation gets a fresh source copy; artifacts are append-only."""
    artifact.mkdir(parents=True, exist_ok=False)
    (artifact / 'v0.py').write_bytes(code['tests'])
    if code.get('mutation') is not None:
        (artifact / 'mutated_source.py').write_bytes(code['mutation'])
    with tempfile.TemporaryDirectory(prefix='groq-mutation-') as temporary:
        work = Path(temporary)
        repo = work / 'repo'
        shutil.copytree(root, repo, ignore=shutil.ignore_patterns(
            '.git', 'tests', 'test', '__pycache__', '*.pyc', '.venv', 'venv', '.env', '.env.*'))
        # The caller applies mutations through a source payload, only to this copy.
        if digest((repo / code['file']).read_bytes()) != code['original_sha256']:
            raise ValueError('Copied source differs from locked original')
        if code.get('mutation') is not None:
            (repo / code['file']).write_bytes(code['mutation'])
        testfile = nodes[0].split('::', 1)[0]
        if any(n.split('::', 1)[0] != testfile for n in nodes):
            raise ValueError('Selected nodes must refer to the exact single v0 test file')
        relative = Path(testfile)
        if relative.is_absolute() or '..' in relative.parts or relative.suffix != '.py':
            raise ValueError('Recovery node file must be a safe relative Python path')
        suite = work / 'suite'
        suite.mkdir()
        testpath = suite / relative
        testpath.parent.mkdir(parents=True, exist_ok=True)
        testpath.write_bytes(code['tests'])
        reportpath = artifact / 'pytest.json'
        cmd = [sys.executable, '-m', 'pytest', '-q', '-o', 'addopts=', '-c', os.devnull,
               '--rootdir=.', '--confcutdir=' + str(suite), '-p', 'pytest_jsonreport.plugin',
               '--json-report', '--json-report-file=' + str(reportpath), *nodes]
        env = {'PATH': '/usr/bin:/bin', 'HOME': str(work), 'TMPDIR': str(work),
               'LANG': 'C.UTF-8', 'PYTHONPATH': str(repo), 'PYTHONHASHSEED': '0',
               'PYTHONDONTWRITEBYTECODE': '1', 'PYTEST_DISABLE_PLUGIN_AUTOLOAD': '1'}
        start = time.monotonic()
        process = subprocess.Popen(cmd, cwd=suite, env=env, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, start_new_session=True)
        timed = False
        try:
            stdout, stderr = process.communicate(timeout=20)
        except subprocess.TimeoutExpired:
            timed = True
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
        (artifact / 'stdout.txt').write_bytes(stdout)
        (artifact / 'stderr.txt').write_bytes(stderr)
        try:
            report = read(reportpath)
        except (OSError, ValueError):
            report = {}
        result = dict(returncode=process.returncode, timeout=timed,
                      seconds=time.monotonic() - start, command=cmd, report=report)
        write_new(artifact / 'result.json', result)
        return result


def cached_execute(root, code, nodes, directory):
    # Interrupted invocations remain intact; retry in a new numbered directory.
    directory.mkdir(parents=True, exist_ok=True)
    for prior in sorted(directory.glob('run-*/result.json')):
        return read(prior)
    index = 1
    while (directory / f'run-{index:04d}').exists():
        index += 1
    return execute(root, code, nodes, directory / f'run-{index:04d}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--recovery', type=Path, help='Default: STUDY/recovery_summary.json')
    args = parser.parse_args()
    study = args.study.resolve()
    manifest_path = study / 'manifest.json'
    manifest = read(manifest_path)
    recovery_path = (args.recovery or study / 'recovery_summary.json').resolve()
    recovery = read(recovery_path)
    selected = {}
    for row in recovery_rows(recovery):
        key = (row['target_id'], row['arm'])
        if key not in selected or row['seed'] < selected[key]['seed']:
            selected[key] = row
    if len(manifest['targets']) * len(manifest['arms']) * 5 > 90:
        raise ValueError('Screen would exceed the 90 mutant-execution cap')
    output = study / 'mutation_screen'
    output.mkdir(exist_ok=True)
    # Lock implementation and every input. Resuming incompatible work fails closed.
    plan = dict(schema_version=1, label='selected-successful-subset',
                manifest_sha256=digest(manifest_path.read_bytes()),
                recovery_sha256=digest(recovery_path.read_bytes()),
                runner_sha256=digest(Path(__file__).read_bytes()), targets=[])
    payloads = {}
    for target in manifest['targets']:
        root = Path(target['root']).resolve()
        file = Path(target['file'])
        if file.is_absolute() or '..' in file.parts or not (root / file).resolve().is_relative_to(root):
            raise ValueError('Unsafe target source path')
        raw = (root / file).read_bytes()
        if digest(raw) != target['source_sha256']:
            raise ValueError(f"Original source hash mismatch: {target['id']}")
        pool = mutants(raw.decode('utf-8'), target['symbol'])
        entries = []
        for number, mutation in enumerate(pool, 1):
            changed = mutation['source'].encode()
            entries.append(dict(id=f'm{number:02d}', **{k: v for k, v in mutation.items() if k != 'source'},
                                source_sha256=digest(changed), original_source_sha256=digest(raw),
                                diff=''.join(difflib.unified_diff(raw.decode().splitlines(True), mutation['source'].splitlines(True), fromfile=str(file), tofile=str(file)))))
        arms = []
        for arm in manifest['arms']:
            row = selected.get((target['id'], arm))
            if row is None:
                arms.append(dict(arm=arm, status='no_stable_recovered_subset'))
                continue
            attempt = study / 'attempts' / f"{target['id']}__{row['seed']}__{arm}"
            tests = (attempt / 'v0.py').read_bytes()
            if digest(tests) != row['v0_sha256'] or digest(raw) != row['source_sha256']:
                raise ValueError('Recovery evidence hashes do not match v0/source')
            arms.append(dict(arm=arm, seed=row['seed'], nodes=row['nodes'], v0_sha256=digest(tests)))
            payloads[(target['id'], arm)] = tests
        plan['targets'].append(dict(id=target['id'], root=str(root), file=str(file),
                                    original_source_sha256=digest(raw), mutants=entries, arms=arms))
        payloads[target['id']] = pool
    if (output / 'plan.json').exists():
        if read(output / 'plan.json') != plan:
            raise ValueError('Existing mutation screen has different inputs; preserving all outputs')
    else:
        write_new(output / 'plan.json', plan)
    details = []
    for target in plan['targets']:
        for arm in target['arms']:
            if 'nodes' not in arm:
                continue
            base = output / target['id'] / arm['arm']
            code = dict(file=target['file'], original_sha256=target['original_source_sha256'], tests=payloads[(target['id'], arm['arm'])])
            if digest((Path(target['root']) / target['file']).read_bytes()) != target['original_source_sha256']:
                raise ValueError('Original source changed during screen')
            original = cached_execute(Path(target['root']), code, arm['nodes'], base / 'original')
            eligible = classify(original, arm['nodes']) == 'survived'
            for mutation, payload in zip(target['mutants'], payloads[target['id']]):
                status = 'inconclusive'
                reason = 'original_replay_not_allpass'
                if eligible:
                    result = cached_execute(Path(target['root']), dict(code, mutation=payload['source'].encode()), arm['nodes'], base / mutation['id'])
                    status = classify(result, arm['nodes'])
                    reason = status
                details.append(dict(target_id=target['id'], arm=arm['arm'], seed=arm['seed'],
                                    mutant_id=mutation['id'], status=status, reason=reason,
                                    original_allpass=eligible))
    totals = dict(collections.Counter(d['status'] for d in details))
    for status in ('killed', 'survived', 'inconclusive'):
        totals.setdefault(status, 0)
    summary = dict(schema_version=1, label='selected-successful-subset', limitations=LIMITATIONS,
                   denominator_including_inconclusive=len(details), counts=totals,
                   killed_fraction_all_scheduled=totals['killed'] / len(details) if details else None,
                   details=details, selections=plan['targets'],
                   per_arm={arm: dict(denominator_including_inconclusive=sum(d['arm'] == arm for d in details),
                                      counts={status: sum(d['arm'] == arm and d['status'] == status for d in details)
                                              for status in ('killed', 'survived', 'inconclusive')})
                            for arm in manifest['arms']})
    destination = output / 'summary.json'
    if destination.exists() and read(destination) != summary:
        index = 1
        while (output / f'summary.resume-{index:04d}.json').exists():
            index += 1
        destination = output / f'summary.resume-{index:04d}.json'
    if not destination.exists():
        write_new(destination, summary)
    print(json.dumps(dict(summary=str(destination), counts=totals)))


if __name__ == '__main__':
    main()
