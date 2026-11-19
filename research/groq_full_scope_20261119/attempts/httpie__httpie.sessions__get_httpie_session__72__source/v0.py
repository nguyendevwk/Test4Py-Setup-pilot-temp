import os
import builtins
import importlib
import types
import pytest
from pathlib import Path

# Import the target function
from httpie.sessions import get_httpie_session

# Helper to create a minimal Environment mock
class DummyEnvironment:
    def __init__(self):
        self._log_level = None
        self._log_file = None

    def log(self, *args, **kwargs):
        pass

# Dummy Session that records initialization arguments
class DummySession:
    def __init__(self, path, env, session_id, bound_host, suppress_legacy_warnings):
        self.path = path
        self.env = env
        self.session_id = session_id
        self.bound_host = bound_host
        self.suppress_legacy_warnings = suppress_legacy_warnings
        self.loaded = False

    def load(self):
        self.loaded = True

def test_anonymous_session_path_and_id(tmp_path, monkeypatch):
    # Patch Session to DummySession
    monkeypatch.setattr(importlib.import_module('httpie.sessions'), 'Session', DummySession)

    env = DummyEnvironment()
    config_dir = tmp_path
    session_name = "~/my_session"
    host = None
    url = "http://example.com"

    session = get_httpie_session(env, config_dir, session_name, host, url)

    # Path should be expanded user path
    expected_path = os.path.expanduser(session_name)
    assert session.path == expected_path
    # session_id should be the same as the path for anonymous sessions
    assert session.session_id == expected_path
    # bound_host should be stripped of port (none in this case)
    assert session.bound_host == "example.com"
    # load should have been called
    assert session.loaded is True

def test_named_session_path_and_id(tmp_path, monkeypatch):
    # Patch Session to DummySession
    monkeypatch.setattr(importlib.import_module('httpie.sessions'), 'Session', DummySession)

    env = DummyEnvironment()
    config_dir = tmp_path
    session_name = "my_session"
    host = "api.test.com:8080"
    url = "http://api.test.com/resource"

    session = get_httpie_session(env, config_dir, session_name, host, url)

    # Path should be inside config_dir with hostname-based directory
    expected_dirname = f"{host.split(':')[0]}-{session_name}"
    expected_path = config_dir / expected_dirname
    assert session.path == expected_path
    # session_id should be the session name
    assert session.session_id == session_name
    # bound_host should be stripped of port
    assert session.bound_host == "api.test.com"
    # load should have been called
    assert session.loaded is True

def test_missing_host_fallback_to_localhost(tmp_path, monkeypatch):
    # Patch Session to DummySession
    monkeypatch.setattr(importlib.import_module('httpie.sessions'), 'Session', DummySession)

    env = DummyEnvironment()
    config_dir = tmp_path
    session_name = "anon"
    host = None
    # URL without hostname (e.g., unix socket)
    url = "unix:///tmp/socket"

    session = get_httpie_session(env, config_dir, session_name, host, url)

    # Since url_as_host would return None, fallback to 'localhost'
    assert session.bound_host == "localhost"
    # Path should be expanded user path for anonymous session
    expected_path = os.path.expanduser(session_name)
    assert session.path == expected_path
    # session_id should match the path
    assert session.session_id == expected_path
    assert session.loaded is True
