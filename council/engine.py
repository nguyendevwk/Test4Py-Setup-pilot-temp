"""Pinned inference, with raw prompts/completions and token accounting."""
from pathlib import Path
import time
from pilot.common import append_json, write_json


class CouncilEngine:
    def __init__(self, coder_model='Qwen/Qwen2.5-Coder-7B-Instruct',
                 critic_model='Qwen/Qwen3-4B-Instruct-2507', coder_device=None,
                 critic_device=None, max_new_tokens=512, mock=False, load_in_4bit=False,
                 coder_revision='main', critic_revision='main', seed=42,
                 enable_critic=True, work=None, temperature=0.0, top_p=0.95):
        self.mock, self.load_in_4bit = mock, load_in_4bit
        self.work = Path(work) if work else None
        self.enable_critic, self.max_new_tokens = enable_critic, max_new_tokens
        self.temperature, self.top_p = float(temperature), float(top_p)
        self.telemetry = {f'{r}_{k}': 0 for r in ('coder', 'critic')
                          for k in ('calls', 'input_tokens', 'tokens', 'seconds')}
        self.versions = dict(mock=mock, seed=seed, models={})
        if mock:
            self.coder_device = self.critic_device = 'cpu'
            return
        import torch
        import transformers
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from huggingface_hub import HfApi
        torch.manual_seed(seed)
        self.versions.update(torch=torch.__version__, transformers=transformers.__version__, cuda=torch.version.cuda)
        count = torch.cuda.device_count()
        self.coder_device = coder_device or ('cuda:0' if count else 'cpu')
        self.critic_device = critic_device or ('cuda:1' if count > 1 else self.coder_device)
        for role, name, requested in (('coder', coder_model, coder_revision), ('critic', critic_model, critic_revision)):
            if role == 'critic' and not enable_critic:
                continue
            device = getattr(self, role+'_device')
            try:
                revision = HfApi().model_info(name, revision=requested).sha
            except Exception as e:
                print(f"[Council WARNING] Could not resolve SHA for {name} via HF API: {e}; falling back to {requested}", flush=True)
                revision = requested
            record = dict(name=name, requested_revision=requested, revision=revision, device=device,
                          quantization='nf4' if load_in_4bit and 'cuda' in device else None)
            self.versions['models'][role] = record
            if self.work:
                write_json(self.work/'engine.json', self.versions)
            opts = dict(device_map={'': device})
            if revision != 'main':
                opts['revision'] = revision
            if record['quantization']:
                from transformers import BitsAndBytesConfig
                opts['quantization_config'] = BitsAndBytesConfig(load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16, bnb_4bit_quant_type='nf4', bnb_4bit_use_double_quant=True)
            else:
                opts['torch_dtype'] = torch.float16 if 'cuda' in device else torch.float32
            print(f'[Council] Loading {role}: {name}@{revision} on {device}', flush=True)
            setattr(self, role+'_tokenizer', AutoTokenizer.from_pretrained(name, revision=revision, use_fast=True))
            setattr(self, role+'_model', AutoModelForCausalLM.from_pretrained(name, **opts).eval())
            if 'cuda' in device:
                record['gpu'] = torch.cuda.get_device_name(device)
            if self.work:
                write_json(self.work/'engine.json', self.versions)

    def snapshot(self):
        if not self.mock:
            import torch
            self.versions['memory'] = {device: dict(
                peak_allocated_gib=torch.cuda.max_memory_allocated(device)/1024**3,
                reserved_gib=torch.cuda.memory_reserved(device)/1024**3)
                for device in {getattr(self, role+'_device') for role in self.versions['models']}
                if 'cuda' in device}
        return self.versions

    def _call(self, role, system, user):
        if role == 'critic' and not self.enable_critic:
            raise RuntimeError('Critic disabled')
        start = time.perf_counter()
        record = dict(role=role, mock=self.mock, sample_id=getattr(self, 'sample_id', None), messages=[dict(role='system', content=system), dict(role='user', content=user)])
        self.telemetry[role+'_calls'] += 1
        try:
            if self.mock:
                record.update(output='```python\ndef test_mock():\n    assert True\n```', input_tokens=None, output_tokens=None)
            else:
                import torch
                tokenizer, model = getattr(self, role+'_tokenizer'), getattr(self, role+'_model')
                inputs = tokenizer.apply_chat_template(record['messages'], tokenize=True,
                    add_generation_prompt=True, return_tensors='pt', return_dict=True).to(getattr(self, role+'_device'))
                length = inputs.input_ids.shape[1]
                record['input_tokens'] = length
                self.telemetry[role+'_input_tokens'] += length
                with torch.inference_mode():
                    gen_opts = dict(max_new_tokens=self.max_new_tokens, pad_token_id=tokenizer.eos_token_id)
                    if self.temperature > 0.0:
                        gen_opts.update(do_sample=True, temperature=self.temperature, top_p=self.top_p)
                    else:
                        gen_opts.update(do_sample=False)
                    output = model.generate(**inputs, **gen_opts)
                ids = output[0, length:]
                record.update(output=tokenizer.decode(ids, skip_special_tokens=True), output_tokens=len(ids),
                              truncated=len(ids) == self.max_new_tokens)
                self.telemetry[role+'_tokens'] += len(ids)
            return record['output']
        except Exception as exc:
            record['error'] = repr(exc)
            raise
        finally:
            record['seconds'] = time.perf_counter()-start
            self.telemetry[role+'_seconds'] += record['seconds']
            if self.work:
                append_json(self.work/'model_calls.jsonl', record)
            if not self.mock:
                try:
                    import torch, gc
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                    gc.collect()
                except Exception:
                    pass

    def call_coder(self, system_prompt, user_prompt):
        return self._call('coder', system_prompt, user_prompt)

    def call_critic(self, system_prompt, user_prompt):
        return self._call('critic', system_prompt, user_prompt)
