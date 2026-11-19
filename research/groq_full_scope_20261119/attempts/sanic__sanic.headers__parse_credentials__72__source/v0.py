import pytest
from sanic.headers import parse_credentials

def test_parse_credentials_basic_prefix():
    header = "Basic abcdef123456"
    prefix, cred = parse_credentials(header)
    assert prefix == "Basic"
    assert cred == "abcdef123456"

def test_parse_credentials_no_prefix_returns_header():
    header = "SomeOtherHeader value"
    prefix, cred = parse_credentials(header, prefixes=("Custom",))
    assert prefix is None
    assert cred == header

def test_parse_credentials_none_header_returns_none_and_none():
    prefix, cred = parse_credentials(None)
    assert prefix is None
    assert cred is None
