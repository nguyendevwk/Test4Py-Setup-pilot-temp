import os
import pytest
from pathlib import Path
from httpie.sessions import get_httpie_session, Session as RealSession

# Dummy Session to intercept initialization without invoking real logic
class DummySession:
    def __init__(self, path, env=None, session_id=None, bound_host=None, suppress_legacy_warnings=False):
        self.path = Path(path)
        self.env = env
        self.session_id = session_id
        self.bound_host = bound_host
        self.suppress_legacy_warnings = suppress_legacy_warnings
        self.loaded = False

    def load(self):
        self.loaded = True

@pytest.fixture
def patch_session(monkeypatch):
    monkeypatch.setattr("httpie.sessions.Session", DummySession)

def test_anonymous_session_path_expansion(patch_session, tmp_path):
    env = object()
    config_dir = tmp_path
    session_name = "~/my_session"
    url = "https://example.com/api"
    session = get_httpie_session(env, config_dir, session_name, host=None, url=url)
    expected_path = Path(os.path.expanduser(session_name))
    assert session.path == expected_path
    assert session.session_id == expected_path
    assert session.bound_host == "example.com"
    assert session.loaded is True

def test_named_session_with_host(patch_session, tmp_path):
    env = object()
    config_dir = tmp_path
    session_name = "my_session"
    host = "api.example.com"
    url = "https://example.com/api"
    session = get_httpie_session(env, config_dir, session_name, host=host, url=url)
    expected_dir = config_dir / f"{host}_{session_name}"
    assert session.path == expected_dir
    assert session.session_id == session_name
    assert session.bound_host == host
    assert session.loaded is True

def test_missing_host_defaults_to_localhost(patch_session, tmp_path):
    env = object()
    config_dir = tmp_path
    session_name = "my_session"
    url = "unix://tmp/socket"
    session = get_httpie_session(env, config_dir, session_name, host=None, url=url)
    expected_dir = config_dir / f"localhost_{session_name}"
    assert session.path == expected_dir
    assert session.session_id == session_name
    assert session.bound_host == "localhost"
    assert session.loaded is True
