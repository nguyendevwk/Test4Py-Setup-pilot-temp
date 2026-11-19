import pytest
from sanic.headers import parse_forwarded
from sanic.exceptions import InvalidHeader

class DummyConfig:
    def __init__(self, secret: str | None = None):
        self.FORWARDED_SECRET = secret

def test_parse_forwarded_success(tmp_path):
    # Create a headers dict with a Forwarded header containing the secret
    headers = {"forwarded": ["for=192.0.2.60;by=203.0.113.43;secret=abc123"]}
    config = DummyConfig(secret="abc123")
    result = parse_forwarded(headers, config)
    assert isinstance(result, dict)
    # The returned dict should contain the key/value pairs in order
    assert result == {"for": "192.0.2.60", "by": "203.0.113.43", "secret": "abc123"}

def test_parse_forwarded_no_secret(tmp_path):
    # Header present but secret does not match
    headers = {"forwarded": ["for=192.0.2.60;by=203.0.113.43;secret=wrong"]}
    config = DummyConfig(secret="abc123")
    result = parse_forwarded(headers, config)
    assert result is None

def test_parse_forwarded_missing_header(tmp_path):
    # No Forwarded header at all
    headers = {}
    config = DummyConfig(secret="abc123")
    result = parse_forwarded(headers, config)
    assert result is None
