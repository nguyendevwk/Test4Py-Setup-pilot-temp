import io
import pytest
from httpie.output.writer import write_raw_data
from httpie.context import Environment
from httpie.cli.dicts import HTTPHeadersDict
from httpie.models import OutputOptions, ProcessingOptions

# Helper Environment that captures written data
class DummyEnv(Environment):
    def __init__(self):
        super().__init__()
        self.stdout = io.BytesIO()

def test_write_raw_data_bytes_output():
    """write_raw_data should write raw bytes unchanged to env.stdout."""
    env = DummyEnv()
    data = b"Hello, world!"
    write_raw_data(env, data)
    env.stdout.seek(0)
    assert env.stdout.read() == data

def test_write_raw_data_with_headers():
    """Headers passed to write_raw_data should be attached to the prepared request."""
    env = DummyEnv()
    data = b"data"
    headers = HTTPHeadersDict({"X-Test": "value"})
    result = write_raw_data(env, data, headers=headers)
    # The returned object should be a requests.PreparedRequest
    assert hasattr(result, "headers")
    assert result.headers.get("X-Test") == "value"

def test_write_raw_data_processing_options_passed():
    """ProcessingOptions should be forwarded to write_message without altering output."""
    env = DummyEnv()
    data = b"sample"
    proc_opts = ProcessingOptions()
    proc_opts.pretty = False  # example flag
    write_raw_data(env, data, processing_options=proc_opts)
    env.stdout.seek(0)
    assert env.stdout.read() == data
