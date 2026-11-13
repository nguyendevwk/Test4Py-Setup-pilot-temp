"""Labeled synthetic artifacts validate analysis logic, never research results."""
import asyncio
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import analyze
from pilot.common import write_json


class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.settings=dict(mode='compare',model='fixture-model',model_revision='fixture-revision',embedding_revision='fixture-embedding',
            upstream='fixture-upstream',target_commit='fixture-target',target_module='fixture',target_function='get_custom_loader',
            generation=dict(do_sample=False),rounds=1,source_hashes={'fixture':'fixture'},seed=42)
        write_json(self.root/'experiment.json',self.settings)
        write_json(self.root/'comparison.json',dict(status='complete',validation_only=False))

    def tearDown(self):
        self.temp.cleanup()

    def arm(self, mode, **overrides):
        score=dict(status='scored',passed=2,mutation_score=.5,mutant_pool_hash='same-pool',branch_coverage={})
        report=dict(status='complete',settings=self.settings,score=score,worker_seconds=10,
                    versions=dict(python='fixture',packages={'fixture':'fixture'}))
        report.update(overrides)
        write_json(self.root/mode/'report.json',report)
        write_json(self.root/mode/'selection.json',dict(selected={'new_target':'x'},candidate_hash='same-candidates'))
        return report

    def test_validation_oracle_is_excluded(self):
        self.arm('verified')
        write_json(self.root/'comparison.json',dict(validation_only=True,status='complete'))
        rows, experiments, *_=analyze.collect(self.root)
        self.assertEqual(rows,[])
        self.assertTrue(experiments[0]['validation_only'])

    def test_missing_arms_and_failed_arms_are_not_zero_imputed(self):
        self.arm('baseline')
        self.arm('verified',status='failed',score={})
        rows,*_=analyze.collect(self.root)
        self.assertEqual(len(rows),4)
        missing=next(row for row in rows if row['mode']=='caller')
        self.assertIsNone(missing['passed'])
        self.assertIsNone(missing['mutation_score'])
        pairs=analyze.paired_rows(rows)
        self.assertFalse(any(pair['valid_pair'] for pair in pairs))

    def test_nested_coverage_unions_concrete_arcs(self):
        scopes={
            'get_custom_loader':dict(executed_branches=[[1,2]],missing_branches=[[1,3]],executed_lines=[1,2],missing_lines=[3]),
            'get_custom_loader.Loader.__init__':dict(executed_branches=[[1,2],[3,4]],missing_branches=[[3,5]],executed_lines=[2,4],missing_lines=[5]),
            'irrelevant':dict(executed_branches=[[100,101]],missing_branches=[],executed_lines=[100],missing_lines=[])}
        result=analyze.scoped_coverage(dict(branch_coverage=dict(functions=scopes,module=dict(covered_branches=9,num_branches=10))),'get_custom_loader')
        self.assertEqual(result['target_branch_pct'],50)
        self.assertEqual(result['target_line_pct'],60)
        self.assertEqual(result['module_branch_pct'],90)
        self.assertIsNone(analyze.scoped_coverage(dict(branch_coverage=dict(module=dict(covered_branches=9,num_branches=10))),'get_custom_loader')['target_branch_pct'])

    def test_pool_mismatch_blocks_mutation_effect(self):
        self.arm('baseline')
        other=self.arm('verified')
        other['score']['mutant_pool_hash']='different-pool'
        write_json(self.root/'verified/report.json',other)
        rows,*_=analyze.collect(self.root)
        pair=next(p for p in analyze.paired_rows(rows) if p['comparator']=='baseline')
        self.assertTrue(pair['valid_pair'])
        self.assertFalse(pair['common_mutant_pool'])
        self.assertIsNone(pair['delta_mutation_score'])

    def test_arm_configuration_mismatch_blocks_all_effects(self):
        self.arm('baseline')
        self.arm('verified',settings=dict(self.settings,model_revision='different-revision'))
        rows,*_=analyze.collect(self.root)
        pair=next(p for p in analyze.paired_rows(rows) if p['comparator']=='baseline')
        self.assertFalse(pair['valid_pair'])
        self.assertIsNone(pair['delta_passed'])

    def test_initialization_counts_sync_and_async_without_altering_results(self):
        from pilot.instrumentation import instrument_initialization
        class Project:
            def analyze_function_members(self, value):
                return value+1
            async def analyze_functions(self):
                return 'original-return'
        project=Project()
        with contextlib.redirect_stdout(io.StringIO()):
            instrument_initialization(project,self.root)
            self.assertEqual(project.analyze_function_members(4),5)
            self.assertEqual(asyncio.run(project.analyze_functions()),'original-return')
        state=json.loads((self.root/'progress.json').read_text())
        self.assertEqual(state['analysis_steps_total'],2)
        self.assertEqual(state['analysis_steps_completed'],2)

    def test_rolling_dashboard_chart_is_bounded_and_labels_units(self):
        from pilot.notebook import render_charts
        frames=[dict(seconds=i*10,tokens=i*30,gpus=[dict(index='0',utilization_percent=50,used_mib=1024)]) for i in range(60)]
        chart=render_charts(frames)
        self.assertIn('GPU utilization (%)',chart)
        self.assertIn('GPU used memory (GiB)',chart)
        self.assertIn('Cumulative model tokens',chart)
        self.assertLess(len(chart),20000)


    def test_candidate_pool_mismatch_blocks_verification_contrast(self):
        self.arm('extracted')
        self.arm('verified')
        write_json(self.root/'verified/selection.json',dict(selected={'new_target':'x'},candidate_hash='different-candidates'))
        rows,*_=analyze.collect(self.root)
        pair=next(p for p in analyze.paired_rows(rows) if p['comparator']=='extracted')
        self.assertFalse(pair['valid_pair'])
        self.assertIsNone(pair['delta_passed'])


    def test_discovery_prunes_checkouts_and_distinguishes_validation(self):
        self.arm('baseline',status='failed')
        hidden=self.root/'upstream'
        hidden.mkdir()
        write_json(hidden/'experiment.json',self.settings)
        validation=self.root/'saved-validation'
        validation.mkdir()
        write_json(validation/'experiment.json',self.settings)
        write_json(validation/'comparison.json',dict(validation_only=True,status='complete'))
        found,truncated=analyze.discover_runs([self.root])
        self.assertFalse(truncated)
        self.assertEqual(len(found),2)
        actual=next(row for row in found if row['path']==str(self.root))
        self.assertEqual(actual['recorded'],1)
        self.assertEqual(actual['completed'],0)
        self.assertTrue(next(row for row in found if row['path']==str(validation))['validation_only'])

    def test_empty_auto_input_stops_without_creating_fake_report(self):
        from unittest.mock import patch
        import sys
        empty=self.root/'empty'; empty.mkdir()
        destination=self.root/'must-not-exist'
        with patch.object(sys,'argv',['analyze.py','--input','auto','--search-root',str(empty),'--output',str(destination)]), \
             contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                analyze.main()
        self.assertEqual(error.exception.code,2)
        self.assertFalse(destination.exists())


    def test_full_research_entrypoint_creates_inputs_and_real_run_plan(self):
        from unittest.mock import patch
        import sys
        import run_research
        destination=self.root/'generated-research'
        invoked=[]
        def fake_command(args,**kwargs):
            invoked.append(list(map(str,args)))
            kwargs['log_path'].write_text('synthetic orchestration test; not measured results')
            if 'analyze.py' in str(args[1]):
                folder=destination/'report'; folder.mkdir()
                (folder/'report.md').write_text('fixture, not research result')
            return dict(returncode=0,timeout=False,stdout='',stderr='')
        with patch.object(sys,'argv',['run_research.py','--output',str(destination)]), \
             patch.object(run_research,'command',fake_command),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(run_research.main(),0)
        self.assertEqual(len(invoked),3)
        self.assertIn('kaggle_run.py',invoked[0][2])
        self.assertEqual(invoked[1][1:4],['-m','pip','install'])
        self.assertEqual(Path(invoked[2][invoked[2].index('--input')+1]),destination/'experiment/comparison')
        spec=json.loads((destination/'input-specification.json').read_text())
        self.assertEqual(spec['kind'],'input_specification_not_experimental_results')
        self.assertTrue((destination/'results.zip').exists())

    def test_research_failure_stops_before_analysis_but_keeps_bundle(self):
        from unittest.mock import patch
        import sys
        import run_research
        destination=self.root/'failed-research'
        calls=[]
        def fail(args,**kwargs):
            calls.append(args)
            kwargs['log_path'].write_text('fixture failure')
            return dict(returncode=1,timeout=False,stdout='',stderr='fixture failure')
        with patch.object(sys,'argv',['run_research.py','--output',str(destination)]), \
             patch.object(run_research,'command',fail),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(run_research.main(),1)
        self.assertEqual(len(calls),1)
        self.assertEqual(json.loads((destination/'research-run.json').read_text())['status'],'failed')
        self.assertTrue((destination/'results.zip').exists())
        self.assertFalse((destination/'report/report.md').exists())

    def test_bundle_retains_generated_tests_and_omits_rebuildable_caches(self):
        import zipfile
        from run_research import bundle_artifacts
        generated=self.root/'experiment/comparison/baseline/PyCG/Test4DT_tests'
        generated.mkdir(parents=True)
        (generated/'test_generated.py').write_text('# fixture')
        (generated.parent/'production.py').write_text('# rebuild from pinned commit')
        upstream=self.root/'experiment/comparison/upstream'; upstream.mkdir(parents=True)
        (upstream/'large.txt').write_text('not included')
        archive=bundle_artifacts(self.root)
        with zipfile.ZipFile(archive) as stream:
            names=stream.namelist()
            self.assertTrue(any(name.endswith('test_generated.py') for name in names))
            self.assertFalse(any(name.endswith('production.py') or name.endswith('large.txt') for name in names))


    def test_partial_experiment_is_reported_without_hiding_failures(self):
        from unittest.mock import patch
        import sys
        import run_research
        destination=self.root/'partial-research'
        calls=[]
        def fake(args,**kwargs):
            calls.append(args)
            kwargs['log_path'].write_text('fixture partial run')
            if len(calls)==1:
                write_json(destination/'experiment/comparison/baseline/report.json',dict(status='failed'))
                return dict(returncode=1,timeout=False,stdout='',stderr='fixture')
            if len(calls)==3:
                folder=destination/'report'; folder.mkdir()
                (folder/'report.md').write_text('fixture partial report')
            return dict(returncode=0,timeout=False,stdout='',stderr='')
        with patch.object(sys,'argv',['run_research.py','--output',str(destination)]), \
             patch.object(run_research,'command',fake),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(run_research.main(),1)
        self.assertEqual(len(calls),3)
        self.assertTrue((destination/'report/report.md').exists())
        self.assertEqual(json.loads((destination/'research-run.json').read_text())['status'],'failed')


if __name__=='__main__':
    unittest.main()
