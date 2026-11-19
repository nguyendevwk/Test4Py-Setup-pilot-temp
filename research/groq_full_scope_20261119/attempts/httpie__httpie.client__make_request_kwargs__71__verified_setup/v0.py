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
    assert kwargs["headers"]["Content-Type"] == "application/json"
    body = kwargs["data"]
    # body is a file-like object; read it
    assert json.loads(body.read()) == {"key": "value"}
    assert kwargs["auth"] is None
    assert kwargs["params"] == []

def test_make_request_kwargs_with_multipart_and_files(tmp_path):
    env = DummyEnvironment()
    # create a temporary file to upload
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
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
        auth=("user", "pass"),
        params={"q": "search"},
        offline=False,
        chunked=False,
    )
    kwargs = make_request_kwargs(env, ns)
    # multipart data should be bytes with boundary
    body = kwargs["data"]
    body_bytes = body.read()
    assert b"myboundary" in body_bytes
    assert b"Content-Disposition: form-data; name=\"file\"; filename=\"test.txt\"" in body_bytes
    assert kwargs["auth"] == ("user", "pass")
    assert kwargs["params"] == [("q", "search")]

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
    # When offline and chunked, Transfer-Encoding should be set
    assert kwargs["headers"]["Transfer-Encoding"] == "chunked"
    # No Content-Length header should be present
    assert "Content-Length" not in kwargs["headers"]
