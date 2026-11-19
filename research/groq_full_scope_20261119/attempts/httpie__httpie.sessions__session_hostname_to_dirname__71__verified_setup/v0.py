import os
import pytest
from httpie.sessions import session_hostname_to_dirname

# Test 1: Normal hostname and session name
def test_session_hostname_to_dirname_basic(tmp_path):
    # Use a simple hostname and session name
    hostname = "example.com"
    session_name = "my_session"
    result = session_hostname_to_dirname(hostname, session_name)
    expected = os.path.join("SESSIONS_DIR_NAME", hostname, f"{session_name}.json")
    assert result == expected, f"Expected {expected!r}, got {result!r}"

# Test 2: Hostname containing a port and IPv6 style address
def test_session_hostname_to_dirname_with_port_and_ipv6(tmp_path):
    # Hostname with port
    hostname_port = "localhost:8080"
    session_name_port = "port_session"
    result_port = session_hostname_to_dirname(hostname_port, session_name_port)
    expected_port = os.path.join("SESSIONS_DIR_NAME", "localhost_8080", f"{session_name_port}.json")
    assert result_port == expected_port, f"Expected {expected_port!r}, got {result_port!r}"

    # IPv6 address (colons replaced)
    hostname_ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    session_name_ipv6 = "ipv6_session"
    result_ipv6 = session_hostname_to_dirname(hostname_ipv6, session_name_ipv6)
    expected_ipv6 = os.path.join(
        "SESSIONS_DIR_NAME",
        "2001_0db8_85a3_0000_0000_8a2e_0370_7334",
        f"{session_name_ipv6}.json"
    )
    assert result_ipv6 == expected_ipv6, f"Expected {expected_ipv6!r}, got {result_ipv6!r}"

# Test 3: Error behavior when hostname is not a string
def test_session_hostname_to_dirname_invalid_hostname():
    # Passing an integer should raise AttributeError because int has no replace method
    with pytest.raises(AttributeError):
        session_hostname_to_dirname(12345, "session")
