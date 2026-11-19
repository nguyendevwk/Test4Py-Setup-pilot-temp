import pytest
from sanic.headers import parse_host

def test_parse_host_valid_with_port():
    """Normal case: host with explicit port."""
    host, port = parse_host("Example.COM:8080")
    assert host == "example.com"
    assert port == 8080

def test_parse_host_valid_without_port():
    """Boundary case: host without port."""
    host, port = parse_host("localhost")
    assert host == "localhost"
    assert port is None

def test_parse_host_invalid_input():
    """Error case: malformed host string returns (None, None)."""
    host, port = parse_host("invalid_host:port")
    assert host is None
    assert port is None
