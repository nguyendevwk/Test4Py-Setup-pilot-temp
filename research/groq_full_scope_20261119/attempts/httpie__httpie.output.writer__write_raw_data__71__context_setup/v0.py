import io
import os
import errno
import pytest
from httpie.output.writer import write_raw_data
from httpie.context import Environment
from httpie.models import OutputOptions, ProcessingOptions
from httpie.cli.dicts import HTTPHeadersDict

# Helper to create a minimal Environment that writes to a temporary file
class DummyEnv(Environment):
    def __init__(self, tmp_path):
        super().__init__()
        self.stdout = open(tmp_path / "out.txt", "wb")
        self.stderr = io.StringIO()
        self.stdout_isatty = True
        self.is_windows = False
        self.stdout.buffer = self.stdout  # ensure buffer attribute

    def close(self):
        self.stdout.close()


def test_write_raw_data_writes_bytes(tmp_path):
    env = DummyEnv(tmp_path)
    data = b"Hello, world!"
    write_raw_data(env, data)
    env.close()
    with open(tmp_path / "out.txt", "rb") as f:
        content = f.read()
    assert content == data


def test_write_raw_data_empty_bytes(tmp_path):
    env = DummyEnv(tmp_path)
    data = b""
    write_raw_data(env, data)
    env.close()
    with open(tmp_path / "out.txt", "rb") as f:
        content = f.read()
    assert content == b""


def test_write_raw_data_with_headers_and_processing_options(tmp_path):
    env = DummyEnv(tmp_path)
    data = b"Header test"
    headers = HTTPHeadersDict({"Content-Type": "text/plain"})
    processing_options = ProcessingOptions(stream=True)
    write_raw_data(env, data, headers=headers, processing_options=processing_options)
    env.close()
    with open(tmp_path / "out.txt", "rb") as f:
        content = f.read()
    # The output should contain the raw data; headers are not printed by write_raw_data
    assert content == data
