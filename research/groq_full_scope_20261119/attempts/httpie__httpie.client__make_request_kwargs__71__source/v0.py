import argparse
import json
import os
import tempfile
import pytest
from httpie.client import make_request_kwargs
from httpie.context import Environment
from httpie.cli.dicts import HTTPHeadersDict

# Helper to create a minimal Environment instance
class DummyEnvironment(Environment):
    def __init__(self):
        super().__init__(None)

def test_make_request_kwargs_with_json_and_headers(tmp_path):
    env = DummyEnvironment()
    ns = argparse.Namespace(
        method="POST",
        url="http://example.com/api",
        data={"key": "value"},
        json=True,
        form=False,
        files=None,
        multipart=False,
        boundary=None,
        headers=HTTPHeadersDict({"X-Custom": "123"}),
        auth=None,
        params={},
        offline=False,
        chunked=False,
    )
    kwargs = make_request_kwargs(env, ns)
    # Body should be JSON string
    assert kwargs["method"] == "post"
    assert kwargs["url"] == "http://example.com/api"
    assert kwargs["headers"]["X-Custom"] == "123"
    # The body should be a bytes object containing JSON
    body = kwargs["data"]
    assert isinstance(body, bytes)
    assert json.loads(body.decode("utf-8")) == {"key": "value"}
    # No Content-Length header should be set automatically
    assert "Content-Length" not in kwargs["headers"]

def test_make_request_kwargs_with_multipart_and_files(tmp_path):
    env = DummyEnvironment()
    # Create a temporary file to upload
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello world")
    ns = argparse.Namespace(
        method="PUT",
        url="http://example.com/upload",
        data=None,
        json=False,
        form=True,
        files=[str(file_path)],
        multipart=True,
        boundary="myboundary",
        headers=HTTPHeadersDict({"Content-Type": "multipart/form-data"}),
        auth=None,
        params={},
        offline=False,
        chunked=False,
    )
    kwargs = make_request_kwargs(env, ns)
    # The body should be a generator yielding multipart data
    body = kwargs["data"]
    # Consume the generator to get the multipart payload
    payload = b"".join(body)
    # Check that the payload contains the file content and boundary
    assert b"hello world" in payload
    assert b"--myboundary" in payload
    # Content-Type header should be set correctly
    assert kwargs["headers"]["Content-Type"].startswith("multipart/form-data")

def test_make_request_kwargs_offline_chunked_header(tmp_path):
    env = DummyEnvironment()
    ns = argparse.Namespace(
        method="GET",
        url="http://example.com/stream",
        data=None,
        json=False,
        form=False,
        files=None,
        multipart=False,
        boundary=None,
        headers=HTTPHeadersDict(),
        auth=None,
        params={},
        offline=True,
        chunked=True,
    )
    kwargs = make_request_kwargs(env, ns)
    # When offline and chunked, Transfer-Encoding should be set to chunked
    assert kwargs["headers"]["Transfer-Encoding"] == "chunked"
    # The body should be empty for a GET request
    body = kwargs["data"]
    assert body == b""
