import os
import pytest
from httpie.sessions import session_hostname_to_dirname, SESSIONS_DIR_NAME


def test_session_hostname_to_dirname_normal_hostname(tmp_path):
    """Test that a simple hostname is converted correctly."""
    hostname = "example.com"
    session_name = "my_session"
    expected = os.path.join(SESSIONS_DIR_NAME, hostname, f"{session_name}.json")
    result = session_hostname_to_dirname(hostname, session_name)
    assert result == expected, f"Expected {expected!r}, got {result!r}"


def test_session_hostname_to_dirname_with_port_and_ipv6(tmp_path):
    """Test that hostnames containing ':' are replaced with '_' and IPv6 addresses are handled."""
    # IPv4 with port
    hostname_ipv4 = "localhost:8080"
    session_name_ipv4 = "ipv4_session"
    expected_ipv4 = os.path.join(SESSIONS_DIR_NAME, "localhost_8080", f"{session_name_ipv4}.json")
    result_ipv4 = session_hostname_to_dirname(hostname_ipv4, session_name_ipv4)
    assert result_ipv4 == expected_ipv4, f"IPv4: Expected {expected_ipv4!r}, got {result_ipv4!r}"

    # IPv6 address
    hostname_ipv6 = "[2001:db8::1]"
    session_name_ipv6 = "ipv6_session"
    # The brackets and colons should all be replaced
    expected_ipv6 = os.path.join(SESSIONS_DIR_NAME, "[2001_db8__1]", f"{session_name_ipv6}.json")
    result_ipv6 = session_hostname_to_dirname(hostname_ipv6, session_name_ipv6)
    assert result_ipv6 == expected_ipv6, f"IPv6: Expected {expected_ipv6!r}, got {result_ipv6!r}"


def test_session_hostname_to_dirname_invalid_input():
    """Test that passing a non-string hostname raises an AttributeError."""
    with pytest.raises(AttributeError):
        session_hostname_to_dirname(None, "session")
