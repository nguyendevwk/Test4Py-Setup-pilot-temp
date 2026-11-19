import pytest
from sanic.headers import parse_forwarded, fwd_normalize, fwd_normalize_address

class DummyHeaders:
    def __init__(self, values):
        self._values = values
    def getall(self, name, default=None):
        return self._values.get(name.lower(), default)

class DummyConfig:
    def __init__(self, secret):
        self.FORWARDED_SECRET = secret

def test_parse_forwarded_normal():
    # Header contains the secret and several parameters
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60;proto=http;by=203.0.113.43;secret=abc123',
            'for=2001:db8::1;proto=https;by=2001:db8::2;secret=abc123'
        ]
    })
    config = DummyConfig(secret="abc123")
    result = parse_forwarded(headers, config)
    # The function should return the first matching element (rightmost)
    assert result == {
        "for": "2001:db8::1",
        "proto": "https",
        "by": "2001:db8::2",
        "secret": "abc123"
    }

def test_parse_forwarded_missing_secret():
    # Header does not contain the secret, should return None
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60;proto=http;by=203.0.113.43'
        ]
    })
    config = DummyConfig(secret="abc123")
    assert parse_forwarded(headers, config) is None

def test_fwd_normalize_address_invalid():
    # Address "unknown" should raise ValueError and be omitted
    with pytest.raises(ValueError):
        fwd_normalize_address("unknown")
    # IPv6 address should be bracketed and lowercased
    assert fwd_normalize_address("2001:DB8::1") == "[2001:db8::1]"
    # Obfuscated string starting with underscore should not be lowercased
    assert fwd_normalize_address("_ObFuscAtEd") == "_ObFuscAtEd"
