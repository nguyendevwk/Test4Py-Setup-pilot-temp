import io
import errno
import types
import pytest

# Import the target function and its module for monkeypatching
from httpie.output.writer import write_message, build_output_stream_for_message
from httpie.output.writer import write_stream, write_stream_with_colors_win

# Minimal stubs for the required classes
class DummyEnvironment:
    def __init__(self):
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()
        self.stdout_isatty = False
        self.is_windows = False

class DummyOutputOptions:
    def __init__(self, any_flag=True):
        self._any = any_flag
    def any(self):
        return self._any

class DummyProcessingOptions:
    def __init__(self, stream=False, show_traceback=False, prettify=None):
        self.stream = stream
        self.show_traceback = show_traceback
        self._prettify = prettify or {}
    def get_prettify(self, env):
        return self._prettify

class DummyRequestsMessage:
    def __init__(self, kind, content):
        self.kind = kind
        self.content = content

# Helper to replace the stream builder
def fake_build_output_stream_for_message(*_, **__):
    # Return a simple stream that writes to a StringIO
    return io.StringIO()

# Helper to replace write_stream to capture arguments
captured_write_stream_args = {}
def fake_write_stream(**kwargs):
    captured_write_stream_args.update(kwargs)

# Helper to replace write_stream_with_colors_win
captured_write_stream_win_args = {}
def fake_write_stream_with_colors_win(**kwargs):
    captured_write_stream_win_args.update(kwargs)

@pytest.fixture(autouse=True)
def patch_functions(monkeypatch):
    monkeypatch.setattr(write_message, "__module__", "httpie.output.writer")
    monkeypatch.setattr(write_message.__globals__, "build_output_stream_for_message", fake_build_output_stream_for_message)
    monkeypatch.setattr(write_message.__globals__, "write_stream", fake_write_stream)
    monkeypatch.setattr(write_message.__globals__, "write_stream_with_colors_win", fake_write_stream_with_colors_win)

def test_write_message_no_output_options():
    """When output_options.any() is False, write_message returns immediately."""
    env = DummyEnvironment()
    output_options = DummyOutputOptions(any_flag=False)
    processing_options = DummyProcessingOptions()
    requests_message = DummyRequestsMessage(kind="request", content="GET / HTTP/1.1")
    write_message(requests_message, env, output_options, processing_options)
    # No output should have been written
    assert env.stdout.getvalue() == ""

def test_write_message_normal_output(tmp_path):
    """write_message writes to stdout when output_options.any() is True."""
    env = DummyEnvironment()
    output_options = DummyOutputOptions(any_flag=True)
    processing_options = DummyProcessingOptions()
    requests_message = DummyRequestsMessage(kind="response", content="HTTP/1.1 200 OK")
    write_message(requests_message, env, output_options, processing_options)
    # The fake_write_stream should have been called with the fake stream
    assert "stream" in captured_write_stream_args
    assert "outfile" in captured_write_stream_args
    # Since we used a StringIO for the stream, nothing is actually written to env.stdout
    # but we can assert that the stream object is a StringIO instance
    assert isinstance(captured_write_stream_args["stream"], io.StringIO)

def test_write_message_windows_colors(monkeypatch):
    """On Windows with colors requested, write_stream_with_colors_win is used."""
    env = DummyEnvironment()
    env.is_windows = True
    output_options = DummyOutputOptions(any_flag=True)
    processing_options = DummyProcessingOptions(prettify={"colors": True})
    requests_message = DummyRequestsMessage(kind="request", content="GET / HTTP/1.1")
    write_message(requests_message, env, output_options, processing_options)
    # Ensure the Windows-specific function was called
    assert captured_write_stream_win_args, "write_stream_with_colors_win was not called"
    # The arguments should match those passed to write_stream_with_colors_win
    assert captured_write_stream_win_args["stream"] == captured_write_stream_args["stream"]
    assert captured_write_stream_win_args["outfile"] == captured_write_stream_args["outfile"]
