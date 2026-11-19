import io
import os
import errno
import pytest
from httpie.output.writer import write_message
from httpie.context import Environment
from httpie.models import RequestsMessage, RequestsMessageKind, HTTPResponse
from httpie.output.processing import Conversion, Formatting
from httpie.output.models import ProcessingOptions
from httpie.output.options import OutputOptions


# Helper to create a minimal RequestsMessage
def make_requests_message(kind: RequestsMessageKind, content: bytes = b""):
    return RequestsMessage(kind=kind, content=content)


# Helper to create a minimal Environment
def make_environment(stdout=None, stderr=None, is_windows=False, stdout_isatty=False):
    stdout = stdout or io.StringIO()
    stderr = stderr or io.StringIO()
    env = Environment()
    env.stdout = stdout
    env.stderr = stderr
    env.is_windows = is_windows
    env.stdout_isatty = stdout_isatty
    return env


# Helper to create minimal OutputOptions
class DummyOutputOptions(OutputOptions):
    def __init__(self, any_value: bool):
        self._any = any_value

    def any(self):
        return self._any


# Helper to create minimal ProcessingOptions
class DummyProcessingOptions(ProcessingOptions):
    def __init__(self, stream=False, show_traceback=False):
        self.stream = stream
        self.show_traceback = show_traceback

    def get_prettify(self, env):
        return {}

    def get_conversion(self, env):
        return Conversion.NONE

    def get_formatting(self, env):
        return Formatting.NONE


def test_write_message_no_output_options(tmp_path):
    """When OutputOptions.any() is False, write_message returns immediately."""
    env = make_environment()
    output_options = DummyOutputOptions(any_value=False)
    processing_options = DummyProcessingOptions()
    msg = make_requests_message(RequestsMessageKind.RESPONSE)
    write_message(msg, env, output_options, processing_options)
    # stdout should remain empty
    assert env.stdout.getvalue() == ""


def test_write_message_writes_to_stdout(tmp_path):
    """write_message writes the message content to env.stdout when options are set."""
    env = make_environment()
    output_options = DummyOutputOptions(any_value=True)
    processing_options = DummyProcessingOptions()
    content = b"Hello, world!"
    msg = make_requests_message(RequestsMessageKind.RESPONSE, content=content)
    write_message(msg, env, output_options, processing_options)
    # The content should be written to stdout
    assert env.stdout.getvalue() == content.decode()


def test_write_message_handles_epipe(tmp_path):
    """write_message should swallow EPIPE errors unless show_traceback is True."""
    env = make_environment()
    output_options = DummyOutputOptions(any_value=True)
    processing_options = DummyProcessingOptions(show_traceback=False)

    # Create a message that will trigger an OSError when writing
    msg = make_requests_message(RequestsMessageKind.RESPONSE, content=b"data")

    # Monkeypatch the write_stream function to raise OSError(EPIPE)
    original_write_stream = __import__('httpie.output.writer').write_stream

    def fake_write_stream(*args, **kwargs):
        raise OSError(errno.EPIPE, "Broken pipe")

    try:
        __import__('httpie.output.writer').write_stream = fake_write_stream
        # Should not raise because EPIPE is ignored
        write_message(msg, env, output_options, processing_options)
        # stderr should contain a newline
        assert env.stderr.getvalue() == "\n"
    finally:
        __import__('httpie.output.writer').write_stream = original_write_stream
