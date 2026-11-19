import os
import pytest
from httpie.sessions import session_hostname_to_dirname, SESSIONS_DIR_NAME

def test_session_hostname_to_dirname_normal(tmp_path):
    # Normal hostname and session name
    hostname = "example.com"
    session_name = "my_session"
    result = session_hostname_to_dirname(hostname, session_name)
    expected = os.path.join(SESSIONS_DIR_NAME, hostname, f"{session_name}.json")
    assert result == expected
    # Ensure the path uses the correct separator
    assert os.path.sep in result

def test_session_hostname_to_dirname_boundary():
    # Hostname with multiple colons and session name with special chars
    hostname = "my:host:port"
    session_name = "sess!@#"
    result = session_hostname_to_dirname(hostname, session_name)
    # Colons should be replaced with underscores
    assert "my_host_port" in result
    # Session name should be preserved in the filename
    assert result.endswith("sess!@#.json")
    # Full path should be constructed correctly
    expected = os.path.join(SESSIONS_DIR_NAME, "my_host_port", "sess!@#.json")
    assert result == expected

def test_session_hostname_to_dirname_error():
    # Passing a non-string hostname should raise an AttributeError
    with pytest.raises(AttributeError):
        session_hostname_to_dirname(123, "session")
