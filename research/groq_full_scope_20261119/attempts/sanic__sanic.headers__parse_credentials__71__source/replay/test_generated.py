import pytest
from sanic.headers import parse_credentials

def test_parse_credentials_with_known_prefixes():
    """Header contains a known prefix; should return the prefix and the stripped credentials."""
    header = "Bearer abc123"
    prefix, credentials = parse_credentials(header)
    assert prefix == "Bearer"
    assert credentials == "abc123"

def test_parse_credentials_without_prefixes_returns_none_and_header():
    """Header does not contain any known prefix; should return None and the original header."""
    header = "Some random header value"
    prefix, credentials = parse_credentials(header)
    assert prefix is None
    assert credentials == header

def test_parse_credentials_with_custom_prefixes_and_none_header():
    """When a custom prefix set is provided and header is None, the function should return (None, None)."""
    header = None
    custom_prefixes = {"Custom", "Token"}
    prefix, credentials = parse_credentials(header, prefixes=custom_prefixes)
    assert prefix is None
    assert credentials is None
