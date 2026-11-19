import io
import os
import pytest
from httpie.uploads import prepare_request_body
from httpie.cli.dicts import RequestDataDict
from httpie.context import Environment
from httpie.uploads import ChunkedUploadStream

# Helper callback that records bytes read
def dummy_callback(data: bytes):
    dummy_callback.read_bytes += data
dummy_callback.read_bytes = b''

@pytest.fixture
def env():
    return Environment()

def test_prepare_request_body_with_bytes_and_offline(env, tmp_path):
    # Create a temporary file to read from
    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello world")
    with open(file_path, "rb") as f:
        body = prepare_request_body(
            env=env,
            raw_body=f,
            body_read_callback=dummy_callback,
            offline=True
        )
    # When offline, the function should return the file contents as bytes
    assert isinstance(body, bytes)
    assert body == b"hello world"
    # The callback should not have been called because offline bypasses reading
    assert dummy_callback.read_bytes == b''

def test_prepare_request_body_with_request_data_dict(env):
    data = RequestDataDict({"a": "1", "b": ["x", "y"]})
    body = prepare_request_body(
        env=env,
        raw_body=data,
        body_read_callback=dummy_callback,
        offline=False,
        chunked=False
    )
    # The body should be URL‑encoded bytes
    assert isinstance(body, bytes)
    # Order of parameters is not guaranteed, but both must be present
    assert b"a=1" in body
    assert b"b=x" in body
    assert b"b=y" in body

def test_prepare_request_body_with_chunked_stream(env):
    data = b"chunked data"
    stream = prepare_request_body(
        env=env,
        raw_body=data,
        body_read_callback=dummy_callback,
        offline=False,
        chunked=True
    )
    # The returned object should be a ChunkedUploadStream
    assert isinstance(stream, ChunkedUploadStream)
    # Reading from the stream should yield the original data
    read_data = stream.read()
    assert read_data == data
    # The callback should have been called with the data chunk
    assert dummy_callback.read_bytes == data
