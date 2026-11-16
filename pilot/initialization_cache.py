"""Exact-prompt cache for GREEDY pre-generation calls only, shared by both arms.

No generation, repair, outcome or mutant-based cache. Corruption fails closed.
Cache reuse is an engineering adaptation, not evidence that summaries are true.
"""
from contextlib import contextmanager
import fcntl
import json
from pathlib import Path
from pilot.common import digest, write_json


def cache_key(settings, versions, messages):
    return digest(dict(policy='greedy-initialization-prefix-v1', model=settings['model'],
        revision=settings['model_revision'], embedding_revision=settings.get('embedding_revision'),
        quantization=settings.get('quantization'), max_new_tokens=settings['max_new_tokens'],
        source_policy=settings.get('adapter_source_hash'), versions=versions,messages=messages))


@contextmanager
def entry(directory, key):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    with (directory/(key+'.lock')).open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        path=directory/(key+'.json')
        data=json.loads(path.read_text()) if path.exists() else None
        if data is not None and (data.get('key')!=key or not isinstance(data.get('output'),str)):
            raise ValueError('Initialization cache corrupt or mismatched; preserve and inspect')
        yield data,lambda payload:write_json(path,dict(payload,key=key))
        fcntl.flock(lock,fcntl.LOCK_UN)
