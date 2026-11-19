import asyncio
import json
from contextlib import nullcontext
from pathlib import Path
import tempfile
import types
import unittest

from pilot.output_contract import (
    OutputContractError,
    append_prompt_contract,
    POLICY,
    validate_initial_generation,
)
from pilot.quality import extract_code


class OutputContractTests(unittest.TestCase):
    def test_generation_contract_and_verbatim_extracted_module(self):
        raw = '''```python
import pytest

@pytest.fixture
def value():
    return 3

def helper(x):
    def test_nested_helper():
        pass
    return x

def test_target(value):
    assert helper(value) == 3
```'''
        system, user = append_prompt_contract('system', 'target context', 'generate_test_case_normal')
        self.assertEqual(system, 'system')
        self.assertIn('exactly one complete pytest test', user)
        self.assertNotIn('one assertion', user)
        extracted = extract_code(raw)
        self.assertEqual(validate_initial_generation(raw), extracted)

    def test_class_test_counts_but_fixture_and_helpers_do_not(self):
        source = '''import pytest

@pytest.fixture
def resource():
    return object()

@pytest.fixture
def test_fixture():
    return object()

def helper():
    def test_nested():
        pass

class TestTarget:
    def helper(self):
        pass

    async def test_target(self, resource):
        assert resource is not None
'''
        self.assertEqual(validate_initial_generation(source), extract_code(source))

    def test_rejects_multiple_or_missing_static_test_shapes(self):
        multiple = 'def test_one():\n    assert True\n\ndef test_two():\n    assert True\n'
        missing = 'def helper():\n    return 1\n'
        with self.assertRaisesRegex(OutputContractError, 'exactly one'):
            validate_initial_generation(multiple)
        with self.assertRaisesRegex(OutputContractError, 'no statically test-shaped'):
            validate_initial_generation(missing)

    def test_rejects_unclosed_fence_and_malformed_python(self):
        with self.assertRaises(OutputContractError):
            validate_initial_generation('```python\ndef test_x():\n    assert True\n')
        with self.assertRaisesRegex(OutputContractError, 'malformed'):
            validate_initial_generation('def test_x(:\n    assert True\n')

    def test_non_generation_calls_are_unmodified_and_repairs_have_no_one_test_limit(self):
        for operation in ('initialization', 'judge_params', 'generate_meaning',
                          'generate_repair_query', 'summary_query'):
            self.assertEqual(
                append_prompt_contract('system', 'user', operation),
                ('system', 'user'),
            )
        existing = (
            'def test_first():\n    assert 1 == 1\n\n'
            'def test_second():\n    assert 2 == 2\n'
        )
        system, repair = append_prompt_contract('system', existing, 'repair_assert_error')
        self.assertEqual(system, 'system')
        self.assertIn('Preserve every existing test', repair)
        self.assertIn('does not impose a one-test limit', repair)
        self.assertNotIn('exactly one complete pytest test', repair)
        self.assertTrue(repair.startswith(existing))


class BackendOutputContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)

    def backend(self, output, output_tokens=8, max_new_tokens=32, policy=POLICY):
        from pilot.backend import TransformersBackend

        class Batch(dict):
            input_ids = types.SimpleNamespace(shape=(1, 4))

            def __init__(self):
                super().__init__(input_ids=self.input_ids)

            def to(self, device):
                return self

        class Generated:
            def __init__(self, count):
                self.tokens = [1] * count

            def __getitem__(self, key):
                return self.tokens

        class Cuda:
            @staticmethod
            def memory_allocated(): return 0
            @staticmethod
            def memory_reserved(): return 0
            @staticmethod
            def max_memory_allocated(): return 0
            @staticmethod
            def is_available(): return True
            @staticmethod
            def empty_cache(): pass

        class FakeTokenizer:
            eos_token_id = 0

            def __init__(self):
                self.seen_messages = None

            def apply_chat_template(self, messages, **kwargs):
                self.seen_messages = messages
                return Batch()

            def decode(self, generated, **kwargs):
                return output

        obj = object.__new__(TransformersBackend)
        obj.settings = dict(max_new_tokens=max_new_tokens, max_input_tokens=100,
                            max_sequence_tokens=200, generation={'do_sample': False},
                            attention_policy='auto', test_output_contract=policy)
        obj.work = self.work
        obj.phase = 'generation_round_1'
        obj.profile = {}
        obj.call_count = obj.calls_finished = obj.calls_failed = 0
        obj.input_tokens = obj.output_tokens = 0
        obj.fresh_input_tokens = obj.fresh_output_tokens = 0
        obj.tokenizer = FakeTokenizer()
        obj.model = types.SimpleNamespace(device='cuda:0', generate=lambda **kwargs: Generated(output_tokens))
        obj.torch = types.SimpleNamespace(inference_mode=nullcontext, cuda=Cuda())
        return obj

    @staticmethod
    def operation(name):
        namespace = {'__name__': 'test4dt.contract_fixture'}
        exec(f'async def {name}(backend):\n    return await backend.ask("system", "user")', namespace)
        return namespace[name]

    def call(self, backend, operation='generate_test_case_normal'):
        return asyncio.run(self.operation(operation)(backend))

    def records(self):
        return [json.loads(line) for line in (self.work / 'model_calls.jsonl').read_text().splitlines()]

    def test_prompt_is_augmented_before_tokenization_and_answer_is_verbatim(self):
        answer = '```python\ndef test_target():\n    assert 1 == 1\n```'
        backend = self.backend(answer)
        self.assertEqual(self.call(backend), answer)
        messages = backend.tokenizer.seen_messages
        self.assertIn('exactly one complete pytest test', messages[1]['content'])
        record, = self.records()
        self.assertEqual(record['output_contract_applied'], POLICY + ':generation')
        self.assertEqual(record['messages'], messages)

    def test_initialization_is_unchanged_even_for_generation_operation(self):
        backend = self.backend('summary')
        backend.phase = 'initialization'
        self.assertEqual(self.call(backend), 'summary')
        self.assertEqual(backend.tokenizer.seen_messages[1]['content'], 'user')
        self.assertIsNone(self.records()[0]['output_contract_applied'])

    def test_missing_policy_keeps_legacy_output_behavior(self):
        answer = '```python\ndef test_one():\n    assert True\ndef test_two():\n    assert True\n```'
        backend = self.backend(answer, policy=None)
        self.assertEqual(self.call(backend), answer)
        self.assertNotIn('exactly one complete pytest test', backend.tokenizer.seen_messages[1]['content'])
        self.assertIsNone(self.records()[0]['output_contract_applied'])

    def test_multiple_test_shapes_and_truncated_generation_are_logged_then_rejected(self):
        answer = '```python\ndef test_one():\n    assert True\ndef test_two():\n    assert True\n```'
        backend = self.backend(answer)
        with self.assertRaisesRegex(OutputContractError, 'exactly one statically'):
            self.call(backend)
        record, = self.records()
        self.assertEqual(record['output'], answer)
        self.assertIn('exactly one complete pytest test', record['messages'][1]['content'])
        self.assertIn('error', record)
        self.assertEqual(backend.fresh_output_tokens, 8)

        self.work = Path(self.tmp.name) / 'capped-generation'
        self.work.mkdir()
        capped = '```python\ndef test_target():\n    assert True\n```'
        backend = self.backend(capped, output_tokens=32, max_new_tokens=32)
        with self.assertRaisesRegex(OutputContractError, 'rejects capped'):
            self.call(backend)
        record, = self.records()
        self.assertTrue(record['truncated'])
        self.assertEqual(record['output'], capped)
        self.assertEqual(backend.fresh_output_tokens, 32)

    def test_repair_allows_multiple_tests_but_requires_complete_syntax_and_rejects_cap(self):
        answer = '```python\ndef test_one():\n    assert True\ndef test_two():\n    assert True\n```'
        backend = self.backend(answer)
        self.assertEqual(self.call(backend, 'repair_assert_error'), answer)
        record, = self.records()
        self.assertEqual(record['output_contract_applied'], POLICY + ':repair')

        malformed = '```python\ndef test_one(:\n```'
        self.work = Path(self.tmp.name) / 'malformed-repair'
        self.work.mkdir()
        backend = self.backend(malformed)
        with self.assertRaisesRegex(OutputContractError, 'malformed'):
            self.call(backend, 'repair_syntax_error')
        record, = self.records()
        self.assertEqual(record['output'], malformed)

        self.work = Path(self.tmp.name) / 'capped-repair'
        self.work.mkdir()
        backend = self.backend(answer, output_tokens=32, max_new_tokens=32)
        with self.assertRaisesRegex(OutputContractError, 'rejects capped'):
            self.call(backend, 'repair_assert_error')
        record, = self.records()
        self.assertTrue(record['truncated'])
        self.assertEqual(record['output'], answer)

    def test_unknown_policy_fails_clearly_before_model_loading(self):
        from pilot.backend import TransformersBackend
        with self.assertRaisesRegex(ValueError, 'Unknown test output contract policy'):
            TransformersBackend({'test_output_contract': 'future-unknown'}, self.work)

    def test_non_code_upstream_operations_are_not_augmented_or_validated(self):
        for index, operation in enumerate(('judge_params', 'generate_meaning',
                                             'generate_repair_query', 'summary_query')):
            with self.subTest(operation=operation):
                self.work = Path(self.tmp.name) / f'non-code-{index}'
                self.work.mkdir()
                backend = self.backend('plain response')
                self.assertEqual(self.call(backend, operation), 'plain response')
                self.assertEqual(backend.tokenizer.seen_messages[1]['content'], 'user')
                self.assertIsNone(self.records()[0]['output_contract_applied'])
        self.assertTrue(issubclass(OutputContractError, ValueError))


if __name__ == '__main__':
    unittest.main()
