import socket
import pytest
from tornado.netutil import is_valid_ip

def test_valid_ipv4_and_ipv6():
    # Standard IPv4 address
    assert is_valid_ip("192.168.1.1") is True
    # Standard IPv6 address
    assert is_valid_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334") is True
    # IPv6 compressed form
    assert is_valid_ip("2001:db8::1") is True

def test_invalid_and_boundary_cases():
    # Empty string should be invalid
    assert is_valid_ip("") is False
    # String containing null byte should be invalid
    assert is_valid_ip("127.0.0.1\x00") is False
    # Non‑numeric hostname should raise EAI_NONAME and return False
    assert is_valid_ip("not.a.valid.host") is False
    # Very long string exceeding IDNA limit should be invalid
    long_ip = "a" * 64
    assert is_valid_ip(long_ip) is False

def test_error_propagation_for_unexpected_gaierror():
    # Simulate an unexpected gaierror by patching socket.getaddrinfo
    original_getaddrinfo = socket.getaddrinfo
    def fake_getaddrinfo(*args, **kwargs):
        raise socket.gaierror(socket.EAI_FAIL, "generic failure")
    socket.getaddrinfo = fake_getaddrinfo
    try:
        with pytest.raises(socket.gaierror) as excinfo:
            is_valid_ip("1.2.3.4")
        assert excinfo.value.args[0] == socket.EAI_FAIL
    finally:
        socket.getaddrinfo = original_getaddrinfo
