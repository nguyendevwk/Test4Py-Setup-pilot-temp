import os
import pytest
from pathlib import Path

from httpie.sessions import (
    get_httpie_session,
    Session,
    Environment,
    session_hostname_to_dirname,
)
from httpie.context import LogLevel


def test_anonymous_session_path_expansion(tmp_path: Path):
    """Anonymous session names should be expanded to an absolute path."""
    env = Environment()
    config_dir = tmp_path
    session_name = "~/.httpie/session.json"
    url = "https://example.com/api"

    session = get_httpie_session(
        env=env,
        config_dir=config_dir,
        session_name=session_name,
        host=None,
        url=url,
    )

    # The session path should be the expanded user path
    expected_path = Path(os.path.expanduser(session_name))
    assert session.path == expected_path
    # The session_id should be the expanded path string
    assert session.session_id == str(expected_path)
    # The bound host should be derived from the URL
    assert session.bound_host == "example.com"


def test_named_session_path_and_id(tmp_path: Path):
    """Named sessions should be stored under a directory derived from the host."""
    env = Environment()
    config_dir = tmp_path
    session_name = "my-session"
    host = "api.test.com"
    url = "https://api.test.com/resource"

    session = get_httpie_session(
        env=env,
        config_dir=config_dir,
        session_name=session_name,
        host=host,
        url=url,
    )

    # The directory name should be derived from the host and session name
    expected_dir = session_hostname_to_dirname(host, session_name)
    expected_path = config_dir / expected_dir
    assert session.path == expected_path
    # The session_id should be the session name
    assert session.session_id == session_name
    # The bound host should be the host without port
    assert session.bound_host == host


def test_unix_socket_url_fallback(tmp_path: Path):
    """When the URL has no hostname, the bound host should default to 'localhost'."""
    env = Environment()
    config_dir = tmp_path
    session_name = "unix-session"
    url = "unix:///tmp/socket"

    session = get_httpie_session(
        env=env,
        config_dir=config_dir,
        session_name=session_name,
        host=None,
        url=url,
    )

    # Since the URL has no hostname, bound_host should be 'localhost'
    assert session.bound_host == "localhost"
    # The session path should still be under the config directory
    assert session.path.parent == config_dir
    # The session_id should be the session name
    assert session.session_id == session_name
