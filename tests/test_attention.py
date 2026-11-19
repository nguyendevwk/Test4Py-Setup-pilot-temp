import sys
import types
import unittest
from contextlib import contextmanager
from unittest.mock import patch

from pilot.attention import POLICY, configure_attention, generation_attention_context


class AttentionTests(unittest.TestCase):
    def test_hf_repeat_kv_preserves_attention_result_on_cpu(self):
        import torch
        from transformers.integrations import sdpa_attention
        torch.manual_seed(19)
        q=torch.randn(1,4,7,8);k=torch.randn(1,2,7,8);v=torch.randn(1,2,7,8)
        expected=torch.nn.functional.scaled_dot_product_attention(
            q,k.repeat_interleave(2,dim=1),v.repeat_interleave(2,dim=1),is_causal=True)
        original=sdpa_attention.use_gqa_in_sdpa
        try:
            configure_attention(dict(attention_policy=POLICY))
            module=types.SimpleNamespace(num_key_value_groups=2,is_causal=True)
            actual,_=sdpa_attention.sdpa_attention_forward(module,q,k,v,None)
            torch.testing.assert_close(actual,expected.transpose(1,2).contiguous())
        finally:
            sdpa_attention.use_gqa_in_sdpa=original

    def test_efficiency_policy_disables_native_gqa_without_changing_cpu_backend_flags(self):
        integration=types.ModuleType('transformers.integrations')
        integration.sdpa_attention=types.SimpleNamespace(use_gqa_in_sdpa=lambda *a:True)
        with patch.dict(sys.modules,{'transformers.integrations':integration}):
            self.assertEqual(configure_attention(dict(attention_policy=POLICY)),dict(attn_implementation='sdpa'))
            self.assertFalse(integration.sdpa_attention.use_gqa_in_sdpa(None,object()))
        calls=[]
        @contextmanager
        def kernel(**kwargs):
            calls.append(kwargs);yield
        attention=types.ModuleType('torch.nn.attention')
        attention.SDPBackend=types.SimpleNamespace(EFFICIENT_ATTENTION='efficient')
        attention.sdpa_kernel=kernel
        with patch.dict(sys.modules,{'torch.nn.attention':attention}):
            with generation_attention_context(dict(attention_policy=POLICY)):
                self.assertEqual(calls,[dict(backends=['efficient'])])
        self.assertEqual(configure_attention({}),{})
        with self.assertRaises(ValueError):configure_attention(dict(attention_policy='unknown'))

