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

def test_parse_forwarded_success_single_line():
    headers = DummyHeaders({"forwarded": ['by=example.com; secret="mysecret"']})
    config = DummyConfig("mysecret")
    result = parse_forwarded(headers, config)
    assert result is not None
    # The returned dict should contain the matching key/value pairs
    assert result["by"] == "example.com"
    assert result["secret"] == "mysecret"

def test_parse_forwarded_multiple_lines_and_quotes():
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60; proto=http',
            'by=proxy1; secret="mysecret"'
        ]
    })
    config = DummyConfig("mysecret")
    result = parse_forwarded(headers, config)
    assert result is not None
    # The order should be preserved from left to right
    assert list(result.keys()) == ["by", "secret"]
    assert result["by"] == "proxy1"
    assert result["secret"] == "mysecret"

def test_parse_forwarded_no_secret_returns_none():
    headers = DummyHeaders({"forwarded": ['by=example.com; secret="wrong"']})
    config = DummyConfig("mysecret")
    result = parse_forwarded(headers, config)
    assert result is None
