import pytest
from sanic.headers import parse_forwarded, fwd_normalize_address

class DummyHeaders:
    def __init__(self, values):
        self._values = values
    def getall(self, name, default=None):
        return self._values.get(name.lower(), default)

class DummyConfig:
    def __init__(self, secret):
        self.FORWARDED_SECRET = secret

def test_parse_forwarded_normal_and_normalization():
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60;proto=https;by=203.0.113.43',
            'secret=supersecret'
        ]
    })
    config = DummyConfig(secret="supersecret")
    result = parse_forwarded(headers, config)
    assert isinstance(result, dict)
    # by and for should be lowercased addresses
    assert result["by"] == "203.0.113.43"
    assert result["for"] == "192.0.2.60"
    # proto should be lowercased
    assert result["proto"] == "https"
    # secret should be omitted from the result
    assert "secret" not in result

def test_parse_forwarded_invalid_port_omitted():
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60;port=notanumber;secret=supersecret'
        ]
    })
    config = DummyConfig(secret="supersecret")
    result = parse_forwarded(headers, config)
    assert isinstance(result, dict)
    assert result["for"] == "192.0.2.60"
    # invalid port should be omitted
    assert "port" not in result

def test_parse_forwarded_no_secret_returns_none():
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60;proto=https;by=203.0.113.43'
        ]
    })
    config = DummyConfig(secret="supersecret")
    result = parse_forwarded(headers, config)
    assert result is None
