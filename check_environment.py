"""Dependency smoke check: CPU-safe and does not download models."""
import argparse
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import sys
from pilot.common import package_versions, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', choices=('legacy', 'modern'), default='legacy')
    parser.add_argument('--report', type=Path, help='write complete metadata here; console stays concise')
    args = parser.parse_args()
    lower, upper = ((3, 11), (3, 13)) if args.runtime == 'modern' else ((3, 10), (3, 12))
    if not lower <= sys.version_info[:2] <= upper:
        raise SystemExit('Pilot requires Python 3.10–3.12. Run python bootstrap_kaggle.py --venv /tmp/test4py-venv and use /tmp/test4py-venv/bin/python.')
    os.environ.setdefault('USE_TF', '0')
    os.environ.setdefault('USE_FLAX', '0')
    os.environ.setdefault('ANONYMIZED_TELEMETRY', 'False')
    # Import paths used by upstream; catches tokenizers, NumPy/Chroma ABI issues.
    for name in ['torch', 'numpy', 'transformers', 'chromadb', 'langchain_core',
                 'openai', 'pytest', 'pytest_jsonreport', 'coverage', 'pylint', 'pkg_resources']:
        importlib.import_module(name)
    import torch
    from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer, BertConfig, Qwen2Config
    # Exercise actual text-model class imports without downloading weights.
    with torch.inference_mode():
        tiny_lm = AutoModelForCausalLM.from_config(Qwen2Config(vocab_size=32, hidden_size=8,
            intermediate_size=16, num_hidden_layers=1, num_attention_heads=2, num_key_value_heads=2)).eval()
        assert tiny_lm(torch.tensor([[1, 2]])).logits.shape == (1, 2, 32)
        tiny_embedding = AutoModel.from_config(BertConfig(vocab_size=32, hidden_size=8,
            intermediate_size=16, num_hidden_layers=1, num_attention_heads=2)).eval()
        assert tiny_embedding(torch.tensor([[1, 2]])).last_hidden_state.shape == (1, 2, 8)
    import chromadb
    client = chromadb.EphemeralClient()
    collection = client.create_collection('pilot_environment_smoke')
    collection.add(ids=['a', 'b'], embeddings=[[1., 0., 0.], [0., 1., 0.]])
    assert collection.query(query_embeddings=[[1., 0., 0.]], n_results=1)['ids'] == [['a']]
    client.delete_collection('pilot_environment_smoke')
    report = dict(runtime=args.runtime, python=platform.python_version(), executable=sys.executable,
                  cuda_available=torch.cuda.is_available(), torch_cuda=torch.version.cuda,
                  packages=package_versions())
    if args.report:
        write_json(args.report, report)
    summary = {key: report[key] for key in ('runtime', 'python', 'executable', 'cuda_available', 'torch_cuda')}
    summary['packages'] = {name: importlib.metadata.version(name) for name in
                           ('torch', 'transformers', 'tokenizers', 'chromadb', 'numpy')}
    summary['full_report'] = str(args.report) if args.report else None
    print('Environment smoke check passed: ' + json.dumps(summary))
    return 0


if __name__ == '__main__':
    sys.exit(main())
