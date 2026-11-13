"""Small, truthful progress events; no guessed percentage for upstream analysis."""
from datetime import datetime, timezone
import json
import time
from pilot.common import append_json, write_json

START = time.perf_counter()
LATEST = {}


def emit(work, phase, event, **details):
    row = dict(time=datetime.now(timezone.utc).isoformat(), mode=work.name,
               phase=phase, event=event, elapsed_seconds=round(time.perf_counter() - START, 2), **details)
    append_json(work / 'events.jsonl', row)
    prior = LATEST.get(str(work), {})
    # A parent scheduler may finalize an arm after its worker exits. Preserve the
    # worker's latest counters instead of replacing them with the parent's cache.
    try:
        prior = dict(prior, **json.loads((work / 'progress.json').read_text()))
    except (OSError, ValueError):
        pass
    latest = dict(prior, **row)
    LATEST[str(work)] = latest
    write_json(work / 'progress.json', latest)
    fields = ' '.join(f'{key}={value}' for key, value in details.items())
    print(f'[{work.name}] {phase}/{event} {fields}', flush=True)
    return row
