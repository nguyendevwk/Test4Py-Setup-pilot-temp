import argparse
import json
import os
import tempfile
import pytest
from httpie.client import make_request_kwargs
from httpie.context import Environment
from httpie.cli.dicts import HTTPHeadersDict

# Helper to create a minimal Environment
def create_env(tmp_path):
    env = Environment()
    env.tmp_path = tmp_path
    return env

def test_json_serialization_and_headers(tmp_path):
    env = create_env(tmp_path)
    args = argparse.Namespace(
        method="POST",
        url="http://example.com/api",
        data={"key": "value"},
        json=True,
        form=False,
        files=None,
        multipart=False,
        boundary=None,
        headers=HTTPHeadersDict(),
        offline=False,
        chunked=False,
        auth=None,
        params=HTTPHeadersDict(),
        multipart_data=None,
    )
    kwargs = make_request_kwargs(env, args)
    # Body should be JSON string
    assert kwargs["data"] == json.dumps({"key": "value"}).encode("utf-8")
    # Method lowercased
    assert kwargs["method"] == "post"
    # URL unchanged
    assert kwargs["url"] == "http://example.com/api"
    # No Content-Type header added by default
    assert "Content-Type" not in kwargs["headers"]

def test_multipart_with_file(tmp_path):
    env = create_env(tmp_path)
    # Create a temporary file to upload
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    args = argparse.Namespace(
        method="PUT",
        url="http://example.com/upload",
        data=None,
        json=False,
        form=False,
        files=[str(file_path)],
        multipart=True,
        boundary="myboundary",
        headers=HTTPHeadersDict(),
        offline=False,
        chunked=False,
        auth=None,
        params=HTTPHeadersDict(),
        multipart_data=None,
    )
    kwargs = make_request_kwargs(env, args)
    # Body should be multipart encoded
    body = kwargs["data"]
    assert isinstance(body, bytes)
    assert b"Content-Disposition: form-data; name=\"file\"; filename=\"test.txt\"" in body
    # Content-Type header should be set
    assert kwargs["headers"]["Content-Type"].startswith("multipart/form-data; boundary=myboundary")

def test_form_and_json_precedence(tmp_path):
    env = create_env(tmp_path)
    args = argparse.Namespace(
        method="POST",
        url="http://example.com/form",
        data={"a": "b"},
        json=False,
        form=True,
        files=None,
        multipart=False,
        boundary=None,
        headers=HTTPHeadersDict(),
        offline=False,
        chunked=False,
        auth=None,
        params=HTTPHeadersDict(),
        multipart_data=None,
    )
    kwargs = make_request_kwargs(env, args)
    # When form=True, data should not be JSON serialized
    assert kwargs["data"] == b"a=b"
    # No JSON header added
    assert "Content-Type" not in kwargs["headers"]
