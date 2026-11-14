"""Source-backed candidates; profiles are hypotheses, not measured model rankings."""
DEFAULT_MODEL = 'Nanbeige/Nanbeige4.1-3B'
PROFILES = {
    DEFAULT_MODEL: dict(name='nanbeige-2026-3b', max_new_tokens=8192, use_fast=False,
        eos_token_id=166101, paper='https://arxiv.org/abs/2602.13367',
        card='https://huggingface.co/Nanbeige/Nanbeige4.1-3B', reasoning=True),
    'Qwen/Qwen3-4B-Instruct-2507': dict(name='qwen3-nonthinking-control', max_new_tokens=2048,
        use_fast=True, paper='https://arxiv.org/abs/2505.09388',
        card='https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507', reasoning=False),
    'Qwen/Qwen2.5-Coder-1.5B-Instruct': dict(name='historical-1.5b', max_new_tokens=2048,
        use_fast=True, paper='https://arxiv.org/abs/2409.12186',
        card='https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct', reasoning=False),
}

def profile(model):
    if model.startswith('Qwen/Qwen3.5'):
        raise ValueError('Qwen3.5 requires a separately validated architecture/runtime adapter; current causal-LM backend is not validated.')
    return dict(PROFILES.get(model, dict(name='custom-unvalidated', max_new_tokens=2048, use_fast=True)))
