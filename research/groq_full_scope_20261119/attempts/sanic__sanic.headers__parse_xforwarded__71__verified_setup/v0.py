import pytest
from sanic.headers import parse_xforwarded

# Helper to mimic Sanic's Headers interface
class DummyHeaders:
    def __init__(self, mapping):
        self._mapping = mapping

    def getone(self, key, default=None):
        return self._mapping.get(key, default)

    def getall(self, key):
        # Return list of values for the key; empty list if missing
        return self._mapping.get(key, [])

# Simple config object with required attributes
class DummyConfig:
    def __init__(self, real_ip_header=None, forwarded_for_header=None,
                 proxies_count=0, **kwargs):
        self.REAL_IP_HEADER = real_ip_header
        self.FORWARDED_FOR_HEADER = forwarded_for_header
        self.PROXIES_COUNT = proxies_count
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_parse_xforwarded_with_real_ip_header():
    """When REAL_IP_HEADER is present, the function returns a dict containing
    the 'for' key with that address and other optional headers if provided."""
    headers = DummyHeaders({
        "X-Real-IP": "192.0.2.1",
        "X-Forwarded-Proto": "https",
        "X-Forwarded-Host": "example.com",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Path": "/path",
    })
    config = DummyConfig(real_ip_header="X-Real-IP",
                         forwarded_for_header="X-Forwarded-For",
                         proxies_count=0)
    result = parse_xforwarded(headers, config)
    assert isinstance(result, dict)
    assert result["for"] == "192.0.2.1"
    assert result["proto"] == "https"
    assert result["host"] == "example.com"
    assert result["port"] == "443"
    assert result["path"] == "/path"

def test_parse_xforwarded_with_proxies_count():
    """When no REAL_IP_HEADER but PROXIES_COUNT is set, the function uses the
    X-Forwarded-For header to determine the client IP."""
    headers = DummyHeaders({
        "X-Forwarded-For": "203.0.113.5, 198.51.100.23, 192.0.2.1",
        "X-Forwarded-Proto": "http",
    })
    config = DummyConfig(real_ip_header=None,
                         forwarded_for_header="X-Forwarded-For",
                         proxies_count=2)
    result = parse_xforwarded(headers, config)
    assert isinstance(result, dict)
    # proxies_count=2 means take the second from the end: 198.51.100.23
    assert result["for"] == "198.51.100.23"
    assert result["proto"] == "http"

def test_parse_xforwarded_missing_headers_returns_none():
    """If neither REAL_IP_HEADER nor a valid X-Forwarded-For entry is present,
    the function returns None."""
    headers = DummyHeaders({})
    config = DummyConfig(real_ip_header="X-Real-IP",
                         forwarded_for_header="X-Forwarded-For",
                         proxies_count=1)
    assert parse_xforwarded(headers, config) is None
