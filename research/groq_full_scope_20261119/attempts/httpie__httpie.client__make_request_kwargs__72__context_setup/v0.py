import argparse
import json
import os
import tempfile
from httpie.client import make_request_kwargs, json_dict_to_request_body
from httpie.cli.dicts import HTTPHeadersDict
from httpie.context import Environment
from httpie.sessions import get_httpie_session

def build_args(**kwargs):
    """Helper to create a Namespace with defaults."""
    ns = argparse.Namespace(
        method='GET',
        url='http://example.com',
        headers=HTTPHeadersDict(),
        data=None,
        json=False,
        form=False,
        files=None,
        multipart=False,
        multipart_data=None,
        boundary=None,
        auth=None,
        params={},
        offline=False,
        chunked=False,
    )
    ns.__dict__.update(kwargs)
    return ns

def test_make_request_kwargs_json_body_and_headers(tmp_path):
    env = Environment()
    # Create a JSON body
    data = {"key": "value"}
    args = build_args(
        method='POST',
        url='https://api.example.com',
        data=data,
        json=True,
        headers=HTTPHeadersDict({'X-Custom': '123'}),
    )
    kwargs = make_request_kwargs(env, args)
    # Method and URL
    assert kwargs['method'] == 'post'
    assert kwargs['url'] == 'https://api.example.com'
    # Headers contain JSON content type and custom header
    assert kwargs['headers']['Content-Type'] == b'application/json'
    assert kwargs['headers']['Accept'] == b'application/json, */*;q=0.5'
    assert kwargs['headers']['X-Custom'] == b'123'
    # Data is JSON string
    assert kwargs['data'] == json.dumps(data).encode('utf-8')
    # No auth or params
    assert kwargs['auth'] is None
    assert list(kwargs['params']) == []

def test_make_request_kwargs_form_with_files(tmp_path):
    env = Environment()
    # Create a temporary file to upload
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello world")
    args = build_args(
        method='PUT',
        url='http://localhost/upload',
        form=True,
        files=[str(file_path)],
        multipart=True,
        multipart_data={'field': 'value'},
        boundary='myboundary',
        headers=HTTPHeadersDict({'Content-Type': 'application/octet-stream'}),
    )
    kwargs = make_request_kwargs(env, args)
    # Method and URL
    assert kwargs['method'] == 'put'
    assert kwargs['url'] == 'http://localhost/upload'
    # Content-Type should be set by multipart helper
    assert kwargs['headers']['Content-Type'].startswith(b'multipart/form-data')
    # Data should be a generator yielding multipart bytes
    data = kwargs['data']
    assert hasattr(data, "__iter__") or hasattr(data, "__next__")
    # Ensure file content is present in the multipart body
    body = b"".join(data)
    assert b"hello world" in body
    # No auth or params
    assert kwargs['auth'] is None
    assert list(kwargs['params']) == []

def test_make_request_kwargs_empty_json_body():
    env = Environment()
    # Empty dict should result in empty string body
    args = build_args(
        method='POST',
        url='https://api.example.com/empty',
        data={},
        json=True,
    )
    kwargs = make_request_kwargs(env, args)
    # Body should be empty string to avoid requests assigning empty list
    assert kwargs['data'] == b''
    # Content-Type should still be set to application/json
    assert kwargs['headers']['Content-Type'] == b'application/json'
    # Accept header should be present
    assert kwargs['headers']['Accept'] == b'application/json, */*;q=0.5'
