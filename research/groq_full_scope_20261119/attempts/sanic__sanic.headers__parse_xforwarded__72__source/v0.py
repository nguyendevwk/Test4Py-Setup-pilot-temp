import pytest
from sanic.headers import parse_xforwarded

class DummyHeaders:
    def __init__(self, mapping):
        self._mapping = mapping

    def getone(self, key, default=None):
        return self._mapping.get(key, default)

    def getall(self, key):
        # Return list of values for the key; if not present raise KeyError
        if key not in self._mapping:
            raise KeyError(key)
        val = self._mapping[key]
        if isinstance(val, list):
            return val
        return [val]

class DummyConfig:
    def __init__(self, real_ip_header=None, forwarded_for_header=None, proxies_count=0):
        self.REAL_IP_HEADER = real_ip_header
        self.FORWARDED_FOR_HEADER = forwarded_for_header
        self.PROXIES_COUNT = proxies_count

def test_parse_xforwarded_no_headers_returns_none():
    headers = DummyHeaders({})
    config = DummyConfig()
    assert parse_xforwarded(headers, config) is None

def test_parse_xforwarded_real_ip_header_used():
    headers = DummyHeaders({"X-Real-IP": "192.0.2.1"})
    config = DummyConfig(real_ip_header="X-Real-IP")
    result = parse_xforwarded(headers, config)
    # The result should be a string containing the address
    assert isinstance(result, str)
    assert "for=192.0.2.1" in result

def test_parse_xforwarded_forwarded_for_with_proxies_count():
    headers = DummyHeaders({
        "X-Forwarded-For": ["203.0.113.1, 198.51.100.2", "198.51.100.3"]
    })
    config = DummyConfig(forwarded_for_header="X-Forwarded-For", proxies_count=2)
    result = parse_xforwarded(headers, config)
    # The second proxy from the end should be used (198.51.100.2)
    assert isinstance(result, str)
    assert "for=198.51.100.2" in result
