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
    # The returned dict should contain the key 'by' with the correct value
    assert result.get("by") == "example.com"
    # The secret key should also be present
    assert result.get("secret") == "mysecret"

def test_parse_forwarded_multiple_lines_and_quotes():
    headers = DummyHeaders({
        "forwarded": [
            'for=192.0.2.60; proto=https',
            'by=proxy1.example.com; secret="mysecret"',
            'by=proxy2.example.com; secret="mysecret"'
        ]
    })
    config = DummyConfig("mysecret")
    result = parse_forwarded(headers, config)
    assert result is not None
    # The first matching element from the right should be returned
    # Since the rightmost line contains the secret, its 'by' should be returned
    assert result.get("by") == "proxy2.example.com"
    # The 'secret' key should also be present
    assert result.get("secret") == "mysecret"

def test_parse_forwarded_no_secret_returns_none():
    headers = DummyHeaders({"forwarded": ['by=example.com; secret="wrong"']})
    config = DummyConfig("mysecret")
    result = parse_forwarded(headers, config)
    assert result is None
