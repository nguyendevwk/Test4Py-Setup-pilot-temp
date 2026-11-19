import os
import pytest
from pathlib import Path
from httpie.sessions import get_httpie_session, is_anonymous_session, session_hostname_to_dirname, strip_port
from httpie.context import Environment

class DummyEnv(Environment):
    """Minimal Environment stub for testing purposes."""
    def __init__(self):
        super().__init__(config_dir=Path('.'))

def test_anonymous_session_path_expansion(tmp_path: Path):
    """Anonymous session names containing a path separator should be expanded to an absolute path."""
    env = DummyEnv()
    config_dir = tmp_path
    session_name = os.path.join('~', 'my_session')
    url = 'https://example.com'
    session = get_httpie_session(env, config_dir, session_name, host=None, url=url)
    expected_path = Path(os.path.expanduser(session_name))
    assert session.path == expected_path
    assert session.session_id == expected_path
    assert session.bound_host == 'example.com'

def test_named_session_path_and_hostname(tmp_path: Path):
    """Named session should be stored under config_dir/sessions/<hostname>/<session_name>.json."""
    env = DummyEnv()
    config_dir = tmp_path
    session_name = 'my_session'
    url = 'https://example.com:8080'
    session = get_httpie_session(env, config_dir, session_name, host=None, url=url)
    expected_dirname = session_hostname_to_dirname('example.com:8080', session_name)
    expected_path = config_dir / expected_dirname
    assert session.path == expected_path
    assert session.session_id == session_name
    assert session.bound_host == 'example.com'

def test_host_port_stripping_and_default_host(tmp_path: Path):
    """Bound host should have port stripped; if no host, default to 'localhost'."""
    env = DummyEnv()
    config_dir = tmp_path
    session_name = 'anon'
    url_with_port = 'http://localhost:5000/api'
    session = get_httpie_session(env, config_dir, session_name, host=None, url=url_with_port)
    assert session.bound_host == 'localhost'
    url_no_host = 'http+unix://%2Fvar%2Frun%2Fsocket.sock'
    session2 = get_httpie_session(env, config_dir, session_name, host=None, url=url_no_host)
    assert session2.bound_host == 'localhost'
