import pytest
from sanic.headers import parse_forwarded

class DummyHeaders:
    def __init__(self, values):
        self._values = values

    def getall(self, key, default=None):
        return self._values.get(key.lower(), default)

class DummyConfig:
    def __init__(self, secret):
        self.FORWARDED_SECRET = secret

def test_parse_forwarded_success(tmp_path):
    # Header contains the secret and a by value
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60;by=203.0.113.43;secret=supersecret',
            'for=198.51.100.17;by=203.0.113.44;secret=supersecret'
        ]
    })
    config = DummyConfig(secret="supersecret")
    result = parse_forwarded(headers, config)
    # The function returns a dict-like object; check key/value pairs
    assert isinstance(result, dict)
    # The first element should be the leftmost occurrence
    assert result["by"] == "203.0.113.43"
    assert result["for"] == "192.0.2.60"
    assert result["secret"] == "supersecret"

def test_parse_forwarded_no_secret(tmp_path):
    # Header present but secret does not match
    headers = DummyHeaders({
        "forwarded": ["for=192.0.2.60;by=203.0.113.43;secret=wrong"]
    })
    config = DummyConfig(secret="supersecret")
    result = parse_forwarded(headers, config)
    assert result is None

def test_parse_forwarded_missing_header(tmp_path):
    # No Forwarded header at all
    headers = DummyHeaders({})
    config = DummyConfig(secret="supersecret")
    result = parse_forwarded(headers, config)
    assert result is None
