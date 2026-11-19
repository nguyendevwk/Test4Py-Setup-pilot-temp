import io
import os
import pytest
from httpie.uploads import prepare_request_body, ChunkedUploadStream
from httpie.context import Environment
from httpie.cli.dicts import RequestDataDict

# Helper callback that records the number of bytes read
class ReadCounter:
    def __init__(self):
        self.total = 0
    def __call__(self, chunk: bytes) -> bytes:
        self.total += len(chunk)
        return chunk

@pytest.fixture
def env():
    # Minimal Environment instance; attributes are not used in prepare_request_body
    return Environment()

def test_prepare_request_body_with_string(env):
    """Body is a plain string; should be returned as bytes."""
    counter = ReadCounter()
    result = prepare_request_body(
        env=env,
        raw_body="hello world",
        body_read_callback=counter,
        offline=False,
        chunked=False
    )
    assert isinstance(result, bytes)
    assert result == b"hello world"
    # No reading should have happened for non-file-like bodies
    assert counter.total == 0

def test_prepare_request_body_chunked_bytes(env):
    """Body is bytes and chunked=True; should return a ChunkedUploadStream."""
    counter = ReadCounter()
    body = b"chunked data"
    result = prepare_request_body(
        env=env,
        raw_body=body,
        body_read_callback=counter,
        offline=False,
        chunked=True
    )
    assert isinstance(result, ChunkedUploadStream)
    # Reading from the stream should trigger the callback
    data = result.read()
    assert data == body
    assert counter.total == len(body)

def test_prepare_request_body_file_like_offline(tmp_path, env):
    """File-like body with offline=True should return the file contents as bytes."""
    counter = ReadCounter()
    file_path = tmp_path / "test.txt"
    file_path.write_text("file content")
    with open(file_path, "rb") as f:
        result = prepare_request_body(
            env=env,
            raw_body=f,
            body_read_callback=counter,
            offline=True,
            chunked=False
        )
    assert isinstance(result, bytes)
    assert result == b"file content"
    # The callback should not be invoked for offline file reads
    assert counter.total == 0
