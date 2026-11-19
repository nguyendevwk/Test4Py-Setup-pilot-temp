import pytest
from sanic.headers import parse_xforwarded, fwd_normalize_address, fwd_normalize

# Simple headers mock that mimics Sanic's Headers API
class DummyHeaders:
    def __init__(self, mapping):
        self._mapping = mapping

    def getone(self, key, default=None):
        return self._mapping.get(key, default)

    def getall(self, key):
        if key not in self._mapping:
            raise KeyError(key)
        value = self._mapping[key]
        if isinstance(value, list):
            return value
        return [value]

# Dummy config with required attributes
class DummyConfig:
    def __init__(self, real_ip_header=None, forwarded_for_header="X-Forwarded-For",
                 proxies_count=0):
        self.REAL_IP_HEADER = real_ip_header
        self.FORWARDED_FOR_HEADER = forwarded_for_header
        self.PROXIES_COUNT = proxies_count

def test_parse_xforwarded_with_real_ip_header():
    """When REAL_IP_HEADER is present, it should be used directly."""
    headers = DummyHeaders({
        "X-Real-IP": "192.0.2.1",
        "X-Forwarded-Proto": "https",
        "X-Forwarded-Host": "example.com",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Path": "/path%20with%20spaces"
    })
    config = DummyConfig(real_ip_header="X-Real-IP")
    result = parse_xforwarded(headers, config)
    assert result == {
        "for": "192.0.2.1",
        "proto": "https",
        "host": "example.com",
        "port": 443,
        "path": "/path with spaces"
    }

def test_parse_xforwarded_with_proxies_count():
    """When no real IP header, proxies_count should pick the correct address."""
    headers = DummyHeaders({
        "X-Forwarded-For": ["203.0.113.1, 198.51.100.2", "192.0.2.3"],
        "X-Forwarded-Proto": "http",
        "X-Forwarded-Host": "example.org",
        "X-Forwarded-Port": "80",
        "X-Forwarded-Path": "/foo"
    })
    config = DummyConfig(proxies_count=2)  # pick the second last address
    result = parse_xforwarded(headers, config)
    assert result == {
        "for": "198.51.100.2",
        "proto": "http",
        "host": "example.org",
        "port": 80,
        "path": "/foo"
    }

def test_parse_xforwarded_invalid_port_and_unknown_address():
    """Invalid port should be omitted; 'unknown' address should raise ValueError and be omitted."""
    headers = DummyHeaders({
        "X-Forwarded-For": "unknown",
        "X-Forwarded-Proto": "HTTPS",
        "X-Forwarded-Host": "EXAMPLE.NET",
        "X-Forwarded-Port": "not-a-number",
        "X-Forwarded-Path": "/bar"
    })
    config = DummyConfig()
    result = parse_xforwarded(headers, config)
    # 'for' should be omitted because 'unknown' triggers ValueError
    # 'port' should be omitted due to ValueError on int conversion
    assert result == {
        "proto": "https",
        "host": "example.net",
        "path": "/bar"
    }
