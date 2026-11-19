import argparse
import json
import os
import tempfile
import urllib.parse
import pytest
from httpie.client import collect_messages
from httpie.context import Environment
from httpie.sessions import get_httpie_session
from httpie.models import RequestsMessage
from httpie.utils import repr_dict

# Helper to create a minimal Environment instance
class DummyEnvironment(Environment):
    def __init__(self, config_dir):
        super().__init__()
        self.config.directory = config_dir

# Helper to create argparse.Namespace with required attributes
def make_args(**kwargs):
    defaults = {
        "session": None,
        "session_read_only": None,
        "headers": {},
        "url": "http://example.com",
        "debug": False,
        "path_as_is": False,
        "compress": 0,
        "offline": True,
        "max_redirects": None,
        "follow": False,
        "all": False,
        "max_headers": 2000,
        "ssl_version": None,
        "ciphers": None,
        "auth_plugin": None,
    }
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)

def test_collect_messages_yields_prepared_request(tmp_path):
    env = DummyEnvironment(tmp_path)
    args = make_args()
    messages = list(collect_messages(env, args))
    # Should yield exactly one PreparedRequest
    assert len(messages) == 1
    req = messages[0]
    assert req.method == "GET"
    assert req.url == args.url
    # Headers should include User-Agent from httpie
    assert "User-Agent" in req.headers

def test_collect_messages_includes_session_headers(tmp_path):
    env = DummyEnvironment(tmp_path)
    # Create a session with a custom header
    session_name = "testsession"
    session = get_httpie_session(
        env=env,
        config_dir=tmp_path,
        session_name=session_name,
        host=None,
        url=None,
    )
    session.headers.update({"X-Custom": "value"})
    session.save()
    args = make_args(session=session_name)
    messages = list(collect_messages(env, args))
    req = messages[0]
    # Session header should be present
    assert req.headers.get("X-Custom") == "value"

def test_collect_messages_path_as_is(tmp_path):
    env = DummyEnvironment(tmp_path)
    # URL with query and fragment
    url = "http://example.com/path?query=1#frag"
    args = make_args(url=url, path_as_is=True)
    messages = list(collect_messages(env, args))
    req = messages[0]
    # ensure_path_as_is should keep the original path
    parsed = urllib.parse.urlparse(req.url)
    assert parsed.path == "/path"
    assert parsed.query == "query=1"
    assert parsed.fragment == "frag"
