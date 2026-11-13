"""Common original/branch/mutation scoring. Never supplies an oracle to the model."""
import ast
import copy
import json
import os
from pathlib import Path
import shutil
import sys

from pilot.common import append_json, command, digest, write_json


def classify(text):
    if any(s in text for s in ('SyntaxError', 'IndentationError', 'invalid syntax', 'E0001')):
        return 'generation'
    if any(s in text for s in ('ImportError', 'ModuleNotFoundError', 'E0401')):
        return 'import'
    if any(s in text for s in ('AssertionError', 'Failed: DID NOT RAISE')):
        return 'assertion'
    if any(s in text for s in ('AttributeError', 'KeyError', 'TypeError', 'ValueError')):
        return 'setup'
    return 'other'


def mutate(source):
    """Two fixed AST operators scoped to the returned loader of the pilot target."""
    tree = ast.parse(source)
    target, = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'get_custom_loader']
    calls = [n for n in ast.walk(target) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Attribute) and n.func.attr == 'set_filepath']
    if len(calls) != 1 or not calls[0].args:
        raise RuntimeError('Unsupported benchmark shape: expected one loader set_filepath call')
    first = copy.deepcopy(tree)
    first_target = next(n for n in first.body if isinstance(n, ast.FunctionDef) and n.name == target.name)
    call = next(n for n in ast.walk(first_target) if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Attribute) and n.func.attr == 'set_filepath')
    call.args[-1] = ast.Constant('pilot_wrong_path.py')
    second = copy.deepcopy(tree)
    second_target = next(n for n in second.body if isinstance(n, ast.FunctionDef) and n.name == target.name)
    call2 = next(n for n in ast.walk(second_target) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Attribute) and n.func.attr == 'set_filepath')
    parents = {child: node for node in ast.walk(second_target) for child in ast.iter_child_nodes(node)}
    branch = call2
    while branch in parents and not isinstance(branch, ast.If):
        branch = parents[branch]
    if not isinstance(branch, ast.If):
        raise RuntimeError('Unsupported benchmark shape: filepath assignment must be conditional')
    parent = parents[branch]
    inserted = False
    # Retain original branch, then unconditionally update path. This changes only
    # preservation of an existing destination's filepath.
    for _, value in ast.iter_fields(parent):
        if isinstance(value, list) and branch in value:
            value.insert(value.index(branch) + 1, ast.Expr(copy.deepcopy(call2)))
            inserted = True
            break
    if not inserted:
        raise RuntimeError('Cannot insert existing-path mutant')
    result = {}
    for name, mutant in [('new_path_wrong', first), ('existing_path_overwritten', second)]:
        ast.fix_missing_locations(mutant)
        text = ast.unparse(mutant) + '\n'
        compile(text, name, 'exec')
        result[name] = dict(source=text, sha256=digest(text),
                            description='wrong new destination filepath' if name == 'new_path_wrong'
                            else 'overwrite old filepath even when destination exists')
    return result


def pytest_run(root, work, label, nodes, timeout, coverage=False):
    artifact = Path(work) / label
    artifact.mkdir(parents=True, exist_ok=False)
    report = artifact / 'pytest.json'
    env = dict(os.environ, PYTHONPATH=str(root), PYTHONDONTWRITEBYTECODE='1',
               PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', COVERAGE_FILE=str(artifact / '.coverage'))
    args = [sys.executable, '-m']
    if coverage:
        args += ['coverage', 'run', '--branch', '--source=pycg.machinery', '-m']
    args += ['pytest', '-p', 'pytest_jsonreport.plugin', '-o', 'addopts=',
             '--json-report', f'--json-report-file={report}', *nodes]
    process = command(args, cwd=root, timeout=timeout, env=env)
    write_json(artifact / 'process.json', process)
    data = json.loads(report.read_text()) if report.exists() else {}
    if coverage:
        cov_process = command([sys.executable, '-m', 'coverage', 'json', '-o', artifact / 'coverage.json'],
                              cwd=root, timeout=timeout, env=env)
        write_json(artifact / 'coverage_process.json', cov_process)
    return process, data, artifact


def passed_nodes(report):
    return [row['nodeid'] for row in report.get('tests', []) if row.get('outcome') == 'passed'
            and row.get('call', {}).get('outcome') == 'passed']


def mutant_verdict(process, report, eligible):
    if process['timeout']:
        return 'timeout_inconclusive'
    tests = {row['nodeid']: row for row in report.get('tests', [])}
    if process['returncode'] not in (0, 1) or set(tests) != set(eligible):
        return 'environment_error'
    for row in tests.values():
        if row.get('setup', {}).get('outcome') != 'passed' or row.get('teardown', {}).get('outcome') not in ('passed', None):
            return 'environment_error'
        if row.get('call', {}).get('outcome') not in ('passed', 'failed'):
            return 'environment_error'
        diagnostic = str(row.get('call', {}))
        if classify(diagnostic) == 'import':
            return 'environment_error'
        if row.get('call', {}).get('outcome') == 'failed' and not (
            classify(diagnostic) == 'assertion' or 'imports.py' in diagnostic
        ):
            return 'unattributed_failure'
    if any(row.get('call', {}).get('outcome') == 'failed' for row in tests.values()):
        return 'killed'
    return 'survived' if process['returncode'] == 0 else 'environment_error'


def score(root, work, config):
    root, work = Path(root).resolve(), Path(work).resolve()
    if root == work or root in work.parents:
        raise ValueError('Scoring output must be outside the source checkout')
    pool = mutate((root / 'pycg/machinery/imports.py').read_text())
    write_json(work / 'mutant_pool.json', pool)
    tests_dir = root / 'Test4DT_tests'
    if not list(tests_dir.glob('test_*.py')):
        result = dict(status='no_generated_tests', passed=0, mutation_score=None,
                      mutants=[dict(name=name, verdict='no_eligible_tests') for name in pool],
                      mutant_pool_hash=digest(pool), branch_coverage=None)
        write_json(work / 'score.json', result)
        return result
    process, report, artifact = pytest_run(root, work, 'original', ['Test4DT_tests'], config['score_timeout'])
    eligible = passed_nodes(report)
    result = dict(status='scored', original_process=process,
                  original_summary=report.get('summary'), eligible_nodeids=eligible,
                  passed=len(eligible), errors=[], mutants=[], branch_coverage=None,
                  mutation_score=None, mutant_pool_hash=digest(pool))
    for row in report.get('tests', []):
        if row.get('outcome') != 'passed':
            result['errors'].append(dict(nodeid=row['nodeid'], category=classify(str(row))))
    if process['timeout'] or process['returncode'] not in (0, 1) or not report:
        result['status'] = 'original_environment_error'
    write_json(work / 'score.json', result)
    if eligible:
        # Replay only original-passing tests for BOTH coverage and mutants.
        replay, replay_report, cov_dir = pytest_run(root, work, 'eligible_original', eligible,
                                                    config['score_timeout'], coverage=True)
        if replay['returncode'] != 0 or set(passed_nodes(replay_report)) != set(eligible):
            result['status'] = 'unstable_original'
            write_json(work / 'score.json', result)
            return result
        cov_file = cov_dir / 'coverage.json'
        if cov_file.exists():
            cov = json.loads(cov_file.read_text())
            record = cov.get('files', {}).get('pycg/machinery/imports.py', {})
            result['branch_coverage'] = dict(module=record.get('summary'),
                                             functions=record.get('functions'))
        else:
            result['status'] = 'coverage_environment_error'
        for name, mutant in pool.items():
            mutant_root = work / 'mutants' / name / 'PyCG'
            shutil.copytree(root, mutant_root, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
            (mutant_root / 'pycg/machinery/imports.py').write_text(mutant['source'])
            proc, data, _ = pytest_run(mutant_root, work, f'mutant_{name}', eligible, config['score_timeout'])
            result['mutants'].append(dict(name=name, sha256=mutant['sha256'],
                                           verdict=mutant_verdict(proc, data, eligible),
                                           process=proc, tests=data.get('tests', [])))
            write_json(work / 'score.json', result)
        # The fixed denominator is two; unresolved mutants do not silently vanish.
        if all(m['verdict'] in ('killed', 'survived') for m in result['mutants']):
            result['mutation_score'] = sum(m['verdict'] == 'killed' for m in result['mutants']) / 2
    if not eligible:
        result['mutants'] = [dict(name=name, verdict='no_eligible_tests') for name in pool]
    write_json(work / 'score.json', result)
    return result
