"""Source provenance checks; these tests do not measure model efficacy."""
import ast
from pathlib import Path
import tempfile
import unittest

from pilot.source_prompt import source_first_prompt, trusted_context


class SourcePromptTests(unittest.TestCase):
    def test_source_retains_descriptor_and_closure_scope_without_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'subject.py').write_text('raise RuntimeError("must not execute")\n'
                'class Box:\n def __init__(self,value): self._value=value\n'
                ' @property\n def value(self): return self._value\n'
                ' def factory(self):\n  def inner(): return self.value\n  return inner\n')
            context,facts=trusted_context(root,'subject.py','Box.value')
            tree=ast.parse(context['code'])
            self.assertEqual(tree.body[0].name,'Box')
            getter=next(n for n in tree.body[0].body if n.name=='value')
            self.assertEqual(getter.decorator_list[0].id,'property')
            self.assertEqual(facts['target']['access'],'instance.value')
            closure,_=trusted_context(root,'subject.py','Box.factory.inner')
            self.assertEqual(closure['target'],'Box.factory.inner')
            self.assertIn('def factory(self)',closure['code'])

    def test_source_and_contract_ablation_share_actual_source_and_system(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'subject.py').write_text('def add(a,b): return a+b\n')
            base=source_first_prompt('Generate tests',root,'subject.py','add','subject',False)
            enriched=source_first_prompt('Generate tests',root,'subject.py','add','subject',True)
            self.assertEqual(base[0],enriched[0])
            self.assertTrue(enriched[1].startswith(base[1]))
            self.assertEqual(base[2]['context'],enriched[2]['context'])
            self.assertIsNone(base[2]['contract'])
            self.assertIsNotNone(enriched[2]['contract'])

    def test_oversized_target_fails_without_truncating_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'subject.py').write_text('def target():\n return '+repr('x'*500)+'\n')
            with self.assertRaisesRegex(ValueError,'exceeds fixed'):
                trusted_context(root,'subject.py','target',max_chars=100)


if __name__=='__main__': unittest.main()
