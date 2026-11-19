import io
import os
import pytest
from httpie.uploads import prepare_request_body
from httpie.context import Environment
from httpie.cli.dicts import RequestDataDict

# Helper callback that simply returns the data unchanged
def identity_callback(data: bytes) -> bytes:
    return data

@pytest.fixture
def env():
    # Create a minimal Environment instance; defaults are sufficient for the tests
    return Environment()

def test_prepare_request_body_with_bytes(env, tmp_path):
    """
    When raw_body is bytes and not offline or chunked,
    prepare_request_body should return the same bytes object.
    """
    data = b"hello world"
    result = prepare_request_body(
        env=env,
        raw_body=data,
        body_read_callback=identity_callback,
        offline=False,
        chunked=False
    )
    assert isinstance(result, bytes)
    assert result == data

def test_prepare_request_body_with_file_offline(env, tmp_path):
    """
    When raw_body is a file-like object and offline=True,
    prepare_request_body should read the file and return its bytes.
    """
    file_path = tmp_path / "sample.txt"
    file_path.write_text("file content")
    with open(file_path, "rb") as f:
        result = prepare_request_body(
            env=env,
            raw_body=f,
            body_read_callback=identity_callback,
            offline=True,
            chunked=False
        )
    assert isinstance(result, bytes)
    assert result == b"file content"

def test_prepare_request_body_with_requestdatadict(env):
    """
    When raw_body is a RequestDataDict, the function should URL‑encode it
    and return the resulting bytes.
    """
    data = RequestDataDict({"a": "1", "b": ["x", "y"]})
    result = prepare_request_body(
        env=env,
        raw_body=data,
        body_read_callback=identity_callback,
        offline=False,
        chunked=False
    )
    assert isinstance(result, bytes)
    # The order of query parameters is not guaranteed, so we check both possibilities
    assert result in (b"a=1&b=x&b=y", b"b=x&b=y&a=1")
