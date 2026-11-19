import pytest
from sanic.headers import parse_forwarded
from sanic.exceptions import InvalidHeader

class DummyConfig:
    def __init__(self, secret: str | None = None):
        self.FORWARDED_SECRET = secret

class DummyHeaders:
    def __init__(self, values):
        self._values = values
    def getall(self, name, default=None):
        return self._values.get(name.lower(), default)

def test_parse_forwarded_success():
    # Header contains the secret and a by value
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60;by=203.0.113.43;secret=abc123',
            'for=198.51.100.17;by=203.0.113.44;secret=abc123'
        ]
    })
    config = DummyConfig(secret="abc123")
    result = parse_forwarded(headers, config)
    # Expect a dict with the last matching element (rightmost) normalized
    assert isinstance(result, dict)
    assert result["by"] == "203.0.113.44"
    assert result["secret"] == "abc123"
    assert result["for"] == "198.51.100.17"

def test_parse_forwarded_multiple_headers_joined():
    # Two separate header lines, secret appears only in the second
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60;by=203.0.113.43',
            'for=198.51.100.17;by=203.0.113.44;secret=xyz'
        ]
    })
    config = DummyConfig(secret="xyz")
    result = parse_forwarded(headers, config)
    assert result["by"] == "203.0.113.44"
    assert result["secret"] == "xyz"
    assert result["for"] == "198.51.100.17"

def test_parse_forwarded_no_secret_returns_none():
    # Header present but secret does not match
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60;by=203.0.113.43;secret=wrong'
        ]
    })
    config = DummyConfig(secret="abc123")
    assert parse_forwarded(headers, config) is None
