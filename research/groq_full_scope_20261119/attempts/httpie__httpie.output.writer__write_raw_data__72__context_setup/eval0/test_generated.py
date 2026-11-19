import io
import sys
import pytest
from httpie.output.writer import write_raw_data
from httpie.context import Environment
from httpie.models import OutputOptions, ProcessingOptions
from httpie.cli.dicts import HTTPHeadersDict

# Minimal Environment stub for testing
class DummyEnv(Environment):
    def __init__(self):
        super().__init__()
        self.stdout = io.BytesIO()
        self.stderr = io.BytesIO()
        self.stdout_isatty = False
        self.is_windows = False
        self.stderr_isatty = False

def test_write_raw_data_writes_bytes_to_stdout():
    env = DummyEnv()
    data = b"hello world"
    write_raw_data(env, data)
    env.stdout.seek(0)
    assert env.stdout.read() == b"hello world"

def test_write_raw_data_includes_headers_in_message():
    env = DummyEnv()
    data = b"test"
    headers = HTTPHeadersDict({"Content-Type": "text/plain"})
    write_raw_data(env, data, headers=headers)
    env.stdout.seek(0)
    # The output should contain the header line followed by the body
    output = env.stdout.read().decode()
    assert "Content-Type: text/plain" in output
    assert output.strip().endswith("test")

def test_write_raw_data_returns_none_and_handles_empty_processing_options():
    env = DummyEnv()
    data = b"sample"
    result = write_raw_data(env, data, processing_options=ProcessingOptions())
    assert result is None
    env.stdout.seek(0)
    assert env.stdout.read() == b"sample"
