import pytest
from sanic.headers import parse_forwarded, fwd_normalize_address

# Helper to mimic the headers object used by parse_forwarded
class DummyHeaders:
    def __init__(self, mapping):
        self._mapping = mapping

    def getall(self, key, default=None):
        return self._mapping.get(key.lower(), default)

# Simple config object with FORWARDED_SECRET attribute
class DummyConfig:
    def __init__(self, secret):
        self.FORWARDED_SECRET = secret

def test_parse_forwarded_normal_case():
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60;proto=http;by=203.0.113.43',
            'secret=supersecret'
        ]
    })
    config = DummyConfig(secret="supersecret")
    result = parse_forwarded(headers, config)
    assert result == {
        "for": "192.0.2.60",
        "proto": "http",
        "by": "203.0.113.43",
        "secret": "supersecret",
    }

def test_parse_forwarded_missing_secret_returns_none():
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60;proto=http;by=203.0.113.43',
            'secret=wrongsecret'
        ]
    })
    config = DummyConfig(secret="supersecret")
    assert parse_forwarded(headers, config) is None

def test_parse_forwarded_invalid_port_is_ignored():
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60;port=notanumber;proto=http;by=203.0.113.43',
            'secret=supersecret'
        ]
    })
    config = DummyConfig(secret="supersecret")
    result = parse_forwarded(headers, config)
    # port should be omitted due to ValueError
    assert result == {
        "for": "192.0.2.60",
        "proto": "http",
        "by": "203.0.113.43",
        "secret": "supersecret",
    }
    assert "port" not in result
