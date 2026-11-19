"""CPU-only regression tests for paired upstream runtime/guards/planning."""
import ast
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch, Mock

from pilot.runtime_limits import load_causal_model, check_token_budget
from pilot.upstream_adapter import stdlib_import_patch, validate_imports, load_cpu_embedding, install_type_guards
from pilot.module_mutation import pool, verdict
import paired_study


class PairedTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.torch=types.SimpleNamespace(float16='fp16')
        self.settings=dict(model=paired_study.MODEL,model_revision='a'*40,quantization='nf4',
                           max_input_tokens=4096,max_new_tokens=1024,max_sequence_tokens=5120)

    def test_opt_in_output_contract_is_frozen_by_plan_and_drift_is_rejected(self):
        output=self.root/'compact-plan'
        proc=subprocess.run([sys.executable,str(paired_study.BASE/'paired_study.py'),
            '--action','plan','--output',str(output),'--max-input-tokens','4096',
            '--max-new-tokens','512','--test-output-contract','single-test-v1'],
            capture_output=True,text=True,timeout=30)
        self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
        saved=json.loads((output/'plan.json').read_text())
        self.assertEqual(saved['settings']['test_output_contract'],'single-test-v1')
        self.assertTrue(saved['protocol'].endswith('+single-test-v1'))
        paired_study.validate_plan(output,paired_study.build_plan(4096,512,'single-test-v1'))
        with self.assertRaisesRegex(ValueError,'Plan/source changed'):
            paired_study.validate_plan(output,paired_study.build_plan(4096,512))
        self.assertNotIn('test_output_contract',paired_study.build_plan()['settings'])

    def test_project_dependency_commands_are_accepted_by_real_pip_offline(self):
        # Real metadata/resolution, without modifying this environment or network access.
        package=self.root/'package';package.mkdir()
        (package/'setup.py').write_text(
            "from setuptools import setup\nsetup(name='test4py-dependency-fixture',version='0.0.1',py_modules=['fixture'])\n")
        (package/'fixture.py').write_text('VALUE = 1\n')
        req_project=self.root/'requirements-project';req_project.mkdir()
        (req_project/'requirements.txt').write_text(str(package)+'\n')
        for product in (package,req_project):
            with self.subTest(product=product.name):
                args=list(map(str,paired_study.project_install_command(sys.executable,product)))
                args[4:4]=['--dry-run','--no-index','--no-deps','--no-build-isolation']
                proc=subprocess.run(args,cwd=product,capture_output=True,text=True,timeout=60)
                self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
                self.assertIn('Would install test4py-dependency-fixture-0.0.1',proc.stdout)

    def test_dependency_install_failure_never_becomes_prepared(self):
        plan=paired_study.build_plan();plan['frame']={'genty':plan['frame']['genty']}
        work=self.root/'prepared/genty';(work/'source').mkdir(parents=True)
        (self.root/'upstream').mkdir()
        (work/'source/setup.py').touch()
        (work/'venv/bin').mkdir(parents=True);(work/'venv/bin/python').touch()
        (self.root/'resolved_models.json').write_text('{}')
        def run(args,**kwargs):
            failed='-e' in args
            return dict(returncode=int(failed),timeout=False,stdout='synthetic dependency failure' if failed else '',stderr='')
        with patch.object(paired_study,'checked',side_effect=[paired_study.UPSTREAM,plan['frame']['genty']['sha']]), \
             patch.object(paired_study,'command',side_effect=run) as command, \
             patch.object(paired_study,'locate_module') as locate:
            self.assertFalse(paired_study.prepare(self.root,plan))
        locate.assert_not_called()
        self.assertEqual(command.call_count,2)  # Existing venv still requires both dependency stages.
        self.assertEqual(json.loads((self.root/'preflight.json').read_text())['genty']['status'],'failed')
        self.assertEqual(json.loads((work/'dependency-install.json').read_text())['returncode'],1)

    def test_nf4_failure_is_not_retried_as_fp16(self):
        model=types.SimpleNamespace(from_pretrained=Mock(side_effect=RuntimeError('NF4 failed')))
        with self.assertRaisesRegex(RuntimeError,'NF4 failed'):
            load_causal_model(self.settings,self.torch,model,lambda **k:k)
        self.assertEqual(model.from_pretrained.call_count,1)
        self.assertIn('quantization_config',model.from_pretrained.call_args.kwargs)

    def test_nf4_revision_dtype_and_device_are_explicit(self):
        loaded=types.SimpleNamespace(is_loaded_in_4bit=True,hf_device_map={'':'cuda:0'})
        loaded.eval=lambda:loaded
        factory=types.SimpleNamespace(from_pretrained=Mock(return_value=loaded))
        actual,mode=load_causal_model(self.settings,self.torch,factory,lambda **k:k)
        self.assertIs(actual,loaded);self.assertEqual(mode,'nf4')
        opts=factory.from_pretrained.call_args.kwargs
        self.assertEqual(opts['revision'],'a'*40)
        self.assertEqual(opts['device_map'],{'':'cuda:0'})
        self.assertEqual(opts['torch_dtype'],'fp16')
        self.assertEqual(opts['quantization_config']['bnb_4bit_quant_type'],'nf4')

    def test_missing_quantization_flag_and_offload_rejected(self):
        for loaded in [types.SimpleNamespace(is_loaded_in_4bit=False),
                       types.SimpleNamespace(is_loaded_in_4bit=True,hf_device_map={'':'cpu'})]:
            loaded.eval=lambda loaded=loaded:loaded
            with self.assertRaises(RuntimeError):
                load_causal_model(self.settings,self.torch,types.SimpleNamespace(from_pretrained=lambda *a,**k:loaded),lambda **k:k)

    def test_exact_input_plus_output_limits(self):
        check_token_budget(4096,self.settings)
        with self.assertRaisesRegex(ValueError,'Input budget'):
            check_token_budget(4097,self.settings)
        with self.assertRaisesRegex(ValueError,'Sequence budget'):
            check_token_budget(4096,dict(self.settings,max_sequence_tokens=5000))

    def test_backend_overflow_is_logged_before_any_gpu_move_or_generation(self):
        import asyncio
        from pilot.backend import TransformersBackend
        backend=object.__new__(TransformersBackend)
        backend.settings=dict(self.settings,max_input_tokens=4,max_new_tokens=1,max_sequence_tokens=5)
        backend.work=self.root;backend.phase='initialization';backend.profile={}
        backend.call_count=backend.calls_finished=backend.calls_failed=backend.input_tokens=backend.output_tokens=0
        class Batch(dict):
            input_ids=types.SimpleNamespace(shape=(1,5))
            def to(self,device):raise AssertionError('overflow must remain on CPU')
        backend.tokenizer=types.SimpleNamespace(apply_chat_template=lambda *a,**k:Batch())
        backend.model=types.SimpleNamespace(device='cuda:0',generate=Mock())
        backend.torch=types.SimpleNamespace(cuda=types.SimpleNamespace(memory_allocated=lambda:0,memory_reserved=lambda:0,
            max_memory_allocated=lambda:0,is_available=lambda:True,empty_cache=lambda:None))
        with self.assertRaisesRegex(ValueError,'Input budget'):
            asyncio.run(backend.ask('system','user'))
        backend.model.generate.assert_not_called()
        record=json.loads((self.root/'model_calls.jsonl').read_text())
        self.assertEqual(record['input_tokens'],5)
        self.assertIn('Input budget',record['error'])
        self.assertEqual(backend.calls_failed,1)

    def test_stress_evidence_is_bound_to_plan_gpu_and_model_revision(self):
        from pilot.common import digest
        plan=paired_study.build_plan()
        evidence=dict(config_hash=digest(plan['settings']),plan_hash=digest(plan),model_revision='a'*40,
                      gpus={'0':dict(status='passed')})
        paired_study.validate_stress(evidence,plan,dict(model='a'*40),['0'])
        for revision,slots in [('b'*40,['0']),('a'*40,['1'])]:
            with self.assertRaises(ValueError):
                paired_study.validate_stress(evidence,plan,dict(model=revision),slots)

    def test_parallel_stress_shares_one_screen_deadline(self):
        import threading
        from pilot.common import write_json
        plan=paired_study.build_plan()
        write_json(self.root/'preflight.json',{p:dict(status='prepared') for p in plan['frame']})
        write_json(self.root/'resolved_models.json',dict(model='a'*40))
        barrier=threading.Barrier(2)
        def run(args,**kwargs):
            barrier.wait(timeout=5)  # Serial execution would break this engineering check.
            folder=Path(args[args.index('--output')+1]);folder.mkdir()
            write_json(folder/'probe.json',dict(status='passed'))
            self.assertGreater(kwargs['timeout'],0);self.assertLessEqual(kwargs['timeout'],1800)
            return dict(returncode=0,timeout=False)
        with patch.object(paired_study,'gpu_slots',return_value=['0','1']),patch.object(paired_study,'command',side_effect=run):
            self.assertTrue(paired_study.stress(self.root,plan,2))
        clock=json.loads((self.root/'screen-clock.json').read_text())
        self.assertEqual(clock['deadline_epoch']-clock['started_epoch'],3600)
        with patch.object(paired_study.time,'time',return_value=clock['deadline_epoch']+1):
            self.assertEqual(paired_study.screen_remaining(self.root),0)
        with self.assertRaises(ValueError):
            paired_study.stress(self.root,plan,2)

    def test_expired_screen_retains_every_trial_without_download_or_worker(self):
        from pilot.common import write_json
        plan=paired_study.build_plan()
        write_json(self.root/'preflight.json',{p:dict(status='prepared') for p in plan['frame']})
        write_json(self.root/'resolved_models.json',dict(model='a'*40,embedding='b'*40))
        write_json(self.root/'stress.json',{})
        with patch.object(paired_study,'gpu_slots',return_value=['0','1']), \
             patch.object(paired_study,'validate_stress'), \
             patch.object(paired_study,'screen_remaining',return_value=0), \
             patch.object(paired_study,'command') as command:
            self.assertFalse(paired_study.execute(self.root,plan,'small',2))
        command.assert_not_called()
        report=json.loads((self.root/'small-summary.json').read_text())
        self.assertEqual(report['planned_module_trials'],4)
        self.assertEqual(len(report['rows']),4)
        self.assertFalse(report['larger_ready'])
        self.assertTrue(all(r['line_pct'] is None for r in report['rows']))

    def test_greedy_prefix_cache_reuses_exact_prompt_without_a_second_decode(self):
        import asyncio
        from contextlib import nullcontext
        from pilot.backend import TransformersBackend
        class Batch(dict):
            input_ids=types.SimpleNamespace(shape=(1,3))
            def to(self,device):return self
        class Output:
            def __getitem__(self,key):return [123]
        generate=Mock(return_value=Output())
        def backend(name):
            b=object.__new__(TransformersBackend)
            b.settings=dict(self.settings,max_new_tokens=1,initialization_greedy=True,
                            initialization_cache=str(self.root/'cache'),generation=dict(do_sample=True,temperature=0.7))
            b.versions=dict(quantization='nf4',torch='fixture')
            b.work=self.root/name;b.work.mkdir();b.phase='initialization';b.profile={}
            b.call_count=b.calls_finished=b.calls_failed=b.input_tokens=b.output_tokens=0
            b.fresh_input_tokens=b.fresh_output_tokens=0
            b.tokenizer=types.SimpleNamespace(apply_chat_template=lambda *a,**k:Batch(),
                            eos_token_id=0,decode=lambda *a,**k:'fixture summary')
            b.model=types.SimpleNamespace(device='cuda:0',generate=generate)
            b.torch=types.SimpleNamespace(inference_mode=nullcontext,cuda=types.SimpleNamespace(memory_allocated=lambda:0,
                memory_reserved=lambda:0,max_memory_allocated=lambda:0,is_available=lambda:True,empty_cache=lambda:None))
            return b
        a=backend('a');b=backend('b')
        self.assertEqual(asyncio.run(a.ask('same','prompt')),asyncio.run(b.ask('same','prompt')))
        self.assertEqual(generate.call_count,1)
        self.assertFalse(generate.call_args.kwargs['do_sample'])
        self.assertEqual(a.fresh_input_tokens,3);self.assertEqual(b.fresh_input_tokens,0)
        self.assertTrue(json.loads((b.work/'model_calls.jsonl').read_text())['cache_hit'])
        b.phase='generation_round_1'
        asyncio.run(b.ask('same','prompt'))
        self.assertEqual(generate.call_count,2)  # generation is never cached
        self.assertTrue(generate.call_args.kwargs['do_sample'])

    def test_prefix_cache_key_changes_with_prompt_revision_and_budget(self):
        from pilot.initialization_cache import cache_key
        first=cache_key(self.settings,{},['prompt'])
        self.assertNotEqual(first,cache_key(dict(self.settings,model_revision='b'*40),{},['prompt']))
        self.assertNotEqual(first,cache_key(dict(self.settings,max_new_tokens=2),{},['prompt']))
        self.assertNotEqual(first,cache_key(self.settings,{},['different prompt']))

    def test_collection_failure_without_tests_key_stays_a_failure(self):
        from pilot.upstream_adapter import tolerate_empty_pytest_report
        path=self.root/'compat.py'
        source="class Testcase:\n    def find_assert_error(self):\n        tests = pytest_report['tests']\n        return tests\n"
        path.write_text(source)
        module=types.ModuleType('compatfixture');module.pytest_report={}
        exec(compile(source,str(path),'exec'),module.__dict__)
        with self.assertRaises(KeyError):module.Testcase().find_assert_error()
        metadata=tolerate_empty_pytest_report(module)
        self.assertEqual(module.Testcase().find_assert_error(),[])
        self.assertIn('collection-error',metadata['policy'])

    def test_unexpected_worker_errors_block_larger_readiness(self):
        plan=paired_study.build_plan();queue=paired_study.tasks(plan,'small')
        for t in queue:
            folder=self.root/'small'/f"{t['project']}-{t['seed']}-{t['arm']}";folder.mkdir(parents=True)
            (folder/'report.json').write_text(json.dumps(dict(status='execution_complete',unexpected_generation_errors=1,modules=[])))
            (folder/'process.json').write_text(json.dumps(dict(returncode=0,timeout=False)))
        self.assertFalse(paired_study.collect(self.root,plan,'small',queue))

    def test_stdlib_patch_preserves_assertions_and_future(self):
        code='"module doc"\nfrom __future__ import annotations\ndef test_x():\n    assert math.isnan(float("nan"))\n'
        patched,modules=stdlib_import_patch(code)
        self.assertEqual(modules,['math'])
        compile(patched,'<patched>','exec')
        assertions=lambda s:[ast.dump(n) for n in ast.walk(ast.parse(s)) if isinstance(n,ast.Assert)]
        self.assertEqual(assertions(code),assertions(patched))
        self.assertLess(patched.index('__future__'),patched.index('import math'))

    def test_no_guessing_third_party_or_shadowed_names(self):
        for code in ['def test_x():\n    assert inventedpkg.value == 1\n',
                     'def test_x(math):\n    assert math.value == 1\n']:
            self.assertEqual(stdlib_import_patch(code),(code,[]))

    def test_import_namespace_contradiction_cannot_become_fact(self):
        (self.root/'provider.py').write_text('class Actual:\n    pass\n')
        good=validate_imports('from provider import Actual\ndef test_x():\n    raise RuntimeError("body must not run")',self.root)
        bad=validate_imports('from provider import Invented',self.root)
        self.assertTrue(good['accepted'])
        self.assertEqual(bad['status'],'contradicted')
        self.assertFalse(bad['accepted'])

    def test_module_attribute_hallucination_and_shadowing(self):
        (self.root/'provider.py').write_text('class Actual:\n    pass\n')
        bad=validate_imports('import provider\ndef test_x():\n    assert provider.Invented',self.root)
        self.assertFalse(bad['accepted'])
        self.assertIn('provider.Invented',bad['module_attribute_checks'])
        shadowed=validate_imports('import provider\ndef test_x(provider):\n    assert provider.runtime_field',self.root)
        self.assertTrue(shadowed['accepted'])
        self.assertEqual(shadowed['module_attribute_checks'],[])

    def test_dynamic_module_attributes_stay_unknown(self):
        (self.root/'provider.py').write_text('def __getattr__(name):\n    return 1\n')
        result=validate_imports('import provider\ndef test_x():\n    assert provider.dynamic == 1',self.root)
        self.assertTrue(result['accepted'])
        self.assertEqual(result['unknown_attributes'],['provider.dynamic'])
        self.assertNotEqual(result['status'],'verified')

    def test_cpu_embedding_adapter_does_not_toggle_global_cuda(self):
        directory=self.root/'test4dt';directory.mkdir()
        source='''import torch
class Embedder:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
embedder = Embedder()
def find_topK_message(name, messages, query_vector, k=1):
    return messages[:k]
'''
        (directory/'embedding.py').write_text(source)
        cuda=Mock(side_effect=AssertionError('global CUDA must not be queried'))
        fake=types.SimpleNamespace(device=lambda name:name,cuda=types.SimpleNamespace(is_available=cuda))
        with patch.dict('sys.modules',{'torch':fake}):
            meta=load_cpu_embedding(self.root)
            import sys
            embedded_module=sys.modules['test4dt.embedding']
        self.assertEqual(meta['embedding_device'],'cpu')
        self.assertEqual((directory/'embedding.py').read_text(),source)
        cuda.assert_not_called()
        self.assertEqual(embedded_module.find_topK_message('x',[],[],1),[])

    def test_type_guard_rejects_wrong_members_and_nonexistent_class(self):
        path=self.root/'provider.py';path.write_text('class Actual:\n    def read(self):\n        return 1\n')
        node=ast.parse(path.read_text()).body[0]
        cls=types.SimpleNamespace(full_name='provider.Actual',class_name='Actual',node=node,
                  file=types.SimpleNamespace(mod_name='provider',file_path=str(path)),full_members={'read'},class_code='class Actual: pass',init_method=None)
        ghost=types.SimpleNamespace(**{**vars(cls),'full_name':'provider.Ghost','class_name':'Ghost'})
        class Arg:
            members=['read'];name='receiver'
            def filter_by_members(self):return [cls,ghost]
        class Class:
            def get_how_to_use(self):return 'invented API example'
        message=types.SimpleNamespace(ArgMessage=Arg,ClassMessage=Class)
        install_type_guards(message,self.root,self.root)
        self.assertEqual(Arg().filter_by_members(),[cls])
        rendered=Class.get_how_to_use(cls)
        self.assertNotIn('invented API',rendered)
        self.assertIn('verified',json.loads((self.root/'type_facts.jsonl').read_text().splitlines()[0])['status'])
        Arg.members=['missing']
        self.assertEqual(Arg().filter_by_members(),[])

    def test_fault_pool_is_fixed_without_test_outcomes(self):
        source='def compute(x):\n    if x < 0:\n        return x - 1\n    return x + 1\n'
        first=pool(source,2)
        self.assertEqual(first,pool(source,2));self.assertEqual(len(first['mutants']),2)
        for m in first['mutants']:compile(m['source'],'mutant','exec')
        self.assertEqual(len(pool('class X:\n    n=1+2\n',4)['mutants']),0)

    def test_mutant_import_setup_timeout_are_not_kills(self):
        eligible=['test_x.py::test_x']
        record=dict(nodeid=eligible[0],setup=dict(outcome='passed'),teardown=dict(outcome='passed'),call=dict(outcome='failed',longrepr='AssertionError'))
        report=dict(tests=[record]);process=dict(returncode=1,timeout=False)
        self.assertEqual(verdict(process,report,eligible),'killed')
        for altered,proc in [(dict(record,setup=dict(outcome='failed')),process),
                             (dict(record,call=dict(outcome='failed',longrepr='ImportError')),process),
                             (record,dict(returncode=1,timeout=True))]:
            self.assertNotEqual(verdict(proc,dict(tests=[altered]),eligible),'killed')

    def test_fault_pool_distinguishes_nested_operators_with_same_start(self):
        mutants=pool('def product(a,b,c):\n return a*b*c\n',4)['mutants']
        self.assertEqual(len(mutants),2)
        outputs=[]
        for mutant in mutants:
            namespace={};exec(mutant['source'],namespace)
            outputs.append(namespace['product'](2,3,4))
        self.assertEqual(outputs,[10,20])

    def test_plan_small_and_larger_are_same_model_and_upstream(self):
        plan=paired_study.build_plan()
        self.assertEqual(plan['settings']['model'],'Qwen/Qwen2.5-Coder-14B-Instruct')
        self.assertEqual(plan['settings']['quantization'],'nf4')
        self.assertEqual(len(paired_study.tasks(plan,'small')),2)
        large=paired_study.tasks(plan,'main')
        self.assertEqual(sum(len(t['modules']) for t in large),12)
        frame=json.loads((paired_study.BASE/'research/benchmark/projects-upstream.json').read_text())
        for name,spec in plan['frame'].items():
            self.assertEqual(len(spec['sha']),40)
            self.assertTrue(set(spec['modules'])<=set(frame[name]))

    def test_collection_retains_missing_trials_and_pairs_by_target_seed(self):
        plan=paired_study.build_plan();queue=paired_study.tasks(plan,'small')
        self.assertFalse(paired_study.collect(self.root,plan,'small',queue))
        report=json.loads((self.root/'small-summary.json').read_text())
        self.assertEqual(len(report['rows']),4)
        self.assertTrue(all(r['line_pct'] is None for r in report['rows']))
        self.assertEqual(len(json.loads((self.root/'small-paired-differences.json').read_text())),2)
        measures=json.loads((self.root/'small-measurement-summary.json').read_text())['arms']
        for arm in plan['arms']:
            self.assertEqual(measures[arm]['planned_module_trials'],2)
            self.assertEqual(measures[arm]['retained_suite_unmeasured_trials'],2)
            self.assertIsNone(measures[arm]['retained_all_pass_rate'])
            self.assertEqual(measures[arm]['observed_successes_per_planned'],0)
            self.assertIsNone(measures[arm]['line']['macro_mean_pct'])
            self.assertIsNone(measures[arm]['semantic_assertion_accuracy'])

    def test_timeout_is_terminal_and_unmeasured_rate_is_not_zero_accuracy(self):
        plan=paired_study.build_plan();queue=paired_study.tasks(plan,'small')
        for t in queue:
            d=self.root/'small'/f"{t['project']}-{t['seed']}-{t['arm']}";d.mkdir(parents=True)
            (d/'report.json').write_text(json.dumps(dict(status='running',modules=[])))
            (d/'process.json').write_text(json.dumps(dict(returncode=-9,timeout=True,seconds=3587)))
        self.assertFalse(paired_study.collect(self.root,plan,'small',queue))
        report=json.loads((self.root/'small-summary.json').read_text())
        self.assertEqual(report['finished_module_rows'],0)
        self.assertEqual(report['reported_module_rows'],4)
        self.assertTrue(all(r['worker_status']=='timeout' and r['worker_seconds']==3587 for r in report['rows']))
        rates=json.loads((self.root/'small-measurement-summary.json').read_text())['arms']
        self.assertTrue(all(r['retained_all_pass_rate'] is None for r in rates.values()))

    def test_mutant_pool_mismatch_blocks_paired_fault_delta(self):
        plan=paired_study.build_plan();queue=paired_study.tasks(plan,'small')
        for i,t in enumerate(queue):
            d=self.root/'small'/f"{t['project']}-{t['seed']}-{t['arm']}";d.mkdir(parents=True)
            (d/'report.json').write_text(json.dumps(dict(status='execution_complete',modules=[dict(module=t['modules'][0],status='scored',passed=1,line_pct=10,branch_pct=0,mutation_score=i,mutant_pool_hash=str(i))])))
            (d/'process.json').write_text(json.dumps(dict(returncode=0,timeout=False)))
        self.assertTrue(paired_study.collect(self.root,plan,'small',queue))
        row=json.loads((self.root/'small-paired-differences.json').read_text())[0]
        self.assertFalse(row['mutant_pool_match']);self.assertIsNone(row['mutation_delta'])
        measures=json.loads((self.root/'small-measurement-summary.json').read_text())['arms']
        self.assertTrue(all(m['branch']['macro_mean_pct']==0 for m in measures.values()))
