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
    # Non‑numeric hostname should raise an error (EAI_NONAME)
    assert is_valid_ip("not.a.valid.host") is False
    # Unicode string longer than 63 characters should be invalid
    long_unicode = "a" * 64
    assert is_valid_ip(long_unicode) is False


def test_error_propagation_for_non_numeric_host():
    # A string that is not a valid hostname or IP should raise a socket.gaierror
    # with EAI_NONAME, which is caught and converted to False by is_valid_ip.
    # We verify that no other exception types are raised.
    with pytest.raises(socket.gaierror) as excinfo:
        # Temporarily monkeypatch getaddrinfo to raise a generic gaierror
        original_getaddrinfo = socket.getaddrinfo
        try:
            socket.getaddrinfo = lambda *_, **__: (_ for _ in ()).throw(
                socket.gaierror(socket.EAI_FAIL, "generic failure")
            )
            is_valid_ip("invalid.host")
        finally:
            socket.getaddrinfo = original_getaddrinfo
    assert excinfo.value.args[0] == socket.EAI_FAIL
