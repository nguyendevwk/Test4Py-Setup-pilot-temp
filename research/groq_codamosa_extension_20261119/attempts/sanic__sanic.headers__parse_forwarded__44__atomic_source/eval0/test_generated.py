import pytest
from sanic.headers import parse_forwarded
from types import SimpleNamespace

# Helper config object with FORWARDED_SECRET attribute
def make_config(secret: str | None):
    return SimpleNamespace(FORWARDED_SECRET=secret)

# Test that a correctly formatted header containing the secret returns the expected options
def test_parse_forwarded_success():
    headers = {
        "forwarded": [
            'for=192.0.2.43;proto=http;by=203.0.113.43;secret=abcd',
            'for=198.51.100.17;proto=https;by=203.0.113.44;secret=abcd'
        ]
    }
    config = make_config("abcd")
    result = parse_forwarded(headers, config)
    # The function returns a dict-like mapping; check key order and values
    assert isinstance(result, dict)
    # The last element containing the secret should be returned
    assert result["by"] == "203.0.113.44"
    assert result["proto"] == "https"
    assert result["for"] == "198.51.100.17"
    assert result["secret"] == "abcd"

# Test that when the secret is missing the function returns None
def test_parse_forwarded_no_secret():
    headers = {
        "forwarded": [
            'for=192.0.2.43;proto=http;by=203.0.113.43',
            'for=198.51.100.17;proto=https;by=203.0.113.44'
        ]
    }
    config = make_config("abcd")
    assert parse_forwarded(headers, config) is None

# Test that when the header key is absent or empty the function returns None
def test_parse_forwarded_missing_header():
    headers = {}
    config = make_config("abcd")
    assert parse_forwarded(headers, config) is None
