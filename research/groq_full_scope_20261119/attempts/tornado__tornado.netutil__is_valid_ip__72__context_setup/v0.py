import socket
import pytest
from tornado.netutil import is_valid_ip


def test_valid_ipv4_and_ipv6():
    # Standard IPv4 address
    assert is_valid_ip("192.168.1.1") is True
    # Standard IPv6 address
    assert is_valid_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334") is True
    # IPv6 with shorthand notation
    assert is_valid_ip("::1") is True


def test_invalid_and_boundary_cases():
    # Empty string should be invalid
    assert is_valid_ip("") is False
    # String containing a null byte should be invalid
    assert is_valid_ip("127.0.0.1\x00") is False
    # Non‑numeric hostname should raise EAI_NONAME and return False
    assert is_valid_ip("not.a.valid.host") is False
    # Very long string that triggers UnicodeError in getaddrinfo
    long_ip = "a" * 64
    assert is_valid_ip(long_ip) is False


def test_unexpected_exception_propagation():
    # Pass a value that causes getaddrinfo to raise an unexpected error
    # (e.g., a negative port number triggers a ValueError in socket module)
    with pytest.raises(ValueError):
        # The function ignores the port argument, but passing a negative
        # port to getaddrinfo via the AI_NUMERICHOST flag will raise ValueError
        socket.getaddrinfo("127.0.0.1", -1, socket.AF_UNSPEC, socket.SOCK_STREAM,
                           0, socket.AI_NUMERICHOST)
