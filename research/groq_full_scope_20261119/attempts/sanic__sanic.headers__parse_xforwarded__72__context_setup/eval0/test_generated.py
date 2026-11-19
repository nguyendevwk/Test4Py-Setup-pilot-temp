import pytest
from sanic.headers import parse_xforwarded, fwd_normalize_address

# Minimal headers mock that mimics sanic's Headers API
class DummyHeaders:
    def __init__(self, mapping):
        self._mapping = mapping

    def getone(self, key, default=None):
        return self._mapping.get(key, default)

    def getall(self, key):
        # Return a list of values for the header key
        return self._mapping.get(key, [])

# Dummy config with required attributes
class DummyConfig:
    def __init__(self, real_ip_header=None, forwarded_for_header="X-Forwarded-For",
                 proxies_count=0):
        self.REAL_IP_HEADER = real_ip_header
        self.FORWARDED_FOR_HEADER = forwarded_for_header
        self.PROXIES_COUNT = proxies_count

def test_parse_xforwarded_with_real_ip_header():
    """When REAL_IP_HEADER is present, it should be used and other headers ignored."""
    headers = DummyHeaders({
        "X-Real-IP": "192.0.2.1",
        "X-Forwarded-Proto": "HTTPS",
        "X-Forwarded-Host": "example.com",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Path": "/path",
    })
    config = DummyConfig(real_ip_header="X-Real-IP")
    result = parse_xforwarded(headers, config)
    assert result == {
        "for": "192.0.2.1",
        "proto": "https",
        "host": "example.com",
        "port": 443,
        "path": "/path",
    }

def test_parse_xforwarded_with_proxies_count_and_multiple_headers():
    """When no REAL_IP_HEADER, proxies_count selects the correct address from multiple X-Forwarded-For entries."""
    headers = DummyHeaders({
        "X-Forwarded-For": ["203.0.113.1, 203.0.113.2", "203.0.113.3"],
        "X-Forwarded-Proto": "http",
    })
    config = DummyConfig(forwarded_for_header="X-Forwarded-For", proxies_count=2)
    result = parse_xforwarded(headers, config)
    # The second-to-last address (index -2) should be used: 203.0.113.2
    assert result == {
        "for": "203.0.113.2",
        "proto": "http",
    }

def test_parse_xforwarded_invalid_port_is_ignored():
    """If the port header cannot be converted to int, it should be omitted from the result."""
    headers = DummyHeaders({
        "X-Real-IP": "198.51.100.5",
        "X-Forwarded-Port": "not-a-number",
    })
    config = DummyConfig(real_ip_header="X-Real-IP")
    result = parse_xforwarded(headers, config)
    # Port should not appear because conversion fails
    assert result == {"for": "198.51.100.5"}
