import pytest
from sanic.headers import parse_forwarded

class DummyHeaders:
    def __init__(self, values):
        self._values = values

    def getall(self, name, default=None):
        return self._values.get(name.lower(), default)

class DummyConfig:
    def __init__(self, secret):
        self.FORWARDED_SECRET = secret

def test_parse_forwarded_success():
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60;by=203.0.113.43;secret=abcd',
            'for=198.51.100.17;by=203.0.113.44;secret=abcd'
        ]
    })
    config = DummyConfig(secret="abcd")
    result = parse_forwarded(headers, config)
    assert isinstance(result, dict)
    # The first matching element (rightmost) should be returned
    assert result["for"] == "198.51.100.17"
    assert result["by"] == "203.0.113.44"
    assert result["secret"] == "abcd"

def test_parse_forwarded_no_secret():
    headers = DummyHeaders({
        "forwarded": ["for=192.0.2.60;by=203.0.113.43"]
    })
    config = DummyConfig(secret="abcd")
    assert parse_forwarded(headers, config) is None

def test_parse_forwarded_multiple_lines_and_quotes():
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60;by=203.0.113.43;secret="abcd"',
            'for=198.51.100.17;by=203.0.113.44;secret=abcd'
        ]
    })
    config = DummyConfig(secret="abcd")
    result = parse_forwarded(headers, config)
    assert result["for"] == "198.51.100.17"
    assert result["by"] == "203.0.113.44"
    assert result["secret"] == "abcd"
