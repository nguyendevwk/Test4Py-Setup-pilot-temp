from contextlib import ExitStack
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import signal
import subprocess
import time
import threading
from collections import deque

UPSTREAM = '3c8b45410545183a9a579a784ffefae722a158a6'
PYCG = '8d5dc40837803beef1d8d379fbf2cdad6cd94641'
BASE = Path(__file__).resolve().parents[1]
MODES = ('baseline', 'caller', 'extracted', 'verified')


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    tmp.replace(path)


def append_json(path, value):
    with Path(path).open('a') as stream:
        stream.write(json.dumps(value, ensure_ascii=False) + '\n')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def command(args, cwd=None, timeout=120, env=None, log_path=None, stream=False, label=None, heartbeat=15, console=None):
    """Kill the process group on timeout; optionally persist output as it arrives."""
    if stream:
        return stream_command(args, cwd, timeout, env, log_path, label, heartbeat, console)
    started = time.perf_counter()
    with ExitStack() as stack:
        sink = stack.enter_context(Path(log_path).open('w')) if log_path else subprocess.PIPE
        proc = subprocess.Popen(list(map(str, args)), cwd=cwd, env=env,
                                stdout=sink, stderr=subprocess.STDOUT if log_path else subprocess.PIPE,
                                text=True, start_new_session=True)
        expired = False
        try:
            out, err = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            expired = True
            os.killpg(proc.pid, signal.SIGKILL)
            out, err = proc.communicate()
    if log_path:
        out, err = Path(log_path).read_text(errors='replace')[-12000:], ''
    return dict(command=list(map(str, args)), returncode=proc.returncode,
                stdout=out, stderr=err, timeout=expired, log_path=str(log_path) if log_path else None,
                seconds=time.perf_counter() - started)


def checked(args, **kwargs):
    result = command(args, **kwargs)
    if result['returncode'] != 0 or result['timeout']:
        raise RuntimeError(json.dumps(result))
    return result['stdout'].strip()


def checkout(url, revision, dst):
    """A new independent checkout for every arm, even on notebook reruns."""
    dst = Path(dst)
    dst.mkdir(parents=True, exist_ok=False)
    checked(['git', 'init', '-q', dst])
    checked(['git', '-C', dst, 'fetch', '--depth', '1', url, revision], timeout=180)
    checked(['git', '-C', dst, 'checkout', '--detach', 'FETCH_HEAD'])
    actual = checked(['git', '-C', dst, 'rev-parse', 'HEAD'])
    if actual != revision:
        raise RuntimeError(f'Wrong commit: {actual}, expected {revision}')
    if checked(['git', '-C', dst, 'status', '--porcelain']):
        raise RuntimeError('Checkout is not clean')
    return actual


def reserve_output(requested):
    """Fresh sibling for notebook reruns; never reuse/delete earlier artifacts."""
    requested = Path(requested).resolve()
    if requested.exists() and not requested.is_dir():
        raise ValueError(f'Output exists and is not a directory: {requested}')
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    for attempt in range(100):
        candidate = requested if attempt == 0 else requested.with_name(
            requested.name + f'-rerun-{timestamp}-{attempt}')
        try:
            candidate.mkdir(parents=True, exist_ok=False)
            return candidate
        except FileExistsError:
            continue
    raise RuntimeError('Could not allocate a fresh output directory')


def package_versions():
    # In system-site-packages venvs, metadata can contain both local and inherited
    # distributions. Resolve each name through active sys.path, matching imports.
    names = {dist.metadata['Name'] for dist in importlib.metadata.distributions()}
    return {name: importlib.metadata.version(name) for name in sorted(names) if name}


def stream_command(args, cwd, timeout, env, log_path, label, heartbeat, console=None):
    """Tee subprocess output to notebook and durable log, including while waiting."""
    from pilot.console import Console
    console = console or Console('full')
    started = time.perf_counter()
    lines = deque(maxlen=250)
    last_output = [started]
    expired = False
    with ExitStack() as stack:
        sink = stack.enter_context(Path(log_path).open('w')) if log_path else None
        proc = subprocess.Popen(list(map(str, args)), cwd=cwd, env=env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors='replace',
            bufsize=1, start_new_session=True)
        def read():
            for line in proc.stdout:
                lines.append(line)
                last_output[0] = time.perf_counter()
                if sink:
                    sink.write(line)
                    sink.flush()
                console.write(line, label=label or 'process')
            proc.stdout.close()
        reader = threading.Thread(target=read, daemon=True)
        reader.start()
        while True:
            remaining = timeout - (time.perf_counter() - started)
            if remaining <= 0:
                expired = True
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
                break
            try:
                proc.wait(timeout=min(heartbeat, remaining))
                break
            except subprocess.TimeoutExpired:
                if time.perf_counter() - last_output[0] >= heartbeat:
                    console.write(f'[{label or "process"}] running {time.perf_counter()-started:.0f}s; waiting for next event', label=label or 'process')
        reader.join()
    return dict(command=list(map(str, args)), returncode=proc.returncode, timeout=expired,
        stdout=''.join(lines)[-12000:], stderr='', seconds=time.perf_counter()-started,
        log_path=str(log_path) if log_path else None)
