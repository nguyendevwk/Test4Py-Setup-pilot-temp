import argparse
import io
import types
import pytest
from httpie.core import program, ExitStatus
from httpie.context import Environment, LogLevel
from httpie.models import RequestsMessageKind, OutputOptions
from httpie.output.writer import MESSAGE_SEPARATOR_BYTES

# Helper to create a minimal Environment
def make_env(isatty=False):
    env = Environment(
        stdout=io.BytesIO(),
        stderr=io.BytesIO(),
        log_level=LogLevel.INFO,
        stdout_isatty=isatty,
        stderr_isatty=isatty,
    )
    return env

# Helper to create a minimal argparse.Namespace
def make_args(**kwargs):
    ns = argparse.Namespace()
    defaults = {
        "download": False,
        "follow": False,
        "output_file": None,
        "output_file_specified": False,
        "output_options": set(),
        "check_status": False,
        "quiet": 0,
        "download_resume": False,
    }
    for k, v in defaults.items():
        setattr(ns, k, v)
    for k, v in kwargs.items():
        setattr(ns, k, v)
    return ns

# Dummy message objects
class DummyMessage:
    def __init__(self, kind, body=None, status_code=200, raw_status=200, raw_reason="OK"):
        self.kind = kind
        self.body = body
        self.status_code = status_code
        self.raw = types.SimpleNamespace(status=raw_status, reason=raw_reason)

# Test 1: program returns SUCCESS when no messages are produced
def test_program_success_no_messages(monkeypatch):
    env = make_env()
    args = make_args()
    # Patch collect_messages to return an empty list
    monkeypatch.setattr("httpie.core.collect_messages", lambda *_, **__: [])
    status = program(args, env)
    assert status == ExitStatus.SUCCESS
    # stdout should be empty
    assert env.stdout.getvalue() == b""

# Test 2: program logs warning and returns non-success when check_status is true and response is 404
def test_program_check_status_failure(monkeypatch):
    env = make_env()
    args = make_args(check_status=True)
    # Patch collect_messages to return a request and a 404 response
    request_msg = DummyMessage(kind=RequestsMessageKind.REQUEST, body=b"")
    response_msg = DummyMessage(kind=RequestsMessageKind.RESPONSE, status_code=404, raw_status=404, raw_reason="Not Found")
    monkeypatch.setattr("httpie.core.collect_messages", lambda *_, **__: [request_msg, response_msg])
    status = program(args, env)
    assert status != ExitStatus.SUCCESS
    # Warning should be logged to stderr
    stderr_output = env.stderr.getvalue().decode()
    assert "HTTP 404 Not Found" in stderr_output

# Test 3: program downloads a file when --download is set
def test_program_download(monkeypatch, tmp_path):
    env = make_env()
    output_file = tmp_path / "out.txt"
    args = make_args(download=True, output_file=output_file.open("wb"), output_file_specified=True)
    # Patch collect_messages to return a request and a 200 response
    request_msg = DummyMessage(kind=RequestsMessageKind.REQUEST, body=b"")
    response_msg = DummyMessage(kind=RequestsMessageKind.RESPONSE, status_code=200, raw_status=200, raw_reason="OK")
    monkeypatch.setattr("httpie.core.collect_messages", lambda *_, **__: [request_msg, response_msg])
    # Patch Downloader.start to return a simple stream
    class DummyStream:
        def __iter__(self):
            yield b"content"
    class DummyDownloader:
        def __init__(self, *_, **__): pass
        def pre_request(self, *_, **__): pass
        def start(self, *_, **__): return DummyStream(), output_file
        def finish(self): pass
        @property
        def finished(self): return True
        @property
        def interrupted(self): return False
    monkeypatch.setattr("httpie.core.Downloader", DummyDownloader)
    status = program(args, env)
    assert status == ExitStatus.SUCCESS
    # File should contain the downloaded content
    assert output_file.read_text() == "content"
