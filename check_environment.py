"""Dependency smoke check: CPU-safe and does not download models."""
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import sys


def main():
    if not (3, 10) <= sys.version_info[:2] <= (3, 12):
        raise SystemExit('Pilot requires Python 3.10–3.12. Run python bootstrap_kaggle.py --venv /tmp/test4py-venv and use /tmp/test4py-venv/bin/python.')
    os.environ.setdefault('ANONYMIZED_TELEMETRY', 'False')
    # Import paths used by upstream; catches tokenizers, NumPy/Chroma ABI issues.
    for name in ['torch', 'numpy', 'transformers', 'chromadb', 'langchain_core',
                 'openai', 'pytest', 'pytest_jsonreport', 'coverage', 'pylint', 'pkg_resources']:
        importlib.import_module(name)
    import torch
    from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer
    import chromadb
    client = chromadb.EphemeralClient()
    collection = client.create_collection('pilot_environment_smoke')
    collection.add(ids=['a', 'b'], embeddings=[[1., 0., 0.], [0., 1., 0.]])
    assert collection.query(query_embeddings=[[1., 0., 0.]], n_results=1)['ids'] == [['a']]
    client.delete_collection('pilot_environment_smoke')
    report = dict(python=platform.python_version(), executable=sys.executable,
                  cuda_available=torch.cuda.is_available(), torch_cuda=torch.version.cuda,
                  packages={d.metadata['Name']: d.version for d in importlib.metadata.distributions()})
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
