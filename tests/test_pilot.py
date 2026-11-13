"""Offline contract tests use a labeled miniature fixture, never benchmark results."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from pilot.common import BASE, checkout, command
from pilot.scoring import classify, mutate, mutant_verdict, passed_nodes
from pilot.setup import extract, probe_one, select

FIXTURE = '''import os
class ImportManager:
    def __init__(self):
        self.current_module = None
        self.nodes = {}
    def set_current_mod(self, name, path):
        self.current_module = name
    def create_node(self, name):
        self.nodes.setdefault(name, {})
    def get_node(self, name):
        return self.nodes.get(name, None)
    def set_filepath(self, name, path):
        self.nodes[name]['path'] = os.path.abspath(path)
    def get_filepath(self, name):
        return self.nodes[name]['path']
def get_custom_loader(import_manager):
    class Loader:
        def __init__(self, fullname, path):
            if import_manager.current_module not in import_manager.nodes:
                raise KeyError('source')
            if fullname not in import_manager.nodes:
                import_manager.create_node(fullname)
                import_manager.set_filepath(fullname, path)
    return Loader
'''
CALLER = '''def caller(self):
    self.import_manager.set_current_mod(self.modname, self.filename)
    self.import_manager.create_node(self.modname)
'''


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        package = self.root / 'pycg/machinery'
        package.mkdir(parents=True)
        (self.root / 'pycg/__init__.py').touch()
        (package / '__init__.py').touch()
        # Give graph nodes truthy metadata, matching the probe's precondition.
        self.source = FIXTURE.replace("self.nodes.setdefault(name, {})", "self.nodes.setdefault(name, {'name': name})")
        (package / 'imports.py').write_text(self.source)
        (self.root / 'pycg/caller.py').write_text(CALLER)
        tests = self.root / 'pycg/tests'
        tests.mkdir()
        (tests / 'test_poison.py').write_text('not valid python; MUST NEVER READ')
        self.config = dict(max_probes=10, probe_timeout=2)

    def tearDown(self):
        self.temp.cleanup()

    def test_deterministic_list_and_selection(self):
        extraction = extract(self.root)
        self.assertEqual(extraction['candidate_hash'], extract(self.root)['candidate_hash'])
        self.assertEqual(len(extraction['candidates']), 10)
        self.assertTrue(all(e['file'] == 'pycg/caller.py' and e['line'] in (2, 3)
                            for e in extraction['evidence']))
        a = self.root / 'a'; a.mkdir()
        b = self.root / 'b'; b.mkdir()
        _, extracted = select(self.root, extraction, 'extracted', a, self.config)
        context, verified = select(self.root, extraction, 'verified', b, self.config)
        self.assertTrue(verified['complete'])
        self.assertEqual(verified['probes'], 8)
        self.assertNotEqual(extracted['selected'], verified['selected'])
        self.assertNotIn('filepath=', context)
        self.assertNotIn('accepted', context)
        self.assertNotIn('assert ', context)
        logs = [json.loads(x) for x in (b / 'probes.jsonl').read_text().splitlines()]
        self.assertEqual(sum(row['accepted'] for row in logs), 2)

    def test_budget_and_timeout(self):
        candidate = extract(self.root)['candidates'][0]
        candidate['code'] = 'while True: pass'
        result = probe_one(self.root, candidate, .1)
        self.assertFalse(result['accepted'])
        self.assertEqual(result['reason'], 'timeout')
        work = self.root / 'limited'; work.mkdir()
        _, selection = select(self.root, extract(self.root), 'verified', work,
                              dict(max_probes=1, probe_timeout=2))
        self.assertFalse(selection['complete'])
        self.assertEqual(selection['probes'], 1)

    def test_mutants_change_only_intended_path_behavior(self):
        pool = mutate(self.source)
        for name, item in pool.items():
            scope = {}
            exec(item['source'], scope)
            manager = scope['ImportManager']()
            manager.set_current_mod('pkg.main', 'main.py')
            manager.create_node('pkg.main')
            if name == 'existing_path_overwritten':
                manager.create_node('pkg.dep'); manager.set_filepath('pkg.dep', 'old.py')
            scope['get_custom_loader'](manager)('pkg.dep', 'new.py')
            path = manager.get_filepath('pkg.dep')
            self.assertTrue(path.endswith('pilot_wrong_path.py' if name == 'new_path_wrong' else 'new.py'))
        self.assertEqual(pool, mutate(self.source))
        with self.assertRaises(RuntimeError):
            mutate('def get_custom_loader(x): return x')

    def test_mutant_verdict_and_original_filter(self):
        def row(outcome, phase='call'):
            value = dict(nodeid='t.py::test_x', outcome=outcome,
                         setup=dict(outcome='passed'), teardown=dict(outcome='passed'),
                         call=dict(outcome=outcome))
            value[phase] = dict(outcome=outcome, longrepr='AssertionError' if outcome == 'failed' else '')
            return value
        eligible = ['t.py::test_x']
        proc = dict(returncode=1, timeout=False)
        self.assertEqual(mutant_verdict(proc, dict(tests=[row('failed')]), eligible), 'killed')
        self.assertEqual(mutant_verdict(proc, dict(tests=[row('failed', 'setup')]), eligible), 'environment_error')
        self.assertEqual(mutant_verdict(proc, {}, eligible), 'environment_error')
        self.assertEqual(mutant_verdict(dict(returncode=0, timeout=True), {}, eligible), 'timeout_inconclusive')
        self.assertEqual(passed_nodes(dict(tests=[row('passed'), row('failed')])), eligible)
        self.assertEqual(classify('ModuleNotFoundError'), 'import')
        self.assertEqual(classify('AssertionError'), 'assertion')
        self.assertEqual(classify('AttributeError'), 'setup')
        self.assertEqual(classify('SyntaxError'), 'generation')

    def test_checkout_exact_commit_and_reject_mismatch(self):
        repo = self.root / 'repo'; repo.mkdir()
        def git(*args):
            return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()
        git('init', '-q')
        (repo / 'hello').write_text('fixture')
        git('add', 'hello')
        git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture')
        sha = git('rev-parse', 'HEAD')
        self.assertEqual(checkout(str(repo), sha, self.root / 'clone'), sha)
        with self.assertRaises(RuntimeError):
            checkout(str(repo), '0' * 40, self.root / 'bad_clone')

    def test_cli_no_dependencies_and_failure_report(self):
        proc = command([sys.executable, BASE / 'run.py', '--help'])
        self.assertEqual(proc['returncode'], 0)
        for mode in ('baseline', 'caller', 'extracted', 'verified', 'compare'):
            self.assertIn(mode, proc['stdout'])
        proc = command([sys.executable, BASE / 'run.py', '--rounds', '0'])
        self.assertEqual(proc['returncode'], 2)


    def test_compare_continues_after_failed_arm(self):
        import types
        from unittest.mock import patch
        import run
        output = self.root / 'experiment'
        fake_hub = types.SimpleNamespace(
            model_info=lambda *a, **kw: types.SimpleNamespace(sha='a' * 40),
            snapshot_download=lambda *a, **kw: str(self.root / 'embedding'))
        def fake_checkout(url, sha, destination):
            destination.mkdir(parents=True)
            if 'Test4Py' in url:
                package = destination / 'test4dt'
                package.mkdir()
                for name in ('message.py', 'testcase.py', 'gptapi.py', 'coverage_message.py'):
                    (package / name).write_text('# fixture')
            return sha
        invoked = []
        def fake_worker(args, **kwargs):
            mode = args[3]
            invoked.append(mode)
            failed = mode == 'caller'
            report = dict(status='failed' if failed else 'complete', input_tokens=1,
                          output_tokens=2, score={}, stages={})
            (Path(args[2]).parent / 'report.json').write_text(json.dumps(report))
            return dict(returncode=int(failed), timeout=False, stdout='', stderr='', seconds=0)
        with patch.object(sys, 'argv', ['run.py', '--output', str(output)]), \
             patch.dict(sys.modules, {'huggingface_hub': fake_hub}), \
             patch.object(run, 'checkout', fake_checkout), patch.object(run, 'command', fake_worker):
            self.assertEqual(run.main(), 1)
        self.assertEqual(invoked, ['baseline', 'caller', 'extracted', 'verified'])
        comparison = json.loads((output / 'comparison.json').read_text())
        self.assertEqual(comparison['status'], 'partial_failure')
        self.assertTrue((output / 'caller/process.json').exists())

    def test_score_only_passed_original_and_same_pool(self):
        from unittest.mock import patch
        from pilot.scoring import score
        tests = self.root / 'Test4DT_tests'; tests.mkdir()
        (tests / 'test_generated.py').write_text('def test_x(): pass')
        scoring_temp = tempfile.TemporaryDirectory()
        self.addCleanup(scoring_temp.cleanup)
        work = Path(scoring_temp.name)
        pass_id = 'Test4DT_tests/test_generated.py::test_pass'
        fail_id = 'Test4DT_tests/test_generated.py::test_fail'
        invoked = []
        def fake_run(root, work, label, nodes, timeout, coverage=False):
            invoked.append((label, nodes))
            artifact = Path(work) / label; artifact.mkdir()
            if label == 'original':
                return dict(returncode=1, timeout=False), dict(tests=[
                    dict(nodeid=pass_id, outcome='passed', call=dict(outcome='passed')),
                    dict(nodeid=fail_id, outcome='failed', call=dict(outcome='failed'))]), artifact
            tests_report = [dict(nodeid=pass_id, outcome='passed', call=dict(outcome='passed'),
                                  setup=dict(outcome='passed'), teardown=dict(outcome='passed'))]
            return dict(returncode=0, timeout=False), dict(tests=tests_report), artifact
        with patch('pilot.scoring.pytest_run', fake_run):
            result = score(self.root, work, dict(score_timeout=2))
        self.assertEqual(result['passed'], 1)
        self.assertEqual(result['mutation_score'], 0)
        for label, nodes in invoked[1:]:
            self.assertEqual(nodes, [pass_id])
        self.assertEqual(len(result['mutants']), 2)
        self.assertTrue((work / 'mutant_pool.json').exists())


if __name__ == '__main__':
    unittest.main()
