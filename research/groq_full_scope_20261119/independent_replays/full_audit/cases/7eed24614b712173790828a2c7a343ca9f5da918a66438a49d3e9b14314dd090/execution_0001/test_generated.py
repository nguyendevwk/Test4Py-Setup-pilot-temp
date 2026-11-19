import os
import pytest
from httpie.sessions import session_hostname_to_dirname, SESSIONS_DIR_NAME

def test_simple_hostname_and_session_name():
    """Verify that a plain hostname and session name produce the expected path."""
    hostname = "example.com"
    session_name = "my_session"
    expected = os.path.join(SESSIONS_DIR_NAME, hostname, f"{session_name}.json")
    result = session_hostname_to_dirname(hostname, session_name)
    assert result == expected, f"Expected {expected!r}, got {result!r}"

def test_hostname_with_port_replaces_colon():
    """Ensure that a colon in the hostname is replaced with an underscore."""
    hostname = "localhost:8080"
    session_name = "test"
    expected_hostname = "localhost_8080"
    expected = os.path.join(SESSIONS_DIR_NAME, expected_hostname, f"{session_name}.json")
    result = session_hostname_to_dirname(hostname, session_name)
    assert result == expected, f"Expected {expected!r}, got {result!r}"
    # The original hostname should remain unchanged
    assert hostname == "localhost:8080"

def test_empty_session_name_and_hostname():
    """Check behavior when empty strings are provided for both parameters."""
    hostname = ""
    session_name = ""
    expected = os.path.join(SESSIONS_DIR_NAME, "", f"{session_name}.json")
    result = session_hostname_to_dirname(hostname, session_name)
    assert result == expected, f"Expected {expected!r}, got {result!r}"
    # The function should not raise an exception for empty inputs
    assert isinstance(result, str)
