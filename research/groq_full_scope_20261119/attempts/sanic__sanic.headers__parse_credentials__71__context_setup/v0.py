import pytest
from sanic.headers import parse_credentials

def test_parse_credentials_with_known_prefixes():
    """Header contains a known prefix; should return the prefix and the stripped credentials."""
    header = "Bearer abc123"
    prefix, credentials = parse_credentials(header)
    assert prefix == "Bearer"
    assert credentials == "abc123"

def test_parse_credentials_with_custom_prefixes_and_no_match():
    """Custom prefixes provided but header does not contain any; should return None and original header."""
    header = "Token abc123"
    custom_prefixes = ("Basic", "Bearer")
    prefix, credentials = parse_credentials(header, prefixes=custom_prefixes)
    assert prefix is None
    assert credentials == header

def test_parse_credentials_with_invalid_prefixes_type_and_none_header():
    """When prefixes is not a list/tuple/set, defaults are used; when header is None, returns (None, None)."""
    header = None
    prefix, credentials = parse_credentials(header, prefixes="not a collection")
    assert prefix is None
    assert credentials is None
