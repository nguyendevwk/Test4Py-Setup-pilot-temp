"""Shared Transformers backend for every upstream LLM call."""
import inspect
import os
import time
from pilot.common import append_json
from pilot.progress import emit
from pilot.model_profiles import profile
from pilot.quality import final_answer


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
        self.call_count = 0
        self.calls_finished = 0
        self.calls_failed = 0
        self.input_tokens = 0
        self.output_tokens = 0
        torch.set_num_threads(settings.get('cpu_threads', 1))
        emit(work, 'model_load', 'start', gpu=os.environ.get('CUDA_VISIBLE_DEVICES', 'inherited'))
        torch.manual_seed(settings['seed'])
        self.profile = profile(settings['model'])
        opts = dict(revision=settings['model_revision'])
        self.tokenizer = AutoTokenizer.from_pretrained(settings['model'], use_fast=self.profile.get('use_fast',True), **opts)
        
        # Check if 4-bit quantization is needed for 7B+ models on 15GB GPUs
        model_str = settings['model'].lower()
        is_large = any(s in model_str for s in ["7b", "8b", "14b", "32b"])
        if is_large and torch.cuda.is_available():
            try:
                from transformers import BitsAndBytesConfig
                bnb_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_use_double_quant=True,
                )
                self.model = AutoModelForCausalLM.from_pretrained(
                    settings['model'],
                    quantization_config=bnb_config,
                    device_map={"": "cuda:0"},
                    **opts
                ).eval()
                print(f"[Backend] Auto 4-bit NF4 enabled for {settings['model']} to prevent CUDA OOM.")
            except Exception as e:
                print(f"[Backend] 4-bit fallback: {e}")
                self.model = AutoModelForCausalLM.from_pretrained(
                    settings['model'], torch_dtype=torch.float16, **opts).to('cuda:0').eval()
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                settings['model'], torch_dtype=torch.float16, **opts).to('cuda:0').eval()
        self.versions = dict(torch=torch.__version__, transformers=transformers.__version__,
                             gpu=torch.cuda.get_device_name(0),
                             loaded_model_revision=getattr(self.model.config, '_commit_hash', None))
        emit(work, 'model_load', 'ready', allocated_gib=round(torch.cuda.memory_allocated()/1024**3, 2))
        torch.cuda.reset_peak_memory_stats()
        actual = self.versions['loaded_model_revision']
        if actual and actual != settings['model_revision']:
            raise RuntimeError(f'Model revision mismatch: {actual}')

    async def ask(self, system, user):
        # No await during inference: upstream concurrent tasks serialize on one GPU.
        callers = []
        upstream_role = None
        frame = inspect.currentframe().f_back
        while frame is not None:
            callers.append(frame.f_code.co_name)
            if upstream_role is None and frame.f_globals.get('__name__', '').startswith('test4dt'):
                upstream_role = frame.f_code.co_name
            frame = frame.f_back
        role = upstream_role or next((name for name in callers if name.startswith(('repair_', 'generate_test_case'))), None)
        messages = [dict(role='system', content=system), dict(role='user', content=user)]
        inputs = self.tokenizer.apply_chat_template(messages, tokenize=True,
                    add_generation_prompt=True, return_tensors='pt', return_dict=True).to(self.model.device)
        start = time.perf_counter()
        record = dict(phase=self.phase, upstream_operation=role, messages=messages,
                      input_tokens=int(inputs.input_ids.shape[1]))
        self.call_count += 1
        emit(self.work, self.phase, 'model_call_start', call=self.call_count, operation=role,
             input_tokens=record['input_tokens'], max_new_tokens=self.settings['max_new_tokens'],
             model_calls_started=self.call_count, model_calls_finished=self.calls_finished)
        try:
            generation = self.settings.get('generation', {})
            sampling = dict(do_sample=bool(generation.get('do_sample',False)))
            if sampling['do_sample']:
                sampling.update(temperature=generation.get('temperature',.6), top_p=generation.get('top_p',.95))
            with self.torch.inference_mode():
                result = self.model.generate(**inputs, **sampling,
                    max_new_tokens=self.settings['max_new_tokens'],
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.profile.get('eos_token_id', self.tokenizer.eos_token_id))
            generated = result[0, inputs.input_ids.shape[1]:]
            output = self.tokenizer.decode(generated, skip_special_tokens=True)
            answer, answer_status = final_answer(output)
            record.update(output=output, final_answer=answer, answer_status=answer_status, output_tokens=len(generated),
                          truncated=len(generated) == self.settings['max_new_tokens'])
            if not answer:
                raise ValueError('Model produced no complete final answer; inspect raw model log and token budget')
            return answer
        except Exception as exc:
            record['error'] = repr(exc)
            record.setdefault('output_tokens', 0)
            raise
        finally:
            record['seconds'] = time.perf_counter() - start
            record['output_tokens_per_second'] = record.get('output_tokens', 0) / max(record['seconds'], 1e-9)
            record['allocated_gib'] = self.torch.cuda.memory_allocated()/1024**3
            record['reserved_gib'] = self.torch.cuda.memory_reserved()/1024**3
            record['peak_allocated_gib'] = self.torch.cuda.max_memory_allocated()/1024**3
            self.calls_finished += 1
            self.calls_failed += int('error' in record)
            self.input_tokens += record['input_tokens']
            self.output_tokens += record.get('output_tokens', 0)
            if self.torch.cuda.is_available():
                self.torch.cuda.empty_cache()
            import gc
            gc.collect()
            append_json(self.work / 'model_calls.jsonl', record)
            emit(self.work, self.phase, 'model_call_end', call=self.call_count,
                 model_calls_started=self.call_count, model_calls_finished=self.calls_finished,
                 model_calls_failed=self.calls_failed, seconds=round(record['seconds'], 2), output_tokens=record.get('output_tokens', 0),
                 tokens_per_second=round(record['output_tokens_per_second'], 2),
                 total_input_tokens=self.input_tokens, total_output_tokens=self.output_tokens,
                 allocated_gib=round(record['allocated_gib'], 2), reserved_gib=round(record['reserved_gib'], 2),
                 error=record.get('error'))
