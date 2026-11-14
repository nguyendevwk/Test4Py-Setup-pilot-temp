import unittest
from pathlib import Path
from pilot.quality import extract_code, final_answer, code_quality, source_context
from pilot.model_profiles import profile, DEFAULT_MODEL

class QualityTests(unittest.TestCase):
    def test_reasoning_is_not_forwarded(self):
        self.assertEqual(final_answer('<think>guess</think>\n42')[0], '42')
        self.assertEqual(final_answer('<think>unfinished')[0], '')
    def test_single_block_only(self):
        self.assertTrue(code_quality(extract_code('```python\ndef f(): return 1\n```'))['ast_parse'])
        for raw in ('```python\nx=1','```python\nx=1\n```\n```python\ny=2\n```'):
            with self.assertRaises(ValueError): extract_code(raw)
    def test_profiles_and_unvalidated_architecture(self):
        self.assertEqual(profile(DEFAULT_MODEL)['eos_token_id'],166101)
        with self.assertRaises(ValueError):profile('Qwen/Qwen3.5-4B')
