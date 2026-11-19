"""Small, truthful progress events; no guessed percentage for upstream analysis."""
from datetime import datetime, timezone
import json
import time
from pilot.common import append_json, write_json

START = time.perf_counter()
LATEST = {}


def count_bar(done, total, width=12):
    """Count-based progress, never a time estimate or a success percentage."""
    if total is None or total<=0:
        return f'{done}/{total if total is not None else "?"}'
    fill=min(width,max(0,int(width*done/total)))
    return '['+'#'*fill+'-'*(width-fill)+f'] {done}/{total}'


def live_summary(state):
    phase=state.get('phase','starting');parts=[str(phase)]
    if state.get('workers_total') is not None:
        parts.append('workers='+count_bar(state.get('workers_finished',0),state['workers_total']))
    if phase=='initialization':
        parts.append(str(state.get('analysis_step','discovery')))
        if state.get('analysis_units_total') is not None:
            parts.append('items='+count_bar(state.get('analysis_units_completed',0),state['analysis_units_total']))
        parts.append('steps='+count_bar(state.get('analysis_steps_completed',0),state.get('analysis_steps_total')))
    elif phase.startswith('generation_round_'):
        parts.append(f"round={state.get('round_index','?')}/{state.get('rounds_total','?')}")
        parts.append('functions='+count_bar(state.get('functions_completed',0),state.get('functions_total')))
        if state.get('current_function'):parts.append(str(state['current_function']))
    elif phase=='scoring':
        parts.append('modules='+count_bar(state.get('modules_completed',0),state.get('modules_total')))
        if state.get('mutants_total') is not None:
            parts.append('mutants='+count_bar(state.get('mutants_completed',0),state['mutants_total']))
    if state.get('operation') and state.get('model_calls_started',0)>state.get('model_calls_finished',0):
        parts.append('operation='+str(state['operation']))
    if state.get('model_calls_finished') is not None:
        parts.append(f"calls_finished={state['model_calls_finished']} (total dynamic)")
    if state.get('status'):parts.append('status='+str(state['status']))
    return ' | '.join(parts)


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
