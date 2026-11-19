import io
import argparse
import types
import pytest
from httpie.core import program, ExitStatus
from httpie.context import Environment, LogLevel
from httpie.models import RequestsMessageKind, OutputOptions
from httpie.output.writer import MESSAGE_SEPARATOR_BYTES

# Helper to create a minimal Environment
class DummyEnv(Environment):
    def __init__(self):
        self.stdout = io.BytesIO()
        self.stderr = io.BytesIO()
        self.stdout_isatty = False
        self.log_messages = []

    def log_error(self, msg, level=LogLevel.ERROR):
        self.log_messages.append((msg, level))

# Helper to create a minimal argparse.Namespace
def make_args(**kwargs):
    ns = argparse.Namespace()
    defaults = {
        'download': False,
        'follow': False,
        'output_file': None,
        'output_file_specified': False,
        'output_options': set(),
        'check_status': False,
        'quiet': 0,
        'download_resume': False,
        'headers': {},
    }
    for k, v in defaults.items():
        setattr(ns, k, v)
    for k, v in kwargs.items():
        setattr(ns, k, v)
    return ns

# Mock message objects
class DummyMessage:
    def __init__(self, kind, body=None, status_code=200, raw=None, url="http://example.com"):
        self.kind = kind
        self.body = body
        self.status_code = status_code
        self.raw = raw or types.SimpleNamespace(status=f"{status_code} OK", reason="OK")
        self.url = url

# Test normal flow: request and response, no errors
def test_program_normal_flow(monkeypatch):
    env = DummyEnv()
    args = make_args()

    # Monkeypatch collect_messages to yield a request and a response
    def fake_collect_messages(env, args, request_body_read_callback=None):
        yield DummyMessage(RequestsMessageKind.REQUEST, body=b"hello")
        yield DummyMessage(RequestsMessageKind.RESPONSE, body=b"world", status_code=200)
    monkeypatch.setattr("httpie.core.collect_messages", fake_collect_messages)

    status = program(args, env)

    # Verify exit status
    assert status == ExitStatus.SUCCESS

    # Verify output contains request and response bodies
    output = env.stdout.getvalue()
    assert b"hello" in output
    assert b"world" in output
    # Separator should not appear because no streamed upload
    assert MESSAGE_SEPARATOR_BYTES not in output

# Test error status handling: 404 should set exit status to ERROR
def test_program_error_status(monkeypatch):
    env = DummyEnv()
    args = make_args(check_status=True)

    def fake_collect_messages(env, args, request_body_read_callback=None):
        yield DummyMessage(RequestsMessageKind.REQUEST, body=b"data")
        yield DummyMessage(RequestsMessageKind.RESPONSE, body=b"not found", status_code=404)
    monkeypatch.setattr("httpie.core.collect_messages", fake_collect_messages)

    status = program(args, env)

    assert status == ExitStatus.ERROR
    # Error message logged
    assert any("HTTP 404" in msg for msg, _ in env.log_messages)

# Test quiet mode with error status: no error log when quiet=1
def test_program_quiet_error(monkeypatch):
    env = DummyEnv()
    args = make_args(check_status=True, quiet=1)

    def fake_collect_messages(env, args, request_body_read_callback=None):
        yield DummyMessage(RequestsMessageKind.REQUEST, body=b"data")
        yield DummyMessage(RequestsMessageKind.RESPONSE, body=b"not found", status_code=404)
    monkeypatch.setattr("httpie.core.collect_messages", fake_collect_messages)

    status = program(args, env)

    assert status == ExitStatus.ERROR
    # No error logged because quiet=1
    assert all(level != LogLevel.WARNING for _, level in env.log_messages)
