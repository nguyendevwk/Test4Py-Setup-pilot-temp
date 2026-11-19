import argparse
import json
import os
import tempfile
from httpie.client import make_request_kwargs, finalize_headers, json_dict_to_request_body
from httpie.cli.dicts import HTTPHeadersDict
from httpie.context import Environment

def _make_args(**kwargs):
    """Helper to create an argparse.Namespace with default attributes."""
    defaults = {
        'method': 'GET',
        'url': 'http://example.com',
        'headers': {},
        'data': None,
        'json': False,
        'form': False,
        'files': None,
        'multipart': False,
        'multipart_data': None,
        'boundary': None,
        'auth': None,
        'params': {},
        'offline': False,
        'chunked': False,
    }
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)

def test_json_body_and_headers(tmp_path):
    """When data is a dict and json flag is set, body is JSON and headers are correct."""
    env = Environment()
    data = {'key': 'value'}
    args = _make_args(data=data, json=True)
    kwargs = make_request_kwargs(env, args)
    # Body should be JSON string
    assert kwargs['data'] == json.dumps(data)
    # Headers should contain JSON content type
    headers = kwargs['headers']
    assert headers['Content-Type'] == b'application/json'
    assert headers['Accept'] == b'application/json, */*;q=0.5'

def test_multipart_with_files(tmp_path):
    """When form is true and files are provided, multipart data is generated."""
    env = Environment()
    # Create a temporary file to act as upload
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    args = _make_args(
        form=True,
        files=[str(file_path)],
        multipart_data={'field': 'value'},
        boundary='myboundary',
    )
    kwargs = make_request_kwargs(env, args)
    # The data should be a multipart body (bytes)
    assert isinstance(kwargs['data'], bytes)
    # Content-Type header should include boundary
    assert 'boundary=myboundary' in kwargs['headers']['Content-Type'].decode()
    # The multipart body should contain the file content
    assert b'content' in kwargs['data']

def test_offline_chunked_header_added(tmp_path):
    """When offline and chunked, Transfer-Encoding header is added if missing."""
    env = Environment()
    args = _make_args(
        offline=True,
        chunked=True,
        headers={},  # no Transfer-Encoding
    )
    kwargs = make_request_kwargs(env, args)
    headers = kwargs['headers']
    # Transfer-Encoding should be set to 'chunked'
    assert headers['Transfer-Encoding'] == b'chunked'
    # Ensure other headers remain untouched
    assert headers['User-Agent'].startswith(b'HTTPie/')
