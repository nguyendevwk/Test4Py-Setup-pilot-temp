"""Fail-closed model loading and token limits, shared by upstream experiments."""


def load_causal_model(settings, torch, model_class, quantization_class):
    model_name = settings['model']
    default_nf4 = any(s in model_name.lower() for s in ('7b', '8b', '14b', '32b'))
    mode = settings.get('quantization', 'nf4' if default_nf4 else 'none')
    if mode not in ('nf4', 'none'):
        raise ValueError('quantization must be nf4 or none')
    opts = dict(revision=settings['model_revision'], device_map={'': 'cuda:0'},
                torch_dtype=torch.float16, low_cpu_mem_usage=True)
    from pilot.attention import configure_attention
    opts.update(configure_attention(settings))
    if mode == 'nf4':
        opts['quantization_config'] = quantization_class(load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16, bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True)
    else:
        opts['torch_dtype'] = torch.float16
    # Never retry with FP16, CPU offload, another model or a different revision.
    model = model_class.from_pretrained(model_name, **opts).eval()
    if any(str(device) in ('cpu', 'disk') for device in getattr(model, 'hf_device_map', {}).values()):
        raise RuntimeError('Unexpected CPU/disk offload; configure and calibrate it explicitly')
    if mode == 'nf4' and not getattr(model, 'is_loaded_in_4bit', False):
        raise RuntimeError('Requested NF4 but model does not report 4-bit loading')
    return model, mode


def check_token_budget(input_tokens, settings):
    output_tokens = settings['max_new_tokens']
    if input_tokens > settings.get('max_input_tokens', 10**12):
        raise ValueError(f'Input budget exceeded: {input_tokens}; no silent truncation')
    if input_tokens + output_tokens > settings.get('max_sequence_tokens', 10**12):
        raise ValueError(f'Sequence budget exceeded: {input_tokens}+{output_tokens}; no silent truncation')
