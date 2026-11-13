"""Shared Transformers backend for every upstream LLM call."""
import inspect
import time
from pilot.common import append_json


class TransformersBackend:
    def __init__(self, settings, work):
        import torch
        import transformers
        from transformers import AutoModelForCausalLM, AutoTokenizer
        if not torch.cuda.is_available():
            raise RuntimeError('GPU unavailable: enable GPU in Kaggle/Colab')
        self.torch = torch
        self.settings, self.work = settings, work
        self.phase = 'initialization'
        torch.manual_seed(settings['seed'])
        opts = dict(revision=settings['model_revision'])
        self.tokenizer = AutoTokenizer.from_pretrained(settings['model'], **opts)
        self.model = AutoModelForCausalLM.from_pretrained(
            settings['model'], torch_dtype=torch.float16, **opts).to('cuda:0').eval()
        self.versions = dict(torch=torch.__version__, transformers=transformers.__version__,
                             gpu=torch.cuda.get_device_name(0),
                             loaded_model_revision=getattr(self.model.config, '_commit_hash', None))
        actual = self.versions['loaded_model_revision']
        if actual and actual != settings['model_revision']:
            raise RuntimeError(f'Model revision mismatch: {actual}')

    async def ask(self, system, user):
        # No await during inference: upstream concurrent tasks serialize on one GPU.
        callers = [frame.function for frame in inspect.stack()]
        role = next((name for name in callers if name.startswith(('repair_', 'generate_test_case'))), None)
        messages = [dict(role='system', content=system), dict(role='user', content=user)]
        inputs = self.tokenizer.apply_chat_template(messages, tokenize=True,
                    add_generation_prompt=True, return_tensors='pt', return_dict=True).to(self.model.device)
        start = time.perf_counter()
        record = dict(phase=self.phase, upstream_operation=role, messages=messages,
                      input_tokens=int(inputs.input_ids.shape[1]))
        try:
            with self.torch.inference_mode():
                result = self.model.generate(**inputs, do_sample=False,
                    max_new_tokens=self.settings['max_new_tokens'],
                    pad_token_id=self.tokenizer.eos_token_id)
            generated = result[0, inputs.input_ids.shape[1]:]
            output = self.tokenizer.decode(generated, skip_special_tokens=True)
            record.update(output=output, output_tokens=len(generated),
                          truncated=len(generated) == self.settings['max_new_tokens'])
            return output
        except Exception as exc:
            record.update(error=repr(exc), output_tokens=0)
            raise
        finally:
            record['seconds'] = time.perf_counter() - start
            append_json(self.work / 'model_calls.jsonl', record)
