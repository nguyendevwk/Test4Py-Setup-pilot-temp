import pytest
from sanic.headers import parse_host

def test_parse_host_valid_ipv4_and_port():
    # Normal case: IPv4 address with port
    host, port = parse_host("192.168.1.1:8080")
    assert host == "192.168.1.1"
    assert port == 8080

def test_parse_host_boundary_ipv6_no_port_and_case_insensitivity():
    # Boundary case: IPv6 address without port and mixed case
    host, port = parse_host("[2001:0db8:85a3:0000:0000:8a2e:0370:7334]")
    assert host == "[2001:0db8:85a3:0000:0000:8a2e:0370:7334]"
    assert port is None

def test_parse_host_invalid_format_returns_none():
    # Error case: invalid host string
    host, port = parse_host("invalid_host:port")
    assert host is None
    assert port is None
