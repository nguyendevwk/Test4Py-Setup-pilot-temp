"""Explicit T4 runtime adapter, common to both experimental arms.

HF 4.57 SDPA may request native GQA, which can select the quadratic math path.
Use HF's existing repeat_kv branch and require PyTorch efficient attention during
CUDA generation. CPU embeddings keep their normal SDPA backend selection.
"""
from contextlib import nullcontext

POLICY = 't4-efficient-sdpa-v1'


def configure_attention(settings):
    policy=settings.get('attention_policy','auto')
    if policy=='auto':
        return {}
    if policy!=POLICY:
        raise ValueError('Unknown attention policy: '+str(policy))
    from transformers.integrations import sdpa_attention
    # This selects HF's own repeat_kv implementation, without editing model weights
    # or installed source. The patch is confined to this isolated worker process.
    sdpa_attention.use_gqa_in_sdpa=lambda attention_mask,key:False
    return dict(attn_implementation='sdpa')


def generation_attention_context(settings):
    if settings.get('attention_policy','auto')=='auto':
        return nullcontext()
    if settings['attention_policy']!=POLICY:
        raise ValueError('Unknown attention policy')
    from torch.nn.attention import SDPBackend, sdpa_kernel
    # No silent math/FP16-model fallback. Unsupported kernels fail the stress gate.
    return sdpa_kernel(backends=[SDPBackend.EFFICIENT_ATTENTION])
