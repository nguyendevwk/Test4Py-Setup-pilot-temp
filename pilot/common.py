from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time

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


def command(args, cwd=None, timeout=120, env=None):
    """Kill the process group on timeout, including any pytest subprocesses."""
    started = time.perf_counter()
    proc = subprocess.Popen(list(map(str, args)), cwd=cwd, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, start_new_session=True)
    expired = False
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        expired = True
        os.killpg(proc.pid, signal.SIGKILL)
        out, err = proc.communicate()
    return dict(command=list(map(str, args)), returncode=proc.returncode,
                stdout=out, stderr=err, timeout=expired,
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
