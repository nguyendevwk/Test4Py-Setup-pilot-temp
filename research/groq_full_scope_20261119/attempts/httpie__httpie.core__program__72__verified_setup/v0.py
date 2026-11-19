import io
import types
import pytest
from httpie.core import program, ExitStatus
from httpie.context import Environment, LogLevel
from httpie.models import RequestsMessageKind, OutputOptions
from httpie.output.writer import MESSAGE_SEPARATOR_BYTES

# Helper to create a minimal argparse.Namespace
def make_args(**kwargs):
    import argparse
    ns = argparse.Namespace()
    for k, v in kwargs.items():
        setattr(ns, k, v)
    return ns

# Dummy message objects
class DummyMessage:
    def __init__(self, kind, body=None, status_code=200, raw=None):
        self.kind = kind
        self.body = body
        self.status_code = status_code
        self.raw = raw or types.SimpleNamespace(status=f"{status_code} OK", reason="OK")

# Dummy environment
class DummyEnv(Environment):
    def __init__(self):
        self.stdout = io.BytesIO()
        self.stdout_isatty = False
        self.log_errors = []
    def log_error(self, msg, level=LogLevel.ERROR):
        self.log_errors.append((msg, level))

# Test normal success flow
def test_program_success(monkeypatch, tmp_path):
    # Prepare args
    args = make_args(
        download=False,
        follow=False,
        output_file=None,
        output_file_specified=False,
        download_resume=False,
        headers={},
        output_options=set(),
        check_status=False,
        quiet=0,
    )
    env = DummyEnv()

    # Mock collect_messages to yield a request and a 200 response
    def fake_collect_messages(env, args, request_body_read_callback=None):
        yield DummyMessage(RequestsMessageKind.REQUEST, body=b"req")
        yield DummyMessage(RequestsMessageKind.RESPONSE, body=b"res", status_code=200)
    monkeypatch.setattr("httpie.core.collect_messages", fake_collect_messages)

    status = program(args, env)
    assert status == ExitStatus.SUCCESS
    # Ensure output contains request and response bodies
    output = env.stdout.getvalue()
    assert b"req" in output
    assert b"res" in output

# Test error status with check_status
def test_program_check_status_error(monkeypatch, tmp_path):
    args = make_args(
        download=False,
        follow=False,
        output_file=None,
        output_file_specified=False,
        download_resume=False,
        headers={},
        output_options=set(),
        check_status=True,
        quiet=0,
    )
    env = DummyEnv()

    def fake_collect_messages(env, args, request_body_read_callback=None):
        yield DummyMessage(RequestsMessageKind.REQUEST, body=b"req")
        yield DummyMessage(RequestsMessageKind.RESPONSE, body=b"res", status_code=404)
    monkeypatch.setattr("httpie.core.collect_messages", fake_collect_messages)

    status = program(args, env)
    assert status == ExitStatus.ERROR
    # Error log should contain HTTP 404
    assert any("HTTP 404" in msg for msg, _ in env.log_errors)

# Test download flow with dummy downloader
def test_program_download(monkeypatch, tmp_path):
    output_file = tmp_path / "out.txt"
    output_file.open("wb")  # create file
    args = make_args(
        download=True,
        follow=True,
        output_file=output_file,
        output_file_specified=True,
        download_resume=False,
        headers={},
        output_options=set(),
        check_status=False,
        quiet=0,
    )
    env = DummyEnv()

    # Dummy downloader that records calls
    class DummyDownloader:
        def __init__(self, env, output_file, resume):
            self.env = env
            self.output_file = output_file
            self.resume = resume
            self.finished = False
            self.interrupted = False
        def pre_request(self, headers):
            self.pre_requested = True
        def start(self, initial_url, final_response):
            self.started = True
            return (io.BytesIO(b"downloaded"), self.output_file)
        def finish(self):
            self.finished = True
        def failed(self):
            self.failed_called = True
    monkeypatch.setattr("httpie.core.Downloader", DummyDownloader)

    def fake_collect_messages(env, args, request_body_read_callback=None):
        yield DummyMessage(RequestsMessageKind.REQUEST, body=b"req")
        yield DummyMessage(RequestsMessageKind.RESPONSE, body=b"res", status_code=200)
    monkeypatch.setattr("httpie.core.collect_messages", fake_collect_messages)

    status = program(args, env)
    assert status == ExitStatus.SUCCESS
    # Ensure downloader was used
    downloader = args.output_file
    # Check that the output file contains downloaded data
    with open(output_file, "rb") as f:
        assert f.read() == b"downloaded"
