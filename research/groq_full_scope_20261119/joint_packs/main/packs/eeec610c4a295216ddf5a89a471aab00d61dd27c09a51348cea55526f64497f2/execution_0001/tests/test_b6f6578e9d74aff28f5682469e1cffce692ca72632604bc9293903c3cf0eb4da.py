import pytest
from sanic.headers import parse_host
from sanic.exceptions import InvalidHeader

def test_parse_host_normal():
    """Normal host with port should return lowercased hostname and int port."""
    host, port = parse_host("Example.COM:8080")
    assert host == "example.com"
    assert port == 8080

def test_parse_host_no_port():
    """Host without port should return hostname and None for port."""
    host, port = parse_host("localhost")
    assert host == "localhost"
    assert port is None

def test_parse_host_invalid():
    """Invalid host string should return (None, None)."""
    host, port = parse_host("invalid host string")
    assert host is None
    assert port is None
