import pytest
from sanic.headers import parse_forwarded

class DummyHeaders:
    def __init__(self, mapping):
        self._mapping = mapping

    def getall(self, key, default=None):
        return self._mapping.get(key.lower(), default)

class DummyConfig:
    def __init__(self, secret):
        self.FORWARDED_SECRET = secret

def test_parse_forwarded_success():
    # Header contains the secret and a by value
    headers = DummyHeaders({
        "forwarded": ['for=192.0.2.60;by=203.0.113.43;secret=abc123']
    })
    config = DummyConfig(secret="abc123")
    result = parse_forwarded(headers, config)
    assert result is not None
    # The returned dict should contain the by and secret keys with correct values
    assert result["by"] == "203.0.113.43"
    assert result["secret"] == "abc123"
    # The 'for' key should also be present
    assert result["for"] == "192.0.2.60"

def test_parse_forwarded_missing_secret():
    # Header does not contain the secret, should return None
    headers = DummyHeaders({
        "forwarded": ['for=192.0.2.60;by=203.0.113.43']
    })
    config = DummyConfig(secret="abc123")
    result = parse_forwarded(headers, config)
    assert result is None

def test_parse_forwarded_multiple_lines_and_quotes():
    # Multiple header lines, secret appears in the second line, quoted value
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60;by=203.0.113.43',
            'secret="abc123";by="203.0.113.44"'
        ]
    })
    config = DummyConfig(secret="abc123")
    result = parse_forwarded(headers, config)
    assert result is not None
    # The returned dict should reflect the second line's values
    assert result["by"] == "203.0.113.44"
    assert result["secret"] == "abc123"
