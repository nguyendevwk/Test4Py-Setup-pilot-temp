import pytest
from sanic.headers import parse_host

def test_parse_host_basic():
    """Normal hostname with port."""
    host, port = parse_host("example.com:8080")
    assert host == "example.com"
    assert port == 8080

def test_parse_host_ipv6():
    """IPv6 address with port."""
    host, port = parse_host("[2001:db8::1]:443")
    assert host == "[2001:db8::1]"
    assert port == 443

def test_parse_host_invalid():
    """Malformed host string returns (None, None)."""
    host, port = parse_host("invalid_host:port")
    assert host is None
    assert port is None
