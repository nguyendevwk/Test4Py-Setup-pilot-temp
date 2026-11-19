import os
import pytest
from httpie.sessions import session_hostname_to_dirname, SESSIONS_DIR_NAME

def test_simple_hostname(tmp_path):
    # Simple hostname without port
    hostname = "example.com"
    session_name = "my_session"
    expected = os.path.join(SESSIONS_DIR_NAME, hostname, f"{session_name}.json")
    result = session_hostname_to_dirname(hostname, session_name)
    assert result == expected, f"Expected {expected!r}, got {result!r}"

def test_hostname_with_port(tmp_path):
    # Hostname with a port number
    hostname = "example.com:8080"
    session_name = "port_session"
    # colon should be replaced by underscore
    expected_hostname = "example.com_8080"
    expected = os.path.join(SESSIONS_DIR_NAME, expected_hostname, f"{session_name}.json")
    result = session_hostname_to_dirname(hostname, session_name)
    assert result == expected, f"Expected {expected!r}, got {result!r}"
    # Ensure the original hostname string is not mutated
    assert hostname == "example.com:8080"

def test_ipv6_hostname(tmp_path):
    # IPv6 address with multiple colons
    hostname = "[2001:db8::1]:443"
    session_name = "ipv6_session"
    # All colons inside brackets and port should be replaced
    expected_hostname = "[2001_db8__1]_443"
    expected = os.path.join(SESSIONS_DIR_NAME, expected_hostname, f"{session_name}.json")
    result = session_hostname_to_dirname(hostname, session_name)
    assert result == expected, f"Expected {expected!r}, got {result!r}"
