"""Execution and evidence gates for the Council development screen (stdlib only).
Subprocess isolation is not a security sandbox for untrusted code.
"""
import ast
import json
import os
from pathlib import Path
import re
import sys

from pilot.common import command, write_json


def clean_code_block(raw_text):
    """Select only a uniquely plausible complete test module; preserve ambiguity.

    A diagnostic block may precede the module. Length is never evidence of validity.
    compile(), not just ast.parse(), catches illegal global declarations.
    """
    from pilot.quality import final_answer
    answer, status = final_answer(raw_text)
    if not answer:
        raise ValueError('Incomplete answer: ' + status)
    if '```' in answer:
        if answer.count('```') % 2:
            raise ValueError('Unclosed code fence')
        blocks = re.findall(r'```([^\n`]*)\n(.*?)```', answer, re.S)
        candidates = [body for lang, body in blocks if lang.strip().lower() in ('', 'python', 'py')]
    else:
        candidates = [answer]
    valid = []
    for body in candidates:
        try:
            tree = ast.parse(body.strip())
            compile(tree, '<generated>', 'exec')
            # pytest collects top-level functions and methods of Test* classes.
            tests = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith('test_')]
            for cls in tree.body:
                if isinstance(cls, ast.ClassDef) and cls.name.startswith('Test'):
                    tests.extend(n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith('test_'))
            if tests:
                valid.append(body.strip())
        except (SyntaxError, ValueError):
            continue
    if len(valid) != 1:
        raise ValueError(f'Expected one compilable test module; found {len(valid)}')
    return valid[0] + '\n'


def checkout_env(root):
    root = Path(root).resolve()
    return dict(os.environ, PYTHONPATH=os.pathsep.join([str(root), str(root/'src')]),
                PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')


def probe_setup_candidate(code, repo_root, timeout=5):
    result = command([sys.executable, '-c', code], cwd=repo_root,
                     env=checkout_env(repo_root), timeout=timeout)
    return dict(accepted=result['returncode'] == 0 and not result['timeout'],
                scope='curated setup execution only; not target invocation verification', process=result)


def inspect_api(root, module, symbol, timeout=20):
    script = '''import importlib, inspect, json
from pathlib import Path
m = importlib.import_module(MODULE)
obj = m
for part in SYMBOL.split('.'):
    obj = getattr(obj, part)
def describe(mod):
    rows = []
    for name in sorted(n for n in vars(mod) if not n.startswith('_')):
        value = getattr(mod, name)
        try: sig = str(inspect.signature(value)) if callable(value) else ''
        except (TypeError, ValueError): sig = ''
        if isinstance(value, type) and hasattr(value, '__members__'):
            sig += ' members=' + repr(list(value.__members__))
        rows.append(name + sig)
    return rows[:100]
parent = importlib.import_module(MODULE.split('.')[0])
print(json.dumps(dict(module=MODULE, symbol=SYMBOL, file=m.__file__,
    signature=str(inspect.signature(obj)), module_symbols=describe(m),
    package_symbols=describe(parent))))
'''.replace('MODULE', repr(module)).replace('SYMBOL', repr(symbol))
    result = command([sys.executable, '-c', script], cwd=root, env=checkout_env(root), timeout=timeout)
    if result['returncode'] or result['timeout']:
        raise RuntimeError('API preflight failed: ' + json.dumps(result))
    payload = json.loads(result['stdout'].splitlines()[-1])
    actual = Path(payload['file']).resolve()
    if not actual.is_relative_to(Path(root).resolve()):
        raise RuntimeError(f'Imported installed package instead of checkout: {actual}')
    return payload


def execute_pytest_and_coverage(test_code, repo_root, target_module, work_dir, timeout=30, node_suffixes=None):
    root, work = Path(repo_root).resolve(), Path(work_dir).resolve()
    work.mkdir(parents=True, exist_ok=False)
    test_file, report_file = work/'test_run.py', work/'pytest_report.json'
    test_file.write_text(test_code)
    env = dict(checkout_env(root), COVERAGE_FILE=str(work/'.coverage'))
    proc = command([sys.executable, '-m', 'coverage', 'run', '--branch',
                    '--source='+target_module, '-m', 'pytest', '-q', '-o', 'addopts=',
                    '--confcutdir='+str(work), '-p', 'pytest_jsonreport.plugin',
                    '--json-report', '--json-report-file='+str(report_file), *([str(test_file)+'::'+n for n in node_suffixes] if node_suffixes is not None else [str(test_file)])],
                   cwd=root, env=env, timeout=timeout)
    write_json(work/'process.json', proc)
    (work/'pytest_debug.log').write_text((proc.get('stdout') or '')+'\n'+(proc.get('stderr') or ''))
    try:
        report = json.loads(report_file.read_text())
    except (OSError, ValueError):
        report = {}
    tests = report.get('tests', [])
    passing = [t['nodeid'] for t in tests if t.get('outcome') == 'passed'
               and all(t.get(p, {}).get('outcome') == 'passed' for p in ('setup', 'call', 'teardown'))]
    collection_errors = sum(c.get('outcome') == 'failed' for c in report.get('collectors', []))
    all_pass = bool(tests and len(passing) == len(tests) and proc['returncode'] == 0
                    and not proc['timeout'] and not collection_errors and not report.get('summary', {}).get('errors', 0))
    status = ('timeout' if proc['timeout'] else 'report_error' if not report else
              'collection_error' if collection_errors or proc['returncode'] not in (0, 1, 5) else
              'no_tests' if not tests else 'passed' if all_pass else 'test_failure')
    line, branch = None, None
    coverage_status = 'not_measured: suite not all-pass'
    # Do not credit execution of failing tests as coverage of an accepted suite.
    if all_pass:
        cov_proc = command([sys.executable, '-m', 'coverage', 'json', '-o', str(work/'coverage.json')],
                           cwd=root, env=env, timeout=timeout)
        write_json(work/'coverage_process.json', cov_proc)
        try:
            data = json.loads((work/'coverage.json').read_text())
            totals = data['totals']
            if cov_proc['returncode'] or cov_proc['timeout'] or not data.get('files') or not totals['num_statements']:
                raise ValueError('No measured target statements')
            line = 100*totals['covered_lines']/totals['num_statements']
            branch = 100*totals['covered_branches']/totals['num_branches'] if totals['num_branches'] else None
            coverage_status = 'measured_module'
        except (OSError, ValueError, KeyError):
            coverage_status = 'coverage_error'
    result = dict(status=status, exit_code=proc['returncode'], timeout=proc['timeout'],
                  total_nodes=len(tests), collected=report.get('summary', {}).get('collected', 0),
                  collection_errors=collection_errors, passing_nodes=passing, pass_count=len(passing),
                  suite_pass=all_pass, line_pct=line, branch_pct=branch, coverage_status=coverage_status,
                  stdout=proc.get('stdout') or '', stderr=proc.get('stderr') or '')
    write_json(work/'evaluation.json', result)
    return result


def readiness(records, planned, mock=False):
    """Strict engineering gate, not a claim of oracle accuracy or generalization."""
    reasons = []
    if mock:
        reasons.append('mock is not GPU/quality evidence')
    if len(records) != planned:
        reasons.append('incomplete planned queue')
    for r in records:
        label = f"{r['target_id']}/{r['arm']}/{r['sample']}"
        if not r.get('suite_pass'):
            reasons.append(label+': suite not all-pass')
        if r.get('replay_status', 'not_run') == 'not_run':
            reasons.append(label+': replay not run')
        elif not r.get('stable'):
            reasons.append(label+': replay unstable')
        if r.get('line_pct') is None or r.get('line_pct', 0) <= 0:
            reasons.append(label+': no positive module coverage')
        if r.get('arm') == 'verified' and not r.get('setup_probe', {}).get('accepted'):
            reasons.append(label+': setup unresolved')
        audit = r.get('audit', {})
        if audit.get('is_hollow') or audit.get('tautological_assertions') or not audit.get('test_functions'):
            reasons.append(label+': syntactic quality gate failed')
        if r.get('repair_audit', {}).get('review_required'):
            reasons.append(label+': changed assertions require review')
        if r.get('status') != 'completed':
            reasons.append(label+': '+r.get('status', 'missing status'))
    harness_reasons = []
    if mock or planned < 1 or len(records) != planned:
        harness_reasons.append('mock or incomplete/nonpositive planned queue')
    for row in records:
        if row.get('status') not in ('completed', 'setup_unresolved', 'extraction_error'):
            harness_reasons.append(f"{row['target_id']}/{row['arm']}: {row.get('status')}")
        evaluation = row.get('final_evaluation', {})
        if evaluation.get('status') == 'report_error' or evaluation.get('coverage_status') == 'coverage_error':
            harness_reasons.append(f"{row['target_id']}/{row['arm']}: missing execution/coverage evidence")
    return dict(automated_ready=not reasons, generation_quality_ready=not reasons,
                harness_ready=not harness_reasons, harness_reasons=harness_reasons, reasons=reasons,
                semantic_review_required=True,
                scope='engineering screen only; no mutation/oracle/generalization claim')


def passing_subset_measurement(code, root, module, work, evaluation):
    """Secondary metric; never edits the suite or changes all-suite pass status."""
    suffixes = sorted(n.split('::', 1)[1] for n in evaluation['passing_nodes'])
    if not suffixes:
        return dict(status='no_eligible_tests', eligible=0, planned=evaluation['total_nodes'],
                    line_pct=None, branch_pct=None)
    if evaluation['status'] in ('timeout', 'collection_error', 'report_error'):
        return dict(status='original_incomplete', eligible=len(suffixes), planned=evaluation['total_nodes'],
                    line_pct=None, branch_pct=None)
    first = execute_pytest_and_coverage(code, root, module, Path(work)/'eligible_1', node_suffixes=suffixes)
    second = execute_pytest_and_coverage(code, root, module, Path(work)/'eligible_2', node_suffixes=suffixes)
    names = lambda r: sorted(n.split('::', 1)[1] for n in r['passing_nodes'])
    stable = (first['suite_pass'] and second['suite_pass'] and names(first) == suffixes == names(second)
              and first['line_pct'] is not None and first['line_pct'] == second['line_pct']
              and first['branch_pct'] == second['branch_pct'])
    return dict(status='stable' if stable else 'unstable_or_unmeasured',
                eligible=len(suffixes), planned=evaluation['total_nodes'],
                node_suffixes=suffixes, line_pct=first['line_pct'] if stable else None,
                branch_pct=first['branch_pct'] if stable else None,
                scope='secondary module coverage of original-passing nodes; full suite remains unchanged')
