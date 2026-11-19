import os
import pytest
from pathlib import Path
from httpie.sessions import get_httpie_session, Session
from httpie.context import Environment

@pytest.fixture
def env():
    # Minimal Environment instance; defaults are sufficient for session creation
    return Environment()

def test_anonymous_session_path(tmp_path, env):
    # Anonymous session: path should be expanded user path
    anon_name = "~/my_session"
    config_dir = tmp_path
    url = "http://example.com"
    # Create an empty file at the expanded path to satisfy load()
    expanded_path = Path(os.path.expanduser(anon_name))
    expanded_path.parent.mkdir(parents=True, exist_ok=True)
    expanded_path.touch()
    session = get_httpie_session(env, config_dir, anon_name, None, url)
    assert session.path == expanded_path
    assert session.session_id == expanded_path
    assert session.bound_host == "example.com"

def test_named_session_path_and_bound_host(tmp_path, env):
    # Named session: path should be under config_dir with hostname dir
    session_name = "my_session"
    host = "example.com"
    url = "http://example.com"
    config_dir = tmp_path
    # Expected path: config_dir / "example.com-my_session"
    expected_path = config_dir / "example.com-my_session"
    expected_path.touch()
    session = get_httpie_session(env, config_dir, session_name, host, url)
    assert session.path == expected_path
    assert session.session_id == session_name
    assert session.bound_host == "example.com"

def test_bound_host_port_stripping(tmp_path, env):
    # When URL contains a port, bound_host should strip it
    session_name = "port_test"
    host = None
    url = "http://example.com:8080/path"
    config_dir = tmp_path
    # Create empty file at expected path
    expected_path = config_dir / "example.com-port_test"
    expected_path.touch()
    session = get_httpie_session(env, config_dir, session_name, host, url)
    assert session.bound_host == "example.com"
    assert session.path == expected_path
