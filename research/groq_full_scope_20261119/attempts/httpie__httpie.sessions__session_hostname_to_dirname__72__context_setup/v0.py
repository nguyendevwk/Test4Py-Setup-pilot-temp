import os
import pytest
from httpie.sessions import session_hostname_to_dirname, SESSIONS_DIR_NAME

def test_normal_hostname_and_session_name():
    """Verify that a simple hostname and session name produce the expected path."""
    hostname = "example.com"
    session_name = "my_session"
    expected = os.path.join(SESSIONS_DIR_NAME, hostname, f"{session_name}.json")
    result = session_hostname_to_dirname(hostname, session_name)
    assert result == expected, f"Expected {expected!r}, got {result!r}"

def test_hostname_with_port_replaces_colon():
    """Ensure that a hostname containing a colon (port) is converted correctly."""
    hostname = "localhost:8080"
    session_name = "test"
    # The colon should be replaced by an underscore
    expected_hostname = "localhost_8080"
    expected = os.path.join(SESSIONS_DIR_NAME, expected_hostname, f"{session_name}.json")
    result = session_hostname_to_dirname(hostname, session_name)
    assert result == expected, f"Expected {expected!r}, got {result!r}"
    # The original hostname should remain unchanged
    assert hostname == "localhost:8080"

def test_multiple_colons_and_empty_session_name():
    """Test that multiple colons are all replaced and an empty session name is handled."""
    hostname = "a:b:c"
    session_name = ""
    expected_hostname = "a_b_c"
    expected = os.path.join(SESSIONS_DIR_NAME, expected_hostname, f"{session_name}.json")
    result = session_hostname_to_dirname(hostname, session_name)
    assert result == expected, f"Expected {expected!r}, got {result!r}"
    # Ensure the function does not raise on empty session_name
    assert result.endswith(".json")
