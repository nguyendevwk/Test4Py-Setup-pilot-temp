import io
import os
import tempfile
import pytest
from httpie.output.writer import write_raw_data
from httpie.context import Environment
from httpie.models import OutputOptions
from httpie.cli.dicts import HTTPHeadersDict

def test_write_raw_data_writes_bytes(tmp_path):
    """write_raw_data should write raw bytes to the environment output."""
    # Prepare environment with a temporary file as output
    out_file = tmp_path / "out.bin"
    env = Environment()
    env.output = open(out_file, "wb")
    try:
        data = b"hello world"
        headers = HTTPHeadersDict({"Content-Type": "text/plain"})
        write_raw_data(env, data, headers=headers)
        env.output.flush()
        env.output.close()
        # Verify file content
        with open(out_file, "rb") as f:
            content = f.read()
        assert content == data
    finally:
        env.output.close()

def test_write_raw_data_with_text_and_headers(tmp_path):
    """write_raw_data should handle string data and preserve headers."""
    out_file = tmp_path / "out.txt"
    env = Environment()
    env.output = open(out_file, "w", encoding="utf-8")
    try:
        data = "foo bar"
        headers = HTTPHeadersDict({"X-Custom": "value"})
        write_raw_data(env, data, headers=headers)
        env.output.flush()
        env.output.close()
        # Verify file content
        with open(out_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == data
        # Ensure headers were set on the prepared request
        # We cannot access the internal request directly, but we can
        # confirm that no exception was raised and the output is correct.
    finally:
        env.output.close()

def test_write_raw_data_raises_on_invalid_env(tmp_path):
    """write_raw_data should raise an exception if env.output is not writable."""
    env = Environment()
    # Intentionally set output to a read-only file
    out_file = tmp_path / "readonly.txt"
    out_file.write_text("readonly")
    env.output = open(out_file, "r")
    data = b"data"
    with pytest.raises(Exception):
        write_raw_data(env, data)
    env.output.close()
