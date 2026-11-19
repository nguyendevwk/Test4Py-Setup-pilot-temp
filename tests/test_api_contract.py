import json
from pathlib import Path
import tempfile
import unittest
import subprocess
import sys

from pilot.api_contract import augment_prompt, build_api_contract, candidate_accepted


class ApiContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def write(self, text):
        (self.root/'subject.py').write_text(text)

    def test_property_inventory_is_source_only_and_does_not_execute_getter(self):
        self.write('''raise RuntimeError("module must never execute")
class Item:
    def __init__(self, value): self._value = value
    @property
    def value(self): raise RuntimeError("getter must never execute")
    @staticmethod
    def create(value): return Item(value)
    @classmethod
    def load(cls, value): return cls(value)
    def save(self): return self._value
''')
        facts = build_api_contract(self.root, 'subject.py', 'Item.value')
        self.assertEqual(facts['target']['kind'], 'property')
        self.assertEqual(facts['target']['access'], 'instance.value')
        kinds = {m['name']:m['kind'] for m in facts['classes'][0]['members']}
        self.assertEqual(kinds['create'], 'staticmethod')
        self.assertEqual(kinds['load'], 'classmethod')
        self.assertEqual(kinds['save'], 'method')
        self.assertFalse(facts['target']['module_level_importable'])
        self.assertEqual(build_api_contract(self.root,'subject.py','Item.save')['target']['access'],'instance.save(...)')
        self.assertEqual(build_api_contract(self.root,'subject.py','Item.create')['target']['access'],'Item.create(...)')

    def test_nested_function_has_enclosing_factory_and_closure_binding(self):
        self.write('''def make(limit):
    def invoke(value):
        return value + limit
    return invoke
''')
        facts = build_api_contract(self.root, 'subject.py', 'invoke')
        self.assertEqual(facts['target']['symbol'], 'make.invoke')
        self.assertEqual(facts['target']['closure_variables'], ['limit'])
        self.assertEqual(facts['enclosing_api']['symbol'], 'make')
        self.assertIn('return invoke', facts['enclosing_api']['source'])

    def test_ambiguous_nested_name_is_not_resolved_by_first_match(self):
        self.write('def first(x):\n def wrap(): return x\n return wrap\ndef second(y):\n def wrap(): return y\n return wrap\n')
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            build_api_contract(self.root, 'subject.py', 'wrap')
        facts = build_api_contract(self.root, 'subject.py', 'second.wrap')
        self.assertEqual(facts['target']['closure_variables'], ['y'])

    def test_class_method_closure_keeps_owning_callable_and_receiver(self):
        self.write('class Client:\n def adapter(self, token):\n  def send(): return token + self.base\n  return send\n')
        facts=build_api_contract(self.root,'subject.py','Client.adapter.send')
        self.assertEqual(facts['enclosing_api']['symbol'],'Client.adapter')
        self.assertEqual(facts['enclosing_api']['kind'],'method')
        self.assertEqual(facts['target']['closure_variables'],['self','token'])
        self.assertEqual(facts['classes'][0]['symbol'],'Client')

    def test_factory_references_expose_class_properties_without_oracle_values(self):
        self.write('class Box:\n @property\n def payload(self): return 123456789\ndef pack(value): return Box()\n')
        facts = build_api_contract(self.root, 'subject.py', 'pack')
        self.assertEqual(facts['classes'][0]['members'][0]['kind'], 'property')
        self.assertNotIn('123456789', json.dumps(facts))

    def test_shadowed_and_custom_property_decorators_remain_unknown(self):
        self.write('def property(fn): return fn\nclass Box:\n @property\n def value(self): return 0\n')
        facts = build_api_contract(self.root, 'subject.py', 'Box.value')
        self.assertEqual(facts['target']['kind'], 'unknown_decorated_member')
        self.write('from builtins import property as readonly\nclass Box:\n @readonly\n def value(self): return 0\n')
        self.assertEqual(build_api_contract(self.root, 'subject.py', 'Box.value')['target']['kind'], 'property')

    def test_property_setter_does_not_make_the_getter_target_ambiguous(self):
        self.write('class Box:\n @property\n def value(self): return self._value\n @value.setter\n def value(self, value): self._value = value\n')
        facts = build_api_contract(self.root, 'subject.py', 'Box.value')
        self.assertEqual(facts['target']['kind'], 'property')

    def test_budget_omits_whole_context_parts_without_cutting_source(self):
        self.write('def factory(value):\n    """'+('long documentation '*400)+'"""\n    def apply(): return value\n    return apply\n')
        facts = build_api_contract(self.root, 'subject.py', 'apply', max_chars=1000)
        self.assertLessEqual(len(json.dumps(facts, ensure_ascii=False, separators=(',', ':'))), 1000)
        self.assertIn('enclosing source excerpt', facts['omitted'])
        self.assertNotIn('source', facts['enclosing_api'])

    def test_shared_instruction_identical_and_only_evidence_differs_between_arms(self):
        self.write('class Box:\n @property\n def value(self): return 0\n')
        baseline = augment_prompt('system','user',self.root,'subject.py','Box.value',False)
        treatment = augment_prompt('system','user',self.root,'subject.py','Box.value',True)
        self.assertEqual(baseline[0],treatment[0])
        self.assertEqual(baseline[1], 'user')
        self.assertIsNone(baseline[2])
        self.assertTrue(treatment[1].startswith('user\n\n'))
        self.assertIn('multiple tests are allowed', baseline[0])

    def test_test_sources_and_outside_paths_are_rejected(self):
        self.write('def target(): return 0\n')
        for path in ['../outside.py','test_subject.py','tests/subject.py']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                build_api_contract(self.root,path,'target')

    def test_common_gate_treats_both_arms_identically_and_keeps_legacy_behavior(self):
        changed = dict(accepted=False,review_required=True)
        preserved = dict(accepted=True,review_required=False)
        for arm in ['baseline','api_contract']:
            self.assertFalse(candidate_accepted(True,changed,arm,'preserve-assertions-v1'))
            self.assertTrue(candidate_accepted(True,preserved,arm,'preserve-assertions-v1'))
            self.assertFalse(candidate_accepted(False,preserved,arm,'preserve-assertions-v1'))
        self.assertTrue(candidate_accepted(True,changed,'baseline'))
        self.assertFalse(candidate_accepted(True,changed,'improved'))

    def test_mechanism_plan_has_two_arms_common_gate_and_no_one_test_constraint(self):
        from paired_study import build_plan
        from pilot.reuse import initialization_settings
        plan = build_plan(mechanism='api-contract-v1')
        self.assertEqual(plan['arms'],['baseline','api_contract'])
        self.assertEqual(plan['settings']['acceptance_policy'],'preserve-assertions-v1')
        self.assertNotIn('test_output_contract',plan['settings'])
        self.assertEqual(initialization_settings(plan['settings']),initialization_settings(build_plan()['settings']))
        with self.assertRaises(ValueError):
            build_plan(test_output_contract='single-test-v1',mechanism='api-contract-v1')

    def test_mechanism_cli_round_trip_uses_frozen_policy_without_gpu_loading(self):
        import paired_study
        output=self.root/'plan'
        args=[sys.executable,str(paired_study.BASE/'paired_study.py'),'--output',str(output)]
        planned=subprocess.run([*args,'--action','plan','--mechanism','api-contract-v1',
            '--max-input-tokens','4096','--max-new-tokens','512'],capture_output=True,text=True,timeout=30)
        self.assertEqual(planned.returncode,0,planned.stdout+planned.stderr)
        reported=subprocess.run([*args,'--action','report'],capture_output=True,text=True,timeout=30)
        self.assertEqual(reported.returncode,0,reported.stdout+reported.stderr)
        saved=json.loads((output/'plan.json').read_text())
        self.assertEqual(saved['arms'],['baseline','api_contract'])
        self.assertEqual(saved['settings']['acceptance_policy'],'preserve-assertions-v1')


if __name__ == '__main__': unittest.main()
