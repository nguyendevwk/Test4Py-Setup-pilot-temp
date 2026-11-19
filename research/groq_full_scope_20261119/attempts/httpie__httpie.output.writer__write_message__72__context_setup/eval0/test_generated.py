import io
import os
import errno
import pytest
from httpie.output.writer import write_message, build_output_stream_for_message
from httpie.context import Environment
from httpie.models import RequestsMessage, RequestsMessageKind, OutputOptions, ProcessingOptions
from httpie.cli.dicts import HTTPHeadersDict

# Helper to create a minimal Environment that writes to an in-memory buffer
class DummyEnv(Environment):
    def __init__(self):
        super().__init__()
        self.stdout = io.BytesIO()
        self.stderr = io.BytesIO()
        self.stdout_isatty = True
        self.is_windows = False

def test_write_message_no_output_options_does_nothing(tmp_path):
    env = DummyEnv()
    msg = RequestsMessage(kind=RequestsMessageKind.REQUEST, headers=HTTPHeadersDict(), body=b'')
    output_options = OutputOptions()
    processing_options = ProcessingOptions()
    # No output options set, write_message should return None and not write anything
    result = write_message(msg, env, output_options, processing_options)
    assert result is None
    assert env.stdout.getvalue() == b''

def test_write_message_writes_request_body(tmp_path):
    env = DummyEnv()
    body_content = b'hello world'
    msg = RequestsMessage(kind=RequestsMessageKind.REQUEST, headers=HTTPHeadersDict(), body=body_content)
    output_options = OutputOptions(kind=RequestsMessageKind.REQUEST, body=True)
    processing_options = ProcessingOptions()
    write_message(msg, env, output_options, processing_options)
    # The output should contain the body content
    assert body_content in env.stdout.getvalue()

def test_write_message_handles_broken_pipe(tmp_path):
    env = DummyEnv()
    # Simulate a broken pipe by raising OSError with errno.EPIPE on flush
    class BrokenPipeFile(io.BytesIO):
        def flush(self):
            raise OSError(errno.EPIPE, "Broken pipe")
    env.stdout = BrokenPipeFile()
    msg = RequestsMessage(kind=RequestsMessageKind.REQUEST, headers=HTTPHeadersDict(), body=b'')
    output_options = OutputOptions(kind=RequestsMessageKind.REQUEST, body=True)
    processing_options = ProcessingOptions(show_traceback=False)
    # write_message should not raise when EPIPE occurs and show_traceback is False
    write_message(msg, env, output_options, processing_options)
    # After handling, the buffer should be empty (nothing written)
    assert env.stdout.getvalue() == b''
