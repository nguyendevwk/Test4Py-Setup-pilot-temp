import pytest
from sanic.headers import parse_xforwarded

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

class DummyConfig:
    def __init__(self, real_ip_header=None, forwarded_for_header="X-Forwarded-For",
                 proxies_count=0, **kwargs):
        self.REAL_IP_HEADER = real_ip_header
        self.FORWARDED_FOR_HEADER = forwarded_for_header
        self.PROXIES_COUNT = proxies_count
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_parse_xforwarded_with_real_ip_header():
    headers = DummyHeaders({
        "X-Real-IP": "203.0.113.195",
        "X-Forwarded-Proto": "https",
        "X-Forwarded-Host": "example.com",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Path": "/resource"
    })
    config = DummyConfig(real_ip_header="X-Real-IP")
    result = parse_xforwarded(headers, config)
    assert result is not None
    # The result should be an Options-like iterable; convert to dict for assertion
    options_dict = dict(result)
    assert options_dict["for"] == "203.0.113.195"
    assert options_dict["proto"] == "https"
    assert options_dict["host"] == "example.com"
    assert options_dict["port"] == "443"
    assert options_dict["path"] == "/resource"

def test_parse_xforwarded_with_forwarded_for_and_proxies_count():
    headers = DummyHeaders({
        "X-Forwarded-For": ["203.0.113.1, 203.0.113.2", "203.0.113.3"],
        "X-Forwarded-Proto": "http",
        "X-Forwarded-Host": "example.org",
        "X-Forwarded-Port": "80",
        "X-Forwarded-Path": "/api"
    })
    config = DummyConfig(forwarded_for_header="X-Forwarded-For", proxies_count=2)
    result = parse_xforwarded(headers, config)
    assert result is not None
    options_dict = dict(result)
    # With proxies_count=2, the second-to-last address should be used
    assert options_dict["for"] == "203.0.113.2"
    assert options_dict["proto"] == "http"
    assert options_dict["host"] == "example.org"
    assert options_dict["port"] == "80"
    assert options_dict["path"] == "/api"

def test_parse_xforwarded_returns_none_when_no_address():
    headers = DummyHeaders({
        "X-Forwarded-Proto": "https",
        "X-Forwarded-Host": "example.net"
    })
    config = DummyConfig(real_ip_header="X-Real-IP", forwarded_for_header="X-Forwarded-For", proxies_count=1)
    result = parse_xforwarded(headers, config)
    assert result is None
