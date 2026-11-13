"""One updating notebook display; subprocess output is kept on disk."""
from collections import deque
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

from pilot.common import BASE, MODES, reserve_output


def read_json(path):
    try:
        # Status/report files are small; never load model_calls.jsonl into the UI.
        if Path(path).stat().st_size > 2_000_000:
            return {}
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return {}


def tail_text(path, limit=3000):
    try:
        with Path(path).open('rb') as stream:
            stream.seek(0, 2)
            stream.seek(max(0, stream.tell() - limit))
            return stream.read(limit).decode(errors='replace')
    except OSError:
        return ''


def snapshot(output):
    output = Path(output)
    run = read_json(output / 'notebook-run.json')
    comparison = read_json(output / 'comparison/comparison.json')
    arms = []
    for mode in MODES:
        work = output / 'comparison' / mode
        progress = read_json(work / 'progress.json')
        report = read_json(work / 'report.json')
        score = report.get('score', {})
        arms.append(dict(mode=mode,
            analysis_done=progress.get('analysis_steps_completed'), analysis_total=progress.get('analysis_steps_total'),
            rounds_done=progress.get('rounds_completed', 0), rounds_total=progress.get('rounds_total', report.get('settings', {}).get('rounds')),
            calls_done=progress.get('model_calls_finished'), calls_started=progress.get('model_calls_started'),
            probes_used=progress.get('probes_used'), probe_budget=progress.get('probe_budget'),
            mutants_done=progress.get('mutants_completed'), mutants_total=progress.get('mutants_total'),
            mutants_skipped=progress.get('mutants_skipped',0), verified_scenarios=progress.get('verified_scenarios'),
            scenarios_total=progress.get('scenarios_total'), phase=progress.get('phase', 'queued'),
            event=progress.get('event', ''), status=report.get('status', 'queued'),
            call=progress.get('call'), input_tokens=progress.get('total_input_tokens', report.get('input_tokens', 0)),
            output_tokens=progress.get('total_output_tokens', report.get('output_tokens', 0)),
            tokens_per_second=progress.get('tokens_per_second'),
            gpu=report.get('versions', {}).get('cuda_visible_devices',
                progress.get('visible_gpus', progress.get('gpu', '—'))),
            allocated_gib=progress.get('allocated_gib'), reserved_gib=progress.get('reserved_gib'),
            passed=score.get('passed'), mutation_score=score.get('mutation_score'),
            updated=progress.get('time', '—')))
    gpu = read_json(output / 'comparison/gpu_latest.json')
    # Attach to an already-running pre-dashboard version, reading only a bounded tail.
    if not gpu:
        for line in reversed(tail_text(output / 'comparison/gpu_usage.jsonl', 8192).splitlines()):
            try:
                gpu = json.loads(line)
                break
            except ValueError:
                continue
    step = run.get('current_step')
    if not step and run.get('status') == 'running':
        completed = {row.get('name') for row in run.get('steps', [])}
        step = next((name for name in ('bootstrap', 'validation', 'comparison') if name not in completed), 'comparison')
    return dict(output=str(output), status=run.get('status', 'starting'), step=step or 'starting',
        completed=len(comparison.get('arms', {})), arms=arms,
        stages_done=run.get('steps_completed', len(run.get('steps', []))),
        stages_total=run.get('steps_total', 3), gpus=gpu.get('gpus', []),
        gpu_updated=gpu.get('time', '—'), failed_step=run.get('failed_step'))


def render(state, elapsed=0, process_code=None, history=()):
    def esc(value):
        return html.escape(str(value if value is not None else '—')[:220])
    status = state['status']
    if process_code is not None and process_code != 0:
        status = 'failed'
    header = f"<b>Test4Py · {esc(status)}</b> · {esc(state['step'])} · elapsed {elapsed:.0f}s · stages {state.get('stages_done',0)}/{state.get('stages_total',3)} · arms {state['completed']}/4"
    columns = ('Mode', 'Status', 'GPU', 'Phase', 'Event', 'Call', 'Tokens in/out', 'tok/s', 'VRAM allocated/reserved GiB', 'Pass', 'Mutation', 'Last event age (s)')
    rows = []
    for arm in state['arms']:
        try:
            age = round((datetime.now(timezone.utc) - datetime.fromisoformat(arm['updated'])).total_seconds())
        except (ValueError, TypeError):
            age = None
        values = [arm['mode'], arm['status'], arm['gpu'], arm['phase'], arm['event'], arm['call'],
                  f"{arm['input_tokens']}/{arm['output_tokens']}", arm['tokens_per_second'],
                  f"{arm['allocated_gib']}/{arm['reserved_gib']}", arm['passed'], arm['mutation_score'], age]
        rows.append('<tr>' + ''.join('<td>' + esc(v) + '</td>' for v in values) + '</tr>')
    counts = []
    def ratio(done, total):
        return f'{done or 0}/{total}' if total else '—'
    for arm in state['arms']:
        values = [arm['mode'], ratio(arm['analysis_done'], arm['analysis_total']),
                  ratio(arm['rounds_done'], arm['rounds_total']),
                  ratio(arm['calls_done'], arm['calls_started']),
                  ratio(arm['probes_used'], arm['probe_budget']), ratio(arm['verified_scenarios'], arm['scenarios_total']),
                  ratio(arm['mutants_done'], arm['mutants_total']) + (f" (skip {arm['mutants_skipped']})" if arm['mutants_skipped'] else '')]
        counts.append('<tr>' + ''.join('<td>' + esc(value) + '</td>' for value in values) + '</tr>')
    counter_table = ('<p><b>Work counters</b> · counts are not estimates of remaining time</p><table style="width:100%">'
        '<tr><th>Mode</th><th>Tracked init steps</th><th>Rounds</th><th>LLM finished/started</th>'
        '<th>Probes/budget</th><th>Verified scenarios</th><th>Mutant runs ended/total</th></tr>' + ''.join(counts) + '</table>')
    gpu_rows = []
    for gpu in state['gpus'][:8]:
        gpu_rows.append(f"GPU {esc(gpu['index'])}: {esc(gpu['utilization_percent'])}% · "
                        f"{gpu['used_mib']/1024:.1f}/{gpu['total_mib']/1024:.1f} GiB")
    return ("<div style='max-width:100%;overflow:auto;border:1px solid #888;padding:12px;font:13px sans-serif'>"
            + header + "<p>" + ' | '.join(gpu_rows) + "</p><table style='border-collapse:collapse;width:100%'>"
            + '<tr>' + ''.join('<th style="text-align:left;padding:4px">' + c + '</th>' for c in columns) + '</tr>'
            + ''.join(rows) + '</table>' + counter_table + render_charts(history) + '<p>GPU sampled: ' + esc(state['gpu_updated']) + '</p>'
            + '<p>Full logs and reports: <code>' + esc(state['output']) + '</code></p></div>')


def watch_run(output, refresh=10, process=None, display_fn=None, html_fn=None):
    """Attach to a run folder without starting, stopping or changing its experiment."""
    if refresh < 1:
        raise ValueError('refresh must be at least one second')
    if display_fn is None:
        from IPython.display import display, HTML
        display_fn, html_fn = display, HTML
    html_fn = html_fn or (lambda value: value)
    start = time.monotonic()
    history = deque(maxlen=60)
    handle = display_fn(html_fn(render(snapshot(output))), display_id=True)
    if handle is None:
        raise RuntimeError('This frontend does not support updating displays; use compact console mode')
    while True:
        state = snapshot(output)
        code = process.poll() if process else None
        elapsed = time.monotonic() - start
        history.append(dict(seconds=elapsed, gpus=state['gpus'],
            tokens=sum((arm['input_tokens'] or 0) + (arm['output_tokens'] or 0) for arm in state['arms']),
            rates={arm['mode']: arm['tokens_per_second'] for arm in state['arms']}))
        handle.update(html_fn(render(state, elapsed, code, history)))
        if code is not None or (process is None and state['status'] in ('complete', 'failed')):
            return state
        time.sleep(refresh)


def stop_process_tree(process):
    # Kaggle provides psutil; stop independently grouped workers too, on cell interrupt.
    try:
        import psutil
        descendants = psutil.Process(process.pid).children(recursive=True)
        for child in reversed(descendants):
            try:
                child.terminate()
            except psutil.NoSuchProcess:
                pass
        _, remaining = psutil.wait_procs(descendants, timeout=3)
        for child in remaining:
            try:
                child.kill()
            except psutil.NoSuchProcess:
                pass
    except Exception:
        pass
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def run_notebook(output='/kaggle/working/pilot-dashboard', project=BASE,
                 jobs=2, gpus='auto', rounds=1, refresh=10, runtime='modern'):
    """Run the guarded launcher with one replacing display, without piping logs to browser."""
    if refresh < 1:
        raise ValueError('refresh must be at least one second')
    root = reserve_output(output)
    run = root / 'run'
    cmd = [sys.executable, '-u', str(Path(project) / 'kaggle_run.py'), '--runtime', runtime,
           '--jobs', str(jobs), '--gpus', gpus, '--rounds', str(rounds), '--console', 'quiet',
           '--output', str(run)]
    with (root / 'launcher.log').open('w') as stream:
        process = subprocess.Popen(cmd, cwd=project, stdout=stream, stderr=subprocess.STDOUT,
                                   start_new_session=True)
        try:
            watch_run(run, refresh=refresh, process=process)
        except BaseException:
            stop_process_tree(process)
            raise
        code = process.wait()
    if code:
        raise RuntimeError(f'Pilot stopped (exit {code}). Inspect {run / "notebook-run.json"} and {root / "launcher.log"}')
    return str(run)


def render_charts(history):
    """Bounded rolling SVG telemetry, not publication statistics or extrapolation."""
    if not history:
        return '<p>Charts waiting for telemetry samples.</p>'
    def chart(title, series, ceiling=None):
        valid = [(x, y) for values in series.values() for x, y in values if y is not None]
        if not valid:
            return '<div>' + html.escape(title) + ': waiting for samples</div>'
        x0, x1 = min(x for x, y in valid), max(x for x, y in valid)
        ymax = ceiling or max(1, max(y for x, y in valid))
        colors = ('#087ea4', '#c05621', '#6b46c1', '#247544')
        lines = []
        for i, (label, values) in enumerate(series.items()):
            points = ' '.join(f'{35+350*(x-x0)/max(x1-x0,1):.1f},{90-70*y/ymax:.1f}'
                              for x, y in values if y is not None)
            lines.append(f'<polyline fill="none" stroke="{colors[i%4]}" stroke-width="2" points="{points}"/>')
        legend = ' · '.join(html.escape(str(label)) for label in series)
        return ('<div style="display:inline-block;vertical-align:top;width:410px;max-width:100%">'
            + '<b>' + html.escape(title) + '</b>'
            + '<svg viewBox="0 0 410 120" role="img" aria-label="' + html.escape(title, quote=True) + '">'
            + '<path d="M35 20V90H385" fill="none" stroke="#888"/>'
            + f'<text x="1" y="24" font-size="10">{ymax:.0f}</text><text x="16" y="94" font-size="10">0</text>'
            + ''.join(lines) + f'<text x="35" y="110" font-size="10">{x0:.0f}s</text>'
            + f'<text x="345" y="110" font-size="10">{x1:.0f}s</text></svg><small>{legend}</small></div>')
    devices = sorted({str(gpu['index']) for row in history for gpu in row['gpus']})[:8]
    utilization, memory = {}, {}
    for device in devices:
        utilization['GPU ' + device] = [(row['seconds'], next((gpu['utilization_percent'] for gpu in row['gpus'] if str(gpu['index']) == device), None)) for row in history]
        memory['GPU ' + device] = [(row['seconds'], next((gpu['used_mib']/1024 for gpu in row['gpus'] if str(gpu['index']) == device), None)) for row in history]
    token_series = {'all arms input + output': [(row['seconds'], row['tokens']) for row in history]}
    return ('<p><b>Rolling telemetry</b> · at most 60 samples; seconds since dashboard attachment</p>'
            + chart('GPU utilization (%)', utilization, 100)
            + chart('GPU used memory (GiB)', memory)
            + chart('Cumulative model tokens', token_series))
