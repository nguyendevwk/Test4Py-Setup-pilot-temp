"""Real subprocess checks of the development screen; no GPU/network/model data."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import council_multitarget as runner
from pilot.multitarget import (clean_code_block, execute_pytest_and_coverage,
                              inspect_api, probe_setup_candidate, readiness)


class ScriptedEngine:
    mock = False
    def __init__(self, *outputs):
        self.outputs = iter(outputs)
        self.roles = []
    def generate(self, role, *args, **kwargs):
        self.roles.append(role)
        return next(self.outputs)


class MultiTargetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base/'repo'
        self.root.mkdir()
        (self.root/'tinycase.py').write_text('''def choose(x: int):
    """Absolute value for nonzero integers; zero remains zero."""
    if x > 0:
        return x
    if x < 0:
        return -x
    return 0
''')
        self.target = dict(id='tiny', project='tiny', module='tinycase', file='tinycase.py',
                           symbol='choose', setup_hint='from tinycase import choose\nx = 1')
        self.good = 'from tinycase import choose\ndef test_positive():\n    assert choose(1) == 1\n'

    def execute(self, code, label='eval', module='tinycase', timeout=15):
        return execute_pytest_and_coverage(code, self.root, module, self.base/label, timeout)

    def sample(self, *outputs):
        engine = ScriptedEngine(*outputs)
        row = runner.run_single_evaluation(self.target, 'verified', 0, engine,
                                           self.root, self.base/'samples')
        return row, engine

    def test_diagnostic_then_unique_complete_module(self):
        raw = 'Error:\n```python\nImportError: bad import\n```\nFixed:\n```python\n'+self.good+'```'
        self.assertEqual(clean_code_block(raw), self.good)

    def test_ambiguous_incomplete_fragment_and_illegal_global_rejected(self):
        bad = ['```python\n'+self.good,
               '```python\n'+self.good+'```\n```python\n'+self.good+'```',
               'Timer.timers.clear()',
               'def test_bad():\n    print(1)\n    global print\n    assert True']
        for raw in bad:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                clean_code_block(raw)

    def test_collection_error_is_zero_nodes_and_missing_coverage(self):
        r = self.execute('from tinycase import Nonexistent\ndef test_x():\n    assert True')
        self.assertEqual(r['status'], 'collection_error')
        self.assertEqual(r['total_nodes'], 0)
        self.assertGreater(r['collection_errors'], 0)
        self.assertIsNone(r['line_pct'])
        self.assertIsNone(r['branch_pct'])

    def test_true_line_and_branch_percentages_from_raw_counts(self):
        r = self.execute(self.good)
        self.assertTrue(r['suite_pass'])
        totals = json.loads((self.base/'eval/coverage.json').read_text())['totals']
        self.assertAlmostEqual(r['line_pct'], 100*totals['covered_lines']/totals['num_statements'])
        self.assertAlmostEqual(r['branch_pct'], 100*totals['covered_branches']/totals['num_branches'])
        self.assertNotEqual(r['line_pct'], totals['percent_covered'])

    def test_no_branch_is_na_not_line_percentage(self):
        (self.root/'flatcase.py').write_text('def identity(x):\n    return x\n')
        r = self.execute('from flatcase import identity\ndef test_identity():\n    assert identity(1) == 1', module='flatcase')
        self.assertTrue(r['suite_pass'])
        self.assertIsNone(r['branch_pct'])

    def test_mixed_suite_stays_failed_and_is_not_pruned(self):
        mixed = self.good+'\ndef test_negative():\n    assert choose(-1) == -1\n'
        row, engine = self.sample(mixed, mixed)
        self.assertEqual(engine.roles, ['coder', 'critic'])
        self.assertTrue(row['repair_attempted'])
        self.assertFalse(row['suite_pass'])
        self.assertEqual(row['pass_count'], 1)
        self.assertEqual(row['total_count'], 2)
        self.assertIsNone(row['line_pct'])
        self.assertIn('test_negative', (self.base/'samples/sample_01/test_final.py').read_text())

    def test_import_repair_preserves_test_and_raw_evidence(self):
        broken = self.good.replace('import choose', 'import choose, Missing')
        row, _ = self.sample(broken, self.good)
        self.assertFalse(row['first_pass'])
        self.assertTrue(row['repaired_by_critic'])
        self.assertTrue(row['suite_pass'])
        self.assertTrue(row['stable'])
        self.assertEqual((self.base/'samples/sample_01/coder_raw.txt').read_text(), broken)
        self.assertTrue(readiness([row], 1)['automated_ready'])

    def test_repair_cannot_delete_failed_test_to_get_all_pass(self):
        mixed = self.good+'\ndef test_negative():\n    assert choose(-1) == -1\n'
        row, _ = self.sample(mixed, self.good)
        self.assertFalse(row['repair_audit']['accepted'])
        self.assertFalse(row['suite_pass'])
        self.assertIn('repair_rejected', row)

    def test_changed_assertion_requires_review_even_if_passes(self):
        wrong = self.good.replace('== 1', '== 2')
        row, _ = self.sample(wrong, self.good)
        self.assertFalse(row['suite_pass'])
        self.assertIn('repair_rejected', row)
        self.assertTrue(row['repair_audit']['review_required'])
        self.assertFalse(readiness([row], 1)['automated_ready'])

    def test_extraction_failure_can_repair_but_requires_review(self):
        row, _ = self.sample('```python\nImportError: bad\n```', self.good)
        self.assertTrue(row['initial_extraction_error'])
        self.assertFalse(row['suite_pass'])
        self.assertFalse(readiness([row], 1)['automated_ready'])

    def test_invalid_critic_fragment_does_not_replace_initial_file(self):
        broken = self.good.replace('import choose', 'import choose, Missing')
        row, _ = self.sample(broken, '```python\nTimer.timers.clear()\n```')
        self.assertIn('repair_extraction_error', row)
        self.assertEqual((self.base/'samples/sample_01/test_final.py').read_text(), broken)

    def test_timeout_preserved_and_not_reported_zero_coverage(self):
        r = self.execute('import time\ndef test_wait():\n    time.sleep(30)\n    assert True', timeout=1)
        self.assertTrue(r['timeout'])
        self.assertEqual(r['status'], 'timeout')
        self.assertIsNone(r['line_pct'])
        self.assertTrue((self.base/'eval/process.json').exists())

    def test_setup_and_api_resolve_checkout_in_fresh_process(self):
        api = inspect_api(self.root, 'tinycase', 'choose')
        self.assertEqual(Path(api['file']).parent, self.root)
        self.assertIn('x: int', api['signature'])
        self.assertTrue(probe_setup_candidate(self.target['setup_hint'], self.root)['accepted'])
        self.assertFalse(probe_setup_candidate('from tinycase import Missing', self.root)['accepted'])

    def test_no_tests_cannot_be_success(self):
        r = self.execute('x = 1')
        self.assertFalse(r['suite_pass'])
        self.assertEqual(r['total_nodes'], 0)

    def test_product_source_modification_rejects_score(self):
        evil = self.good+"\nfrom pathlib import Path\nPath(__import__('tinycase').__file__).write_text('changed')\n"
        row, _ = self.sample(evil)
        self.assertEqual(row['status'], 'product_modified')
        self.assertFalse(row['suite_pass'])
        self.assertIsNone(row['line_pct'])

    def test_execution_exception_still_writes_result(self):
        with patch.object(runner, 'inspect_api', side_effect=RuntimeError('preflight error')):
            row, _ = self.sample(self.good)
        self.assertEqual(row['status'], 'execution_error')
        self.assertTrue((self.base/'samples/sample_01/result.json').exists())

    def test_mock_queue_complete_offline_and_never_ready(self):
        out = self.base/'mock'
        p = subprocess.run([sys.executable, str(runner.BASE_DIR/'council_multitarget.py'),
                            '--mock', '--output', str(out)], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        summary = json.loads((out/'summary.json').read_text())
        self.assertEqual(summary['planned'], 8)
        self.assertEqual(summary['finished'], 8)
        self.assertFalse(json.loads((out/'readiness.json').read_text())['automated_ready'])
        self.assertTrue(all(r['line_pct'] is None and not r['suite_pass'] for r in summary['records']))
        self.assertTrue(out.with_suffix('.zip').exists())

    def test_engine_load_failure_retains_every_planned_row_and_archive(self):
        out = self.base/'engine_failure'
        argv = ['council_multitarget.py', '--mock', '--output', str(out)]
        with patch.object(sys, 'argv', argv), patch.object(runner, 'DualGPUBenchmarkEngine', side_effect=RuntimeError('load failed')):
            self.assertEqual(runner.main(), 2)
        summary = json.loads((out/'summary.json').read_text())
        self.assertEqual(summary['finished'], summary['planned'])
        self.assertEqual(summary['finished'], 8)
        self.assertTrue(all(r['status'] == 'preflight_or_engine_error' for r in summary['records']))
        self.assertTrue(out.with_suffix('.zip').exists())

    def test_setup_failure_is_explicit_not_fallback_to_baseline(self):
        self.target['setup_hint'] = 'from tinycase import Missing'
        row, engine = self.sample(self.good)
        self.assertEqual(row['status'], 'setup_unresolved')
        self.assertEqual(engine.roles, [])
        self.assertFalse(readiness([row], 1)['automated_ready'])

    def test_replay_instability_blocks_readiness(self):
        # Process-local state changes only in the test-output directory; fixture
        # demonstrates why a single all-pass execution cannot establish stability.
        marker = self.base/'once'
        code = self.good + f"\nfrom pathlib import Path\ndef test_once():\n    marker = Path({str(marker)!r})\n    assert not marker.exists()\n    marker.touch()\n"
        row, _ = self.sample(code)
        self.assertTrue(row['suite_pass'])
        self.assertFalse(row['stable'])
        self.assertFalse(readiness([row], 1)['automated_ready'])

    def test_hollow_tests_do_not_pass_readiness(self):
        code = 'from tinycase import choose\ndef test_hollow():\n    choose(1)\n    assert True\n'
        row, _ = self.sample(code)
        self.assertTrue(row['suite_pass'])
        self.assertFalse(readiness([row], 1)['automated_ready'])

    def test_notebook_cells_compile(self):
        notebook = json.loads((runner.BASE_DIR/'notebooks/kaggle_multitarget_smoke_v4.ipynb').read_text())
        for i, cell in enumerate(notebook['cells']):
            if cell['cell_type'] == 'code':
                compile(''.join(cell['source']), f'notebook-cell-{i}', 'exec')

    def test_mixed_suite_has_separate_stable_subset_without_pass_credit(self):
        mixed = self.good+'\ndef test_bad():\n    assert choose(-2) == -2\n'
        row, _ = self.sample(mixed, mixed)
        self.assertFalse(row['suite_pass'])
        self.assertEqual(row['replay_status'], 'not_run')
        self.assertEqual(row['passing_subset']['eligible'], 1)
        self.assertEqual(row['passing_subset']['planned'], 2)
        self.assertEqual(row['passing_subset']['status'], 'stable')
        self.assertGreater(row['passing_subset']['line_pct'], 0)
        self.assertIsNone(row['line_pct'])
        self.assertFalse(readiness([row], 1)['automated_ready'])

    def test_subset_replay_failure_has_no_coverage_credit(self):
        from pilot.multitarget import passing_subset_measurement
        marker = self.base/'subset_once'
        code = self.good+f"\nfrom pathlib import Path\ndef test_once():\n    p=Path({str(marker)!r})\n    assert not p.exists()\n    p.touch()\n"
        evaluated = self.execute(code)
        measured = passing_subset_measurement(code, self.root, 'tinycase', self.base/'subset', evaluated)
        self.assertEqual(measured['status'], 'unstable_or_unmeasured')
        self.assertIsNone(measured['line_pct'])

    def test_replay_not_run_is_not_mislabeled_as_unstable(self):
        mixed = self.good+'\ndef test_bad():\n    assert False\n'
        row, _ = self.sample(mixed, mixed)
        reasons = readiness([row], 1)['reasons']
        self.assertTrue(any('replay not run' in r for r in reasons))
        self.assertFalse(any('replay unstable' in r for r in reasons))

    def test_self_repair_keeps_initial_raw_and_is_not_critic_credit(self):
        broken = self.good.replace('import choose', 'import choose, Missing')
        engine = ScriptedEngine(broken, self.good)
        row = runner.run_single_evaluation(self.target, 'grounded', 0, engine,
                                          self.root, self.base/'selfrepair', repair_with='coder')
        self.assertTrue(row['suite_pass'])
        self.assertFalse(row['repaired_by_critic'])
        self.assertEqual(engine.roles, ['coder', 'coder'])
        self.assertEqual((self.base/'selfrepair/sample_01/coder_raw.txt').read_text(), broken)
        self.assertEqual((self.base/'selfrepair/sample_01/repair_raw.txt').read_text(), self.good)

    def test_generic_return_type_and_relative_import_grounding(self):
        from pilot.grounding import dependency_context
        package = self.root/'src'/'unrelatedpkg'
        package.mkdir(parents=True)
        (package/'__init__.py').write_text('')
        (package/'model.py').write_text('class Outcome:\n    @property\n    def valid(self):\n        return True\n')
        (package/'api.py').write_text('from .model import Outcome\ndef make() -> Outcome:\n    return Outcome()\n')
        d = dependency_context(self.root, 'src/unrelatedpkg/api.py', 'make')
        self.assertEqual([n['symbol'] for n in d['snippets']], ['Outcome'])
        self.assertIn('def valid', d['snippets'][0]['source'])
        self.assertNotIn('test_', json.dumps(d))
        small = dependency_context(self.root, 'src/unrelatedpkg/api.py', 'make', max_chars=5)
        self.assertEqual(small['snippets'], [])
        self.assertTrue(small['omitted'])

    def test_invocation_witness_checks_target_entry_not_just_setup(self):
        from pilot.grounding import verify_target_invocation
        good = verify_target_invocation('value = 4', self.root, 'tinycase', 'choose')
        self.assertTrue(good['accepted'])
        self.assertIn('_target(x=value)', good['invocation'])
        compile(good['invocation'], '<witness>', 'exec')
        bad = verify_target_invocation('value = None', self.root, 'tinycase', 'choose')
        self.assertFalse(bad['accepted'])
        # A setup that imports a callable but supplies no required argument is insufficient.
        empty = verify_target_invocation('from tinycase import choose', self.root, 'tinycase', 'choose')
        self.assertFalse(empty['accepted'])

    def test_constructor_witness_scope_is_explicit(self):
        from pilot.grounding import verify_target_invocation
        (self.root/'widget.py').write_text('class Widget:\n    def __init__(self):\n        self.ready = False\n    def activate(self):\n        self.ready = True\n')
        result = verify_target_invocation('from widget import Widget\nw = Widget()', self.root, 'widget', 'Widget')
        self.assertTrue(result['accepted'])
        self.assertIn('constructor', result['scope'])
        self.assertIn('no method-state guarantee', result['scope'])

    def test_input_token_budget_rejects_before_model_inference(self):
        # Fake tokenizer measures a deliberately oversized context; no weights are used.
        import types
        engine = object.__new__(runner.DualGPUBenchmarkEngine)
        engine.mock = False
        engine.max_input_tokens = 2
        engine.coder_tokenizer = types.SimpleNamespace(apply_chat_template=lambda *a, **k: [1,2,3])
        fake_torch = types.SimpleNamespace(manual_seed=lambda seed: None)
        with patch.dict(sys.modules, {'torch': fake_torch}), self.assertRaisesRegex(ValueError, 'no silent truncation'):
            engine.generate('coder', 'system', 'context')

    def test_external_benchmark_frame_requires_pins_and_production_paths(self):
        from pilot.grounding import load_target_spec
        spec = self.base/'frame.json'
        target = dict(self.target, repo_url='https://example.invalid/repo.git', commit='a'*40)
        spec.write_text(json.dumps(dict(targets=[target])))
        self.assertEqual(load_target_spec(spec)[0]['id'], 'tiny')
        for invalid in [dict(target, commit='main'), dict(target, file='../escape.py'),
                        dict(target, file='tests/test_example.py'), dict(target, project='../escape')]:
            spec.write_text(json.dumps([invalid]))
            with self.assertRaises(ValueError):
                load_target_spec(spec)

    def test_qualified_method_resolves_source_and_invocation(self):
        from pilot.grounding import dependency_context, verify_target_invocation
        (self.root/'machine.py').write_text('class Machine:\n    def __init__(self):\n        self.active = False\n    def enable(self):\n        self.active = True\n    def read(self):\n        return self.active\n')
        info = runner.extract_target_source(self.root/'machine.py', 'Machine.read')
        self.assertIn('def read', info['source'])
        self.assertEqual(info['parent_class'], 'Machine')
        api = inspect_api(self.root, 'machine', 'Machine.read')
        self.assertEqual(api['signature'], '(self)')
        d = dependency_context(self.root, 'machine.py', 'Machine.read')
        self.assertIn('def __init__', d['snippets'][0]['source'])
        witness = verify_target_invocation('from machine import Machine\nw = Machine()\nw.enable()', self.root, 'machine', 'Machine.read')
        self.assertTrue(witness['accepted'])
        self.assertIn('.Machine.read', witness['invocation'])
        compile(witness['invocation'], '<method-witness>', 'exec')

    def test_probe_does_not_export_observed_return_values(self):
        from pilot.grounding import verify_target_invocation
        (self.root/'oraclecase.py').write_text('def action(x):\n    return "secret_observed_value"\n')
        witness = verify_target_invocation('value=1', self.root, 'oraclecase', 'action')
        self.assertTrue(witness['accepted'])
        self.assertNotIn('secret_observed_value', json.dumps(witness))

    def test_dependency_grounding_ablation_does_not_use_test_sources(self):
        (self.root/'models.py').write_text('class Result:\n    valid=True\n')
        (self.root/'tinycase.py').write_text('from models import Result\ndef choose(x: int) -> Result:\n    return Result()\n')
        good = 'from tinycase import choose\ndef test_result():\n    assert choose(1).valid\n'
        (self.root/'test_secret.py').write_text('EXPECTED_ANSWER = 123456789')
        for arm in ['baseline', 'grounded']:
            row = runner.run_single_evaluation(self.target, arm, 0, ScriptedEngine(good), self.root, self.base/arm)
            context = json.loads((self.base/arm/'sample_01/context.json').read_text())
            self.assertNotIn('EXPECTED_ANSWER', context['context'])
            self.assertEqual('class Result' in context['context'], arm == 'grounded')
            self.assertTrue(row['suite_pass'])

    def test_gate_separates_execution_integrity_from_generation_quality(self):
        # Synthetic metadata, not measured benchmark results.
        row = dict(target_id='fixture', arm='baseline', sample='sample_01', status='completed',
                   suite_pass=False, stable=False, replay_status='not_run', line_pct=None,
                   final_evaluation=dict(status='test_failure'))
        gate = readiness([row], 1)
        self.assertTrue(gate['harness_ready'])
        self.assertFalse(gate['automated_ready'])
        self.assertFalse(gate['generation_quality_ready'])
        row['status'] = 'product_modified'
        self.assertFalse(readiness([row], 1)['harness_ready'])

    def test_missing_target_is_explicit_not_source_fallback(self):
        with self.assertRaises(ValueError):
            runner.extract_target_source(self.root/'tinycase.py', 'unknown')

    def test_unknown_target_rejected_before_model_load(self):
        p = subprocess.run([sys.executable, str(runner.BASE_DIR/'council_multitarget.py'),
                            '--targets', 'typo', '--output', str(self.base/'invalid')], capture_output=True)
        self.assertEqual(p.returncode, 2)
        self.assertFalse((self.base/'invalid').exists())


if __name__ == '__main__':
    unittest.main()
