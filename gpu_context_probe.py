"""Synthetic KV/prefill/decode stress, NOT test-generation efficacy evidence."""
import argparse
import json
from pathlib import Path
import sys
import time
import traceback

from pilot.backend import TransformersBackend
from pilot.common import write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--settings', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--inputs', default='2048,4096,6144')
    parser.add_argument('--output-tokens', type=int, default=1024)
    parser.add_argument('--headroom-gib', type=float, default=1.5)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    config = json.loads(args.settings.read_text())
    lengths = [int(n) for n in args.inputs.split(',')]
    if not lengths or min(lengths) < 1 or args.output_tokens < 1:
        parser.error('positive input/output lengths required')
    results = dict(kind='synthetic_memory_stress_not_efficacy', status='running', tests=[], settings=config,
                   margin_gib=args.headroom_gib, policy='forced full-length decode; no context-fit inference from load alone')
    backend = None
    try:
        backend = TransformersBackend(config, args.output)
        torch = backend.torch
        # Tokens are repeatable synthetic source text, not claimed to be real upstream prompts.
        token_ids = backend.tokenizer.encode('def example(value):\n    return value\n', add_special_tokens=False)
        for length in lengths + [max(lengths)]:
            from pilot.runtime_limits import check_token_budget
            check_token_budget(length, dict(config,max_new_tokens=args.output_tokens))
            started = time.perf_counter()
            print(f'[stress-probe] input={length} output={args.output_tokens} attention={config.get("attention_policy","auto")}',flush=True)
            total = torch.cuda.get_device_properties(0).total_memory
            torch.cuda.reset_peak_memory_stats()
            ids = torch.tensor([(token_ids*((length//len(token_ids))+1))[:length]], dtype=torch.long, device='cuda:0')
            mask = torch.ones_like(ids)
            from pilot.attention import generation_attention_context
            with torch.inference_mode(), generation_attention_context(config):
                out = backend.model.generate(input_ids=ids, attention_mask=mask, do_sample=False,
                       min_new_tokens=args.output_tokens, max_new_tokens=args.output_tokens,
                       pad_token_id=backend.tokenizer.eos_token_id)
            torch.cuda.synchronize()
            measured = out.shape[1]-length
            free, _ = torch.cuda.mem_get_info()
            peak_reserved = torch.cuda.max_memory_reserved()
            # Reserve-based margin plus actual free memory account for allocator/external usage.
            margin = min(free, total-peak_reserved)/1024**3
            results['tests'].append(dict(input_tokens=length, output_tokens=measured,
                allocated_gib=torch.cuda.memory_allocated()/1024**3,
                peak_allocated_gib=torch.cuda.max_memory_allocated()/1024**3,
                peak_reserved_gib=peak_reserved/1024**3, free_gib=free/1024**3,
                conservative_headroom_gib=margin, seconds=time.perf_counter()-started,
                passed=measured == args.output_tokens and margin >= args.headroom_gib))
            del ids, mask, out
            torch.cuda.empty_cache()
            write_json(args.output/'probe.json', results)
        results['versions'] = backend.versions
        results['status'] = 'passed' if all(t['passed'] for t in results['tests']) else 'insufficient_headroom'
    except Exception as exc:
        results.update(status='failed', error=repr(exc), traceback=traceback.format_exc())
        print('[stress-probe ERROR] '+repr(exc),flush=True)
    finally:
        write_json(args.output/'probe.json', results)
    print(json.dumps(results, indent=2), flush=True)
    return 0 if results['status'] == 'passed' else 2


if __name__ == '__main__':
    sys.exit(main())
