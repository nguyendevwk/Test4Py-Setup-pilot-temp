"""Small, truthful progress events; no guessed percentage for upstream analysis."""
from datetime import datetime, timezone
import time
from pilot.common import append_json, write_json

START = time.perf_counter()
LATEST = {}


def emit(work, phase, event, **details):
    row = dict(time=datetime.now(timezone.utc).isoformat(), mode=work.name,
               phase=phase, event=event, elapsed_seconds=round(time.perf_counter() - START, 2), **details)
    append_json(work / 'events.jsonl', row)
    latest = dict(LATEST.get(str(work), {}), **row)
    LATEST[str(work)] = latest
    write_json(work / 'progress.json', latest)
    fields = ' '.join(f'{key}={value}' for key, value in details.items())
    print(f'[{work.name}] {phase}/{event} {fields}', flush=True)
    return row
