import ast
import copy
import json
from pathlib import Path
import tempfile
import unittest

from pilot.reuse import verify_calibration,WRAPPER_SHA256,import_initialization_prefix
from pilot.common import write_json,digest
from pilot.initialization_cache import cache_key


class ReuseTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.previous=self.root/'previous'
        self.settings=dict(attention_policy='t4-efficient-sdpa-v1',max_input_tokens=4096,max_new_tokens=512)
        self.revisions=dict(model='a'*40)
        expected=dict(self.settings,model_revision='a'*40,seed=42)
        self.runtime=dict(torch='2.11.0+cu130',transformers='4.57.6',gpu='Tesla T4',device_count=2)
        script=Path(__file__).resolve().parents[1]/'scripts/kaggle_quick_oom_check.py'
        tree=ast.parse(script.read_text())
        wrapper=next(n.value.value for n in tree.body if isinstance(n,ast.Assign)
                     and any(isinstance(t,ast.Name) and t.id=='wrapper' for t in n.targets))
        (self.root/'attention-wrapper.py').write_text(wrapper)
        write_json(self.root/'settings.json',expected)
        write_json(self.root/'provenance.json',dict(previous_study=str(self.previous),settings=expected,wrapper_sha256=WRAPPER_SHA256))
        self.summary=dict(passed=True,results=[])
        for gpu in ('0','1'):
            test=dict(passed=True,input_tokens=4096,output_tokens=512,conservative_headroom_gib=3.67)
            probe=dict(status='passed',settings=expected,margin_gib=1.5,tests=[copy.deepcopy(test),copy.deepcopy(test)],
                       versions=dict(torch='2.11.0+cu130',transformers='4.57.6',gpu='Tesla T4',loaded_model_revision='a'*40,quantization='nf4'))
            self.summary['results'].append(dict(gpu=gpu,passed=True,process=dict(returncode=0,timeout=False),probe=probe))
        self.save()

    def save(self):
        for row in self.summary['results']:write_json(self.root/('gpu-'+row['gpu'])/'probe.json',row['probe'])
        write_json(self.root/'summary.json',self.summary)

    def verify(self,**kwargs):
        return verify_calibration(self.root,kwargs.get('settings',self.settings),self.revisions,
                                  kwargs.get('runtime',self.runtime),self.previous)

    def test_matching_calibration_has_explicit_imported_origin(self):
        accepted=self.verify()
        self.assertEqual(set(accepted),{'0','1'})
        self.assertTrue(all(r['origin']=='validated_existing_session_diagnostic' for r in accepted.values()))

    def test_generation_only_contract_keeps_exact_memory_calibration(self):
        accepted=self.verify(settings=dict(self.settings,test_output_contract='single-test-v1'))
        self.assertEqual(set(accepted),{'0','1'})
        with self.assertRaises(ValueError):
            self.verify(settings=dict(self.settings,test_output_contract='unverified'))

    def test_changed_budget_environment_or_wrapper_rejects_reuse(self):
        with self.assertRaises(ValueError):self.verify(settings=dict(self.settings,max_input_tokens=2048))
        with self.assertRaises(ValueError):self.verify(runtime=dict(self.runtime,torch='different'))
        (self.root/'attention-wrapper.py').write_text('unverified adapter')
        with self.assertRaises(ValueError):self.verify()

    def test_failed_or_incomplete_max_context_evidence_rejects_reuse(self):
        original=copy.deepcopy(self.summary)
        for mutation in ('timeout','missing_repeat','insufficient_headroom'):
            self.summary=copy.deepcopy(original)
            record=self.summary['results'][0]
            if mutation=='timeout':record['process']['timeout']=True
            elif mutation=='missing_repeat':record['probe']['tests'].pop()
            else:record['probe']['tests'][0]['conservative_headroom_gib']=0.5
            self.save()
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):self.verify()

    def test_prefix_import_uses_only_initialization_and_preserves_raw_outputs(self):
        previous=self.root/'prefix-old';current=self.root/'prefix-new';current.mkdir()
        settings=dict(self.settings,model='fixture-model',quantization='nf4',initialization_greedy=True)
        old=dict(settings=settings,frame={'genty':{}},small=dict(project='genty',modules=['genty.args']),arms=['baseline','improved'],source_sha256={'observer':'old'})
        new=dict(old,settings=dict(settings,test_output_contract='single-test-v1'),source_sha256={'observer':'new'})
        revisions=dict(model='a'*40,embedding='b'*40)
        write_json(previous/'plan.json',old);write_json(current/'resolved_models.json',revisions)
        code='VALUE = 1\n';import hashlib
        write_json(current/'prepared/genty/source_hashes.json',{'genty/args.py':hashlib.sha256(code.encode()).hexdigest()})
        versions=dict(quantization='nf4',torch=self.runtime['torch'],transformers=self.runtime['transformers'],
                      gpu=self.runtime['gpu'],loaded_model_revision=revisions['model'],attention_policy=settings['attention_policy'])
        messages=[dict(role='user',content='summarize this source')]
        for arm in old['arms']:
            worker=previous/'small'/('genty-42-'+arm);(worker/'product/genty').mkdir(parents=True)
            (worker/'product/genty/args.py').write_text(code)
            cfg=dict(settings,model_revision=revisions['model'],embedding_revision=revisions['embedding'],adapter_source_hash=digest(old['source_sha256']))
            write_json(worker/'worker-settings.json',cfg)
            write_json(worker/'analysis_scope.json',dict(selected_generation_modules=['genty.args']))
            key=cache_key(cfg,versions,messages)
            cached=dict(key=key,output='original summary',output_tokens=3,truncated=False)
            write_json(previous/'initialization-cache'/(key+'.json'),cached)
            call=dict(cached,phase='initialization',cache_key=key,messages=messages,input_tokens=8,inference_started=arm=='baseline')
            forbidden=dict(phase='generation_round_1',output='assert False',messages=messages)
            (worker/'model_calls.jsonl').write_text(json.dumps(call)+'\n'+json.dumps(forbidden)+'\n')
        # A declared generation-only contract may change; physical/model budgets may not.
        with self.assertRaises(ValueError):
            import_initialization_prefix(current,previous,
                dict(new,settings=dict(new['settings'],max_new_tokens=1024)),self.runtime)
        with self.assertRaises(ValueError):
            import_initialization_prefix(current,previous,
                dict(new,settings=dict(new['settings'],test_output_contract='unverified')),self.runtime)
        import_initialization_prefix(current,previous,new,self.runtime)
        files=list((current/'initialization-cache').glob('*.json'));self.assertEqual(len(files),1)
        self.assertEqual(json.loads(files[0].read_text())['output'],'original summary')
        receipt=json.loads((current/'initialization-reuse.json').read_text())
        self.assertEqual(receipt['unique_prompts'],1);self.assertEqual(receipt['prior_fresh_calls'],1)
        self.assertEqual(receipt['generation_output_contract']['current'],'single-test-v1')
