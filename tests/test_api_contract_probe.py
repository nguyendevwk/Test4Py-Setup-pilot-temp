"""Offline diagnostic orchestration test; scripted model is not efficacy data."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from pilot.common import append_json,write_json


class ApiContractProbeTests(unittest.TestCase):
    def test_real_pytest_replay_reach_and_failed_attempts_are_preserved_for_both_arms(self):
        spec=importlib.util.spec_from_file_location('api_probe_fixture',Path(__file__).resolve().parents[1]/'scripts/api_contract_probe.py')
        probe=importlib.util.module_from_spec(spec);spec.loader.exec_module(probe)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);study=root/'study';product=root/'subject';(product/'genty').mkdir(parents=True)
            (product/'genty/__init__.py').write_text('')
            source='class Box:\n def __init__(self, value): self._value=value\n @property\n def value(self): return self._value\n'
            (product/'genty/box.py').write_text(source)
            import hashlib
            hashes={str(p.relative_to(product)):hashlib.sha256(p.read_bytes()).hexdigest() for p in product.rglob('*.py')}
            write_json(study/'plan.json',dict(settings=dict(max_input_tokens=4096,max_new_tokens=512)))
            write_json(study/'resolved_models.json',dict(model='a'*40))
            write_json(study/'preflight.json',dict(genty=dict(import_root=str(product))))
            write_json(study/'prepared/genty/source_hashes.json',hashes)
            write_json(study/'prepared/genty/mutant-pools.json',{'genty.box':dict(mutants=[
                dict(id='fixture-boundary',source=source.replace('return self._value','return self._value+1'))])})
            versions=dict(torch='fixture',transformers='fixture',gpu='SCRIPTED_NOT_GPU',loaded_model_revision='a'*40,quantization='nf4',attention_policy='fixture')
            for gpu in ['0','1']:write_json(study/('stress-gpu-'+gpu)/'probe.json',dict(versions=versions))
            messages=[dict(role='system',content='pytest'),dict(role='user',content='target')]
            manifest=dict(model_revision='a'*40,diagnostic_fixture=True,arms=['baseline','api_contract'],targets=[dict(id='fixture',project='genty',module='genty.box',file='genty/box.py',symbol='Box.value',seed=42,messages=messages,prompt_sha256=hashlib.sha256(json.dumps(messages,sort_keys=True).encode()).hexdigest())])
            write_json(root/'manifest.json',manifest)
            package='genty'
            class ScriptedBackend:
                def __init__(self,settings,work):
                    self.work=work;self.versions=versions;self.torch=types.SimpleNamespace(manual_seed=lambda seed:None)
                async def ask(self,system,user):
                    access='box.value' if 'Production API facts' in user else 'box.value()'
                    code='from '+package+'.box import Box\ndef test_value():\n box=Box(3)\n assert '+access+' == 3\n'
                    result='```python\n'+code+'```'
                    append_json(self.work/'model_calls.jsonl',dict(fixture=True,input_tokens=0,output_tokens=0,seconds=0,truncated=False,output=result))
                    return result
            args=types.SimpleNamespace(study=study,output=root/'out',manifest=root/'manifest.json',gpu='0')
            with patch('pilot.backend.TransformersBackend',ScriptedBackend):
                self.assertEqual(probe.worker(args),0)
                args.gpu='1';self.assertEqual(probe.worker(args),0)
            baseline=json.loads((root/'out/gpu-0/results.json').read_text())[0]
            treatment=json.loads((root/'out/gpu-1/results.json').read_text())[0]
            self.assertEqual(baseline['status'],'pytest_failed')
            self.assertFalse(baseline['first_pass'])
            self.assertEqual(baseline['collected'],1)
            self.assertEqual(treatment['status'],'scored')
            self.assertTrue(treatment['first_pass'])
            self.assertTrue(treatment['replay_stable'])
            self.assertTrue(treatment['meaningful_target_test'])
            self.assertEqual(treatment['target_covered_lines'],1)
            self.assertEqual(treatment['mutants'],[dict(id='fixture-boundary',verdict='killed')])
            self.assertTrue(baseline['source_integrity']);self.assertTrue(treatment['source_integrity'])
            # Held-out preparation must select its own package/interpreter and
            # hashes, rather than silently executing the development checkout.
            package='widget'
            (product/'genty').rename(product/package)
            hashes={str(p.relative_to(product)):hashlib.sha256(p.read_bytes()).hexdigest() for p in product.rglob('*.py')}
            write_json(root/'source_hashes.json',hashes)
            write_json(root/'mutant-pools.json',{'widget.box':dict(mutants=[])} )
            write_json(root/'prepared.json',dict(ready=True,projects={'widget':dict(source=str(product),interpreter=sys.executable)}))
            target=manifest['targets'][0]
            target.update(project='widget',module='widget.box',file='widget/box.py',source_sha256=hashes['widget/box.py'])
            write_json(root/'manifest.json',manifest)
            args.prepared=root/'prepared.json';args.output=root/'heldout-fixture'
            with patch('pilot.backend.TransformersBackend',ScriptedBackend):
                args.gpu='0';self.assertEqual(probe.worker(args),0)
                args.gpu='1';self.assertEqual(probe.worker(args),0)
            result=json.loads((args.output/'gpu-1/results.json').read_text())[0]
            self.assertEqual(result['status'],'scored')
            self.assertTrue(result['meaningful_target_test'])
            self.assertEqual(result['project'],'widget')


if __name__=='__main__':unittest.main()
