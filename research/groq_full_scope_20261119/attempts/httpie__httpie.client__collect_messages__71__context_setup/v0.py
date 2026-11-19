import argparse
import http.client
import json
import sys
import types
import urllib3
import requests
import pytest
from httpie.client import collect_messages
from httpie.context import Environment
from httpie.sessions import get_httpie_session
from httpie.models import RequestsMessage

# Helper to create a minimal Environment
class DummyEnv(Environment):
    def __init__(self):
        self.config = types.SimpleNamespace(directory="/tmp")

def make_args(**kwargs):
    defaults = {
        "method": "GET",
        "url": "http://example.com",
        "headers": {},
        "files": None,
        "data": None,
        "json": False,
        "form": False,
        "multipart": False,
        "multipart_data": None,
        "boundary": None,
        "auth": None,
        "params": [],
        "timeout": None,
        "verify": "yes",
        "cert": None,
        "cert_key": None,
        "cert_key_pass": types.SimpleNamespace(value=None),
        "proxy": [],
        "session": None,
        "session_read_only": None,
        "auth_plugin": None,
        "debug": False,
        "path_as_is": False,
        "compress": 0,
        "offline": False,
        "chunked": False,
        "max_headers": None,
        "max_redirects": None,
        "follow": False,
        "all": False,
        "ssl_version": None,
        "ciphers": None,
    }
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)

def test_collect_messages_yields_prepared_request_offline(tmp_path):
    env = DummyEnv()
    args = make_args(offline=True)
    msgs = list(collect_messages(env, args))
    # Should yield exactly one PreparedRequest and stop before sending
    assert len(msgs) == 1
    req = msgs[0]
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == "GET"
    assert req.url == "http://example.com"
    # No response should be yielded
    assert all(isinstance(m, requests.PreparedRequest) for m in msgs)

def test_collect_messages_path_as_is(tmp_path):
    env = DummyEnv()
    # Original URL has a path that would normally be normalized
    orig_url = "http://example.com/../"
    args = make_args(url=orig_url, path_as_is=True)
    msgs = list(collect_messages(env, args))
    assert len(msgs) == 1
    req = msgs[0]
    assert isinstance(req, requests.PreparedRequest)
    # The path should remain '/../' after preparation
    assert req.url.startswith("http://example.com/../")
    # Ensure query string is preserved if any
    assert req.url == "http://example.com/../"

def test_collect_messages_session_cookies(tmp_path):
    env = DummyEnv()
    # Create a temporary session file to simulate cookie persistence
    session_name = "testsession"
    session_path = tmp_path / f"{session_name}.json"
    # Write a dummy session with a cookie
    session_path.write_text(json.dumps({"cookies": {"foo": "bar"}}))
    args = make_args(session=session_name, offline=True)
    msgs = list(collect_messages(env, args))
    # Should yield a PreparedRequest with the cookie header set
    req = msgs[0]
    assert isinstance(req, requests.PreparedRequest)
    assert req.headers.get("Cookie") == "foo=bar"
