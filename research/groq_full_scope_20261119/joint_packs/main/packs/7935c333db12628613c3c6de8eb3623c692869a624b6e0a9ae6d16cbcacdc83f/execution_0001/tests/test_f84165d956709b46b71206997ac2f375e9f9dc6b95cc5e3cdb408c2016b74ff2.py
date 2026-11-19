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


def test_invalid_and_boundary_inputs():
    # Empty string should be invalid
    assert is_valid_ip("") is False
    # String containing a null byte should be invalid
    assert is_valid_ip("127.0.0.1\x00") is False
    # Non‑numeric hostname should raise EAI_NONAME and be considered invalid
    assert is_valid_ip("not.a.valid.host") is False


def test_long_unicode_input():
    # Input longer than 63 characters triggers UnicodeError in getaddrinfo
    long_ip = "a" * 64
    assert is_valid_ip(long_ip) is False
