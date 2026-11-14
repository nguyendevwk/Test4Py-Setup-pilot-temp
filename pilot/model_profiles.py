"""Source-backed candidates; profiles are hypotheses, not measured model rankings."""
DEFAULT_MODEL = 'Qwen/Qwen3-4B-Instruct-2507'
PROFILES = {
    'Nanbeige/Nanbeige4.1-3B': dict(name='nanbeige-2026-3b', publisher='Nanbeige LLM Lab', license='apache-2.0',
        model_kind='post-trained-reasoning', publication_date='2026-02-13', max_new_tokens=8192, use_fast=False,
        eos_token_id=166101, paper='https://arxiv.org/abs/2602.13367',
        card='https://huggingface.co/Nanbeige/Nanbeige4.1-3B', reasoning=True),
    'Qwen/Qwen3-4B-Instruct-2507': dict(name='qwen3-nonthinking-control', publisher='Qwen', license='apache-2.0',
        model_kind='instruct-nonthinking', max_new_tokens=2048,
        use_fast=True, paper='https://arxiv.org/abs/2505.09388',
        card='https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507', reasoning=False),
    'Qwen/Qwen2.5-Coder-3B-Instruct': dict(name='code-specialist-3b', publisher='Qwen', license='qwen-research',
        model_kind='code-instruct', max_new_tokens=2048, use_fast=True, reasoning=False,
        paper='https://arxiv.org/abs/2409.12186', card='https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct'),
    'Qwen/Qwen2.5-Coder-1.5B-Instruct': dict(name='historical-1.5b', publisher='Qwen', license='apache-2.0',
        model_kind='code-instruct', max_new_tokens=2048,
        use_fast=True, paper='https://arxiv.org/abs/2409.12186',
        card='https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct', reasoning=False),
}

def profile(model):
    if model.startswith('Qwen/Qwen3.5'):
        raise ValueError('Qwen3.5 requires a separately validated architecture/runtime adapter; current causal-LM backend is not validated.')
    return dict(PROFILES.get(model, dict(name='custom-unvalidated', max_new_tokens=2048, use_fast=True)))
