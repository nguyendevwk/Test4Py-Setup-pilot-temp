import argparse
import json
import os
import tempfile
import urllib.parse
import pytest
from httpie.client import collect_messages
from httpie.context import Environment
from httpie.sessions import get_httpie_session
from httpie.uploads import compress_request

# Helper to create a minimal Environment with a temporary config directory
@pytest.fixture
def env(tmp_path):
    env = Environment()
    env.config.directory = tmp_path
    return env

# Helper to create argparse.Namespace with required attributes
def make_args(**kwargs):
    defaults = {
        'session': None,
        'session_read_only': None,
        'headers': {},
        'url': '',
        'method': 'GET',
        'data': None,
        'json': None,
        'auth_plugin': None,
        'debug': False,
        'path_as_is': False,
        'compress': 0,
        'offline': False,
        'max_redirects': None,
        'follow': False,
        'all': False,
        'max_headers': None,
        'ssl_version': None,
        'ciphers': None,
        'verify': True,
    }
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)

def test_collect_messages_yields_prepared_request_offline(env):
    """When offline, collect_messages yields only the prepared request."""
    args = make_args(
        url='http://example.com',
        method='GET',
        offline=True,
    )
    msgs = list(collect_messages(env, args))
    assert len(msgs) == 1
    req = msgs[0]
    assert req.method == 'GET'
    assert req.url == 'http://example.com'
    # No response should be yielded
    assert not hasattr(req, 'status_code')

def test_collect_messages_path_as_is_preserves_encoded_path(env):
    """When path_as_is is set, the URL path is not modified."""
    encoded_path = '/path%20with%20space'
    args = make_args(
        url=f'http://example.com{encoded_path}',
        method='GET',
        path_as_is=True,
        offline=True,
    )
    msgs = list(collect_messages(env, args))
    req = msgs[0]
    # The prepared URL should keep the encoded space
    assert urllib.parse.urlparse(req.url).path == '/path%20with%20space'

def test_collect_messages_compress_request_called(env, monkeypatch):
    """When compress is enabled and a body is present, compress_request is invoked."""
    body = b'{"key":"value"}'
    called = {'flag': False}
    def fake_compress_request(request, always):
        called['flag'] = True
        # Ensure body is unchanged for this test
        assert request.body == body
    monkeypatch.setattr('httpie.uploads.compress_request', fake_compress_request)

    args = make_args(
        url='http://example.com',
        method='POST',
        data=body,
        compress=1,
        offline=True,
    )
    # Provide a callback that simply records the body
    def body_callback(b):
        assert b == body
    msgs = list(collect_messages(env, args, request_body_read_callback=body_callback))
    req = msgs[0]
    assert called['flag'] is True
    assert req.body == body
