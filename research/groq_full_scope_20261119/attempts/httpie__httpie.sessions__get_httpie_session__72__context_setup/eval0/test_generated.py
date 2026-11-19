import os
import pytest
from pathlib import Path
from httpie.sessions import get_httpie_session, is_anonymous_session, session_hostname_to_dirname, strip_port
from httpie.context import Environment

# Helper to create a minimal Environment instance
def make_env():
    # Environment is used only for attribute storage; a simple object suffices
    return Environment()

@pytest.fixture
def tmp_config_dir(tmp_path):
    return tmp_path

def test_anonymous_session_path_and_id(tmp_config_dir):
    env = make_env()
    # Anonymous session name contains a path separator
    anon_name = os.path.join("~", "my_session")
    url = "http://example.com/api"
    session = get_httpie_session(env, tmp_config_dir, anon_name, None, url)
    # Path should be expanded user path
    expected_path = Path(os.path.expanduser(anon_name))
    assert session.path == expected_path
    # session_id should be the expanded path
    assert session.session_id == expected_path
    # bound_host should be stripped of port (none here)
    assert session.bound_host == "example.com"

def test_normal_session_path_and_id(tmp_config_dir):
    env = make_env()
    session_name = "my_session"
    url = "https://example.com:8080/api"
    session = get_httpie_session(env, tmp_config_dir, session_name, None, url)
    # hostname derived from URL
    hostname = "example.com:8080"
    # Path should be under config_dir/sessions/hostname/session_name.json
    expected_path = tmp_config_dir / session_hostname_to_dirname(hostname, session_name)
    assert session.path == expected_path
    # session_id should be the session name
    assert session.session_id == session_name
    # bound_host should be stripped of port
    assert session.bound_host == "example.com"

def test_host_override_and_legacy_warning_flag(tmp_config_dir):
    env = make_env()
    session_name = "override_session"
    url = "http://example.com/api"
    # Override host with port
    host = "override.com:9090"
    session = get_httpie_session(env, tmp_config_dir, session_name, host, url, suppress_legacy_warnings=True)
    # bound_host should be stripped of port
    assert session.bound_host == "override.com"
    # suppress_legacy_warnings flag should be set
    assert session.suppress_legacy_warnings is True
