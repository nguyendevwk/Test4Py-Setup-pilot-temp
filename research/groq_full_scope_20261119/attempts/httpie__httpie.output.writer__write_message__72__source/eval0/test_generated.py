import errno
import types
import pytest

# Import the target function and related classes
from httpie.output.writer import write_message
from httpie.output.writer import OutputOptions, ProcessingOptions
from httpie.models import RequestsMessage, RequestsMessageKind
from httpie.context import Environment


# Helper to create a minimal RequestsMessage
class DummyRequestMessage(RequestsMessage):
    def __init__(self):
        super().__init__(kind=RequestsMessageKind.REQUEST, request=None, response=None)


# Helper to create a minimal Environment
class DummyEnvironment(Environment):
    def __init__(self, stdout=None, stderr=None, is_windows=False, stdout_isatty=False):
        super().__init__()
        self.stdout = stdout or types.SimpleNamespace(write=lambda *args, **kwargs: None)
        self.stderr = stderr or types.SimpleNamespace(write=lambda *args, **kwargs: None)
        self.is_windows = is_windows
        self.stdout_isatty = stdout_isatty


def test_write_message_no_output_options(monkeypatch):
    """When OutputOptions.any() is False, write_message returns immediately."""
    env = DummyEnvironment()
    output_options = OutputOptions()
    processing_options = ProcessingOptions()
    # Ensure any() returns False
    assert not output_options.any()
    # Monkeypatch write_stream to detect if called
    called = {"flag": False}
    def fake_write_stream(**kwargs):
        called["flag"] = True
    monkeypatch.setattr(write_message, "write_stream", fake_write_stream)
    # Call the function
    write_message(DummyRequestMessage(), env, output_options, processing_options)
    # write_stream should not have been called
    assert not called["flag"]


def test_write_message_calls_write_stream(monkeypatch):
    """write_message should call write_stream with correct kwargs when output is enabled."""
    env = DummyEnvironment(stdout_isatty=True)
    output_options = OutputOptions()
    # Force any() to return True
    output_options.any = lambda: True
    processing_options = ProcessingOptions()
    # Capture the kwargs passed to write_stream
    captured = {}
    def fake_write_stream(**kwargs):
        captured.update(kwargs)
    monkeypatch.setattr(write_message, "write_stream", fake_write_stream)
    # Build a dummy stream object to return from build_output_stream_for_message
    dummy_stream = types.SimpleNamespace()
    monkeypatch.setattr(write_message, "build_output_stream_for_message",
                        lambda **kw: dummy_stream)
    # Call the function
    write_message(DummyRequestMessage(), env, output_options, processing_options)
    # Verify that write_stream was called with expected arguments
    assert captured["stream"] is dummy_stream
    assert captured["outfile"] is env.stdout
    assert captured["flush"] is True  # stdout_isatty True


def test_write_message_handles_epipe(monkeypatch):
    """write_message should swallow EPIPE errors when show_traceback is False."""
    env = DummyEnvironment(stderr=types.SimpleNamespace(write=lambda *args, **kwargs: None))
    output_options = OutputOptions()
    output_options.any = lambda: True
    processing_options = ProcessingOptions()
    processing_options.show_traceback = False
    # Make build_output_stream_for_message return a dummy stream
    dummy_stream = types.SimpleNamespace()
    monkeypatch.setattr(write_message, "build_output_stream_for_message",
                        lambda **kw: dummy_stream)
    # Monkeypatch write_stream to raise EPIPE
    def fake_write_stream(**kwargs):
        raise OSError(errno.EPIPE, "Broken pipe")
    monkeypatch.setattr(write_message, "write_stream", fake_write_stream)
    # Expect the exception to propagate
    with pytest.raises(OSError) as excinfo:
        write_message(DummyRequestMessage(), env, output_options, processing_options)
    assert excinfo.value.errno == errno.EPIPE
