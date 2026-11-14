"""Offline regression checks for scientific reporting contracts."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch, MagicMock

from council.critic import clean_code_block, audit_test_quality
from council.engine import CouncilEngine
from council.runner import branch_percentage, suite_all_pass, repair_audit, run_council_pipeline, run_sample
from ablation_runner import compile_ablation_reports
from pilot.common import BASE, write_json


def passed_report():
    row = dict(nodeid='Test4DT_tests/test_generated.py::test_ok', outcome='passed',
               setup=dict(outcome='passed'), call=dict(outcome='passed'), teardown=dict(outcome='passed'))
    return dict(tests=[row], summary=dict(total=1, passed=1))


def args(output, **kwargs):
    values = dict(samples=1, mode='baseline', coder_model='mock-coder', critic_model='mock-critic',
        no_repair=False, max_new_tokens=512, mock=True, output=output, seed=42)
    values.update(kwargs)
    return SimpleNamespace(**values)


class CouncilTests(unittest.TestCase):
    def test_parse_complete_and_reject_ambiguous(self):
        self.assertEqual(clean_code_block('<think>reason</think>\n```python\ndef test_x():\n    assert 2 == 2\n```'),
                         'def test_x():\n    assert 2 == 2')
        for raw in ('<think>incomplete', '```python\na=1\n```\n```python\nb=2\n```', '```python\na=1'):
            with self.assertRaises(ValueError):
                clean_code_block(raw)

    def test_syntactic_quality_never_claims_semantics(self):
        audit = audit_test_quality('def test_x():\n    assert True\n')
        self.assertTrue(audit['is_hollow'])
        self.assertEqual(audit['tautological_assertions'], 1)
        self.assertIsNone(audit['semantic_assertion_accuracy'])
        self.assertFalse(audit_test_quality('def test_x():\n    with pytest.raises(ValueError):\n        f()')['is_hollow'])

    def test_suite_requires_every_node_every_phase(self):
        report = passed_report()
        proc = dict(returncode=0, timeout=False)
        self.assertTrue(suite_all_pass(proc, report))
        self.assertFalse(suite_all_pass(dict(returncode=0, timeout=True), report))
        self.assertFalse(suite_all_pass(proc, {}))
        for phase in ('setup', 'call', 'teardown'):
            bad = copy.deepcopy(report)
            bad['tests'][0][phase]['outcome'] = 'failed'
            self.assertFalse(suite_all_pass(proc, bad))
        mixed = copy.deepcopy(report)
        mixed['tests'].append(dict(nodeid='bad', outcome='failed', call=dict(outcome='failed')))
        self.assertFalse(suite_all_pass(dict(returncode=1), mixed))
        skipped = copy.deepcopy(report)
        skipped['tests'].append(dict(nodeid='skip', outcome='skipped'))
        self.assertFalse(suite_all_pass(proc, skipped))
        collection = copy.deepcopy(report)
        collection['collectors'] = [dict(outcome='failed')]
        self.assertFalse(suite_all_pass(proc, collection))

    def test_zero_coverage_is_not_missing(self):
        self.assertEqual(branch_percentage(dict(covered_branches=0, num_branches=10)), 0)
        self.assertEqual(branch_percentage(dict(covered_branches=8, num_branches=10)), 80)
        self.assertIsNone(branch_percentage(dict(covered_branches=0, num_branches=0)))
        self.assertIsNone(branch_percentage({}))

    def test_repair_cannot_drop_tests_checks_or_replace_with_true(self):
        before = 'def test_x():\n    assert f() == 1\n'
        for after in ('def test_x():\n    pass\n', 'def test_y():\n    assert f() == 1\n', 'def test_x():\n    assert True\n'):
            self.assertFalse(repair_audit(before, after)['accepted'])
        changed = repair_audit(before, 'def test_x():\n    assert f() == 2\n')
        self.assertTrue(changed['accepted'])
        self.assertTrue(changed['review_required'])
        self.assertIsNone(changed['semantic_preservation'])

    def test_syntax_repair_requires_review_and_valid_checks(self):
        repaired = repair_audit('def test_broken(:', 'def test_fixed():\n    assert f() == 1')
        self.assertTrue(repaired['accepted'])
        self.assertTrue(repaired['review_required'])
        self.assertFalse(repair_audit('def test_broken(:', 'def test_fixed():\n    pass')['accepted'])

    def test_mock_is_offline_and_never_scores(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)/'mock'
            with patch('council.runner.checkout') as checkout, patch('council.runner.score') as score:
                summary = run_council_pipeline(args(output))
            self.assertFalse(checkout.called)
            self.assertFalse(score.called)
            self.assertEqual(summary['run_kind'], 'mock')
            self.assertEqual(summary['passed_samples'], 0)
            self.assertIsNone(summary['results'][0]['suite_all_pass'])
            calls = [json.loads(line) for line in (output/'model_calls.jsonl').read_text().splitlines()]
            self.assertTrue(calls[0]['mock'])
            self.assertIsNone(calls[0]['output_tokens'])
            table = compile_ablation_reports(output)
            self.assertIn('mock/non-real output excluded', table)
            self.assertNotIn('100.0%', table)

    def test_engine_failure_preserves_planned_denominator(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch('council.runner.CouncilEngine', side_effect=RuntimeError('synthetic load failure')):
                summary = run_council_pipeline(args(Path(folder)/'failed', samples=3))
            self.assertEqual(summary['planned_samples'], 3)
            self.assertEqual(summary['samples'], 0)
            self.assertEqual(summary['status'], 'failed')
            self.assertTrue((Path(summary['output'])/'summary.json').exists())

    def run_synthetic_sample(self, folder, no_repair=False, score_status='scored', repair_code=None):
        product = folder/'product'
        product.mkdir()
        directory = folder/'sample'
        directory.mkdir()
        mixed = passed_report()
        bad = copy.deepcopy(mixed['tests'][0])
        bad.update(nodeid='Test4DT_tests/test_generated.py::test_bad', outcome='failed', call=dict(outcome='failed'))
        mixed['tests'].append(bad)
        initial = 'def test_ok():\n    assert f() == 1\ndef test_bad():\n    assert g() == 2\n'
        def scoring(root, work, settings):
            report = mixed if no_repair else passed_report()
            write_json(work/'original/pytest.json', report)
            return dict(status=score_status, passed=1, original_process=dict(returncode=1 if no_repair else 0),
                branch_coverage=dict(module=dict(covered_branches=0, num_branches=10)),
                mutation_score=0, mutant_pool_hash='fixed-pool',
                mutants=[dict(name='a', verdict='survived'), dict(name='b', verdict='survived')])
        settings = json.loads((BASE/'pilot.json').read_text())
        with patch('council.runner.source_context', return_value='source'), \
             patch('council.runner.generate_test_with_coder', return_value=initial), \
             patch('council.runner.pytest_run', side_effect=[(dict(returncode=1, timeout=False, stdout='failed', stderr='warning'), mixed, directory),
                 (dict(returncode=0, timeout=False), passed_report(), directory)]), \
             patch('council.runner.repair_with_critic', return_value=repair_code or initial) as repair, \
             patch('council.runner.score', side_effect=scoring):
            row = run_sample(args(folder, no_repair=no_repair), CouncilEngine(mock=True), product, directory, settings)
        return row, repair

    def test_partial_failure_is_not_success(self):
        with tempfile.TemporaryDirectory() as folder:
            row, repair = self.run_synthetic_sample(Path(folder), no_repair=True)
        self.assertFalse(repair.called)
        self.assertEqual(row['status'], 'failed')
        self.assertFalse(row['suite_all_pass'])
        self.assertEqual(row['branch_pct'], 0)
        self.assertTrue(row['any_passing_tests'])

    def test_partial_failure_gets_repair_and_final_audit(self):
        with tempfile.TemporaryDirectory() as folder:
            row, repair = self.run_synthetic_sample(Path(folder))
        self.assertTrue(repair.called)
        self.assertFalse(row['first_pass'])
        self.assertTrue(row['suite_all_pass'])
        self.assertTrue(row['repaired_by_critic'])
        self.assertEqual(row['branch_pct'], 0)
        self.assertIn('audit', row)

    def test_unstable_scoring_cannot_become_success(self):
        with tempfile.TemporaryDirectory() as folder:
            row, _ = self.run_synthetic_sample(Path(folder), score_status='unstable_original')
        self.assertFalse(row['suite_all_pass'])
        self.assertEqual(row['status'], 'scoring_error')
        self.assertIsNone(row['mutation_score'])
        self.assertIsNone(row['branch_pct'])

    def test_incomplete_setup_never_reaches_generator(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); (root/'product').mkdir(); (root/'sample').mkdir()
            with patch('council.runner.extract', return_value={}), \
                 patch('council.runner.select', return_value=('', dict(complete=False))), \
                 patch('council.runner.generate_test_with_coder') as generate:
                row = run_sample(args(root, mode='council'), CouncilEngine(mock=True), root/'product', root/'sample', {})
            self.assertFalse(generate.called)
            self.assertEqual(row['status'], 'setup_incomplete')
            self.assertTrue((root/'sample/result.json').exists())

    def test_aggregation_keeps_zero_n_and_exposes_legacy_corrupt(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            data = dict(schema_version=2, mock=False, run_kind='real', cohort='cohort-a', planned_samples=3,
                status='complete', coder_model='synthetic', results=[
                    dict(scoring_complete=True, branch_pct=0, mutation_score=0, mutant_pool_hash='same', suite_all_pass=True),
                    dict(scoring_complete=True, branch_pct=80, mutation_score=1, mutant_pool_hash='same', suite_all_pass=True),
                    dict(status='execution_error', suite_all_pass=False)])
            write_json(root/'real/summary.json', data)
            write_json(root/'legacy/summary.json', dict(samples=10, passed_samples=10))
            (root/'corrupt').mkdir(); (root/'corrupt/summary.json').write_text('{')
            table = compile_ablation_reports(root)
            self.assertIn('40.00 (2/3)', table)
            self.assertIn('0.50 (2/3)', table)
            self.assertIn('2/3', table)
            self.assertIn('legacy/unsupported', table)
            self.assertIn('corrupt/summary.json', table)

    def test_model_and_tokenizer_share_resolved_revision_no_unused_critic(self):
        import sys
        torch = SimpleNamespace(__version__='stub', version=SimpleNamespace(cuda=None),
            manual_seed=MagicMock(), cuda=SimpleNamespace(device_count=lambda: 0), float32='fp32')
        tokenizer = MagicMock()
        model = MagicMock()
        transformers = SimpleNamespace(__version__='stub', AutoTokenizer=tokenizer, AutoModelForCausalLM=model)
        api = MagicMock()
        api.return_value.model_info.return_value.sha = 'immutable-sha'
        with patch.dict(sys.modules, dict(torch=torch, transformers=transformers,
                        huggingface_hub=SimpleNamespace(HfApi=api))):
            engine = CouncilEngine(coder_model='coder', critic_model='critic', enable_critic=False)
        self.assertEqual(tokenizer.from_pretrained.call_count, 1)
        self.assertEqual(model.from_pretrained.call_count, 1)
        self.assertEqual(tokenizer.from_pretrained.call_args.kwargs['revision'], 'immutable-sha')
        self.assertEqual(model.from_pretrained.call_args.kwargs['revision'], 'immutable-sha')
        self.assertEqual(set(engine.versions['models']), {'coder'})

    def test_product_mutation_rejects_scoring(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); product = root/'product'; directory = root/'sample'
            (product/'pycg').mkdir(parents=True); directory.mkdir()
            (product/'pycg/source.py').write_text('value = 1')
            def execute(repo, *unused):
                (repo/'pycg/source.py').write_text('value = 2')
                return dict(returncode=0), passed_report(), directory
            with patch('council.runner.source_context', return_value='source'), \
                 patch('council.runner.generate_test_with_coder', return_value='def test_ok():\n    assert f() == 1'), \
                 patch('council.runner.pytest_run', side_effect=execute), \
                 patch('council.runner.score') as scorer:
                row = run_sample(args(root, no_repair=True), CouncilEngine(mock=True), product, directory,
                                 json.loads((BASE/'pilot.json').read_text()))
            self.assertFalse(scorer.called)
            self.assertEqual(row['status'], 'execution_error')
            self.assertIn('Product source changed', row['error'])
            self.assertIsNone(row['mutation_score'])

    def test_ranked_control_uses_no_probe_and_caller_is_deduplicated(self):
        from pilot.setup import select
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            candidates = [dict(id=str(i), scenario=scenario, operations=ops, code='example')
                          for i, ops in enumerate([[], ['a'], ['a', 'b']])
                          for scenario in ('new_target', 'existing_target')]
            extraction = dict(candidate_hash='pool', candidates=candidates, evidence=[
                dict(file='source.py', line=line, owner_line=10, snippet='def owner(): pass', operation='create_node')
                for line in (11, 12)])
            with patch('pilot.setup.probe_one') as probe:
                _, selection = select(root, extraction, 'ranked', root, dict(max_probes=10))
            self.assertFalse(probe.called)
            self.assertEqual(set(selection['selected'].values()), {'2'})
            self.assertEqual(selection['probes'], 0)
            context, _ = select(root, extraction, 'caller', root, dict(max_probes=10))
            self.assertEqual(context.count('def owner(): pass'), 1)



if __name__ == '__main__':
    unittest.main()
