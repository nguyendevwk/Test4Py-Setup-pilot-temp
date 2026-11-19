import pytest
from sanic.headers import parse_forwarded

class DummyConfig:
    def __init__(self, secret: str | None):
        self.FORWARDED_SECRET = secret

class DummyHeaders:
    def __init__(self, values):
        self._values = values

    def getall(self, key, default=None):
        return self._values.get(key.lower(), default)

def test_parse_forwarded_missing_header_and_secret():
    headers = DummyHeaders({})
    config = DummyConfig(secret="s3cr3t")
    # No "forwarded" header -> None
    assert parse_forwarded(headers, config) is None

    # Header present but secret empty -> None
    headers = DummyHeaders({"forwarded": ["by=unknown"]})
    config = DummyConfig(secret=None)
    assert parse_forwarded(headers, config) is None

def test_parse_forwarded_secret_not_present():
    headers = DummyHeaders({"forwarded": ["by=unknown"]})
    config = DummyConfig(secret="s3cr3t")
    # Secret not in header -> None
    assert parse_forwarded(headers, config) is None

def test_parse_forwarded_success_and_order():
    # Two header lines, secret appears in second line
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.43;proto=http',
            'by=203.0.113.43;secret=s3cr3t;host=example.com'
        ]
    })
    config = DummyConfig(secret="s3cr3t")
    result = parse_forwarded(headers, config)
    # Result should be a dict with keys in the order they appear in the matched element
    assert isinstance(result, dict)
    expected = {
        "by": "203.0.113.43",
        "secret": "s3cr3t",
        "host": "example.com"
    }
    assert result == expected
