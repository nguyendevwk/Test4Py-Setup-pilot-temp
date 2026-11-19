import pytest
from sanic.headers import parse_host

def test_parse_host_normal_and_lowercase():
    """Normal host with port should return lowercased hostname and int port."""
    host, port = parse_host("Example.COM:8080")
    assert host == "example.com"
    assert port == 8080

def test_parse_host_no_port_and_boundary():
    """Host without port should return None for port; test boundary port 65535."""
    host, port = parse_host("localhost")
    assert host == "localhost"
    assert port is None

    host, port = parse_host("127.0.0.1:65535")
    assert host == "127.0.0.1"
    assert port == 65535

def test_parse_host_invalid_inputs():
    """Invalid host strings should return (None, None)."""
    for bad in ["", ":", "host:", ":80", "host:abc", "host:70000", "host:80:extra"]:
        host, port = parse_host(bad)
        assert host is None
        assert port is None
