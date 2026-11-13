"""One updating notebook display; subprocess output is kept on disk."""
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
        arms.append(dict(mode=mode, phase=progress.get('phase', 'queued'),
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
        completed=len(comparison.get('arms', {})), arms=arms, gpus=gpu.get('gpus', []),
        gpu_updated=gpu.get('time', '—'), failed_step=run.get('failed_step'))


def render(state, elapsed=0, process_code=None):
    def esc(value):
        return html.escape(str(value if value is not None else '—')[:220])
    status = state['status']
    if process_code is not None and process_code != 0:
        status = 'failed'
    header = f"<b>Test4Py · {esc(status)}</b> · {esc(state['step'])} · elapsed {elapsed:.0f}s · arms {state['completed']}/4"
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
    gpu_rows = []
    for gpu in state['gpus'][:8]:
        gpu_rows.append(f"GPU {esc(gpu['index'])}: {esc(gpu['utilization_percent'])}% · "
                        f"{gpu['used_mib']/1024:.1f}/{gpu['total_mib']/1024:.1f} GiB")
    return ("<div style='max-width:100%;overflow:auto;border:1px solid #888;padding:12px;font:13px sans-serif'>"
            + header + "<p>" + ' | '.join(gpu_rows) + "</p><table style='border-collapse:collapse;width:100%'>"
            + '<tr>' + ''.join('<th style="text-align:left;padding:4px">' + c + '</th>' for c in columns) + '</tr>'
            + ''.join(rows) + '</table><p>GPU sampled: ' + esc(state['gpu_updated']) + '</p>'
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
    handle = display_fn(html_fn(render(snapshot(output))), display_id=True)
    if handle is None:
        raise RuntimeError('This frontend does not support updating displays; use compact console mode')
    while True:
        state = snapshot(output)
        code = process.poll() if process else None
        handle.update(html_fn(render(state, time.monotonic() - start, code)))
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
