import io
import errno
import types
import pytest
from httpie.output.writer import write_message
from httpie.context import Environment
from httpie.models import OutputOptions, RequestsMessage, RequestsMessageKind
from httpie.output.processing import ProcessingOptions

# Helper to create a minimal RequestsMessage
def make_requests_message(body=b"hello", kind=RequestsMessageKind.RESPONSE):
    return RequestsMessage(
        kind=kind,
        request=types.SimpleNamespace(url="http://example.com"),
        response=types.SimpleNamespace(status_code=200, headers={}, content=body),
        request_headers={},
        response_headers={},
    )

# Dummy Environment that captures writes
class DummyEnv(Environment):
    def __init__(self):
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()
        self.is_windows = False
        self.stdout_isatty = False

# Dummy OutputOptions that can be toggled
class DummyOutputOptions(OutputOptions):
    def __init__(self, any_flag=True):
        self._any = any_flag
    def any(self):
        return self._any

# Dummy ProcessingOptions
class DummyProcessingOptions(ProcessingOptions):
    def __init__(self, stream=False, show_traceback=False):
        self.stream = stream
        self.show_traceback = show_traceback
    def get_prettify(self, env):
        return {}

# Test that nothing is written when output_options.any() is False
def test_write_message_no_output():
    env = DummyEnv()
    msg = make_requests_message()
    output_options = DummyOutputOptions(any_flag=False)
    processing_options = DummyProcessingOptions()
    write_message(msg, env, output_options, processing_options)
    assert env.stdout.getvalue() == ""

# Test that on Windows with colors, write_stream_with_colors_win is used
def test_write_message_windows_colors(monkeypatch):
    env = DummyEnv()
    env.is_windows = True
    msg = make_requests_message()
    output_options = DummyOutputOptions()
    processing_options = DummyProcessingOptions()
    # Patch get_prettify to indicate colors
    def fake_get_prettify(env):
        return {"colors": True}
    monkeypatch.setattr(processing_options, "get_prettify", fake_get_prettify)
    # Capture that write_stream_with_colors_win is called by patching it
    called = {"called": False}
    def fake_write_stream_with_colors_win(*args, **kwargs):
        called["called"] = True
    monkeypatch.setattr("httpie.output.writer.write_stream_with_colors_win", fake_write_stream_with_colors_win)
    write_message(msg, env, output_options, processing_options)
    assert called["called"] is True
    # Ensure stdout got the message content
    assert "hello" in env.stdout.getvalue()

# Test that a broken pipe (EPIPE) is ignored unless show_traceback is True
def test_write_message_broken_pipe(monkeypatch):
    env = DummyEnv()
    msg = make_requests_message()
    output_options = DummyOutputOptions()
    processing_options = DummyProcessingOptions(stream=True, show_traceback=False)
    # Patch write_stream to raise OSError EPIPE
    def fake_write_stream(*args, **kwargs):
        raise OSError(errno.EPIPE, "Broken pipe")
    monkeypatch.setattr("httpie.output.writer.write_stream", fake_write_stream)
    write_message(msg, env, output_options, processing_options)
    # stderr should contain a newline
    assert env.stderr.getvalue() == "\n"
