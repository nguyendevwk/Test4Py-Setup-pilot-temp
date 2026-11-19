import pytest
from sanic.headers import parse_credentials

def test_parse_basic_header():
    header = "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    prefix, credentials = parse_credentials(header)
    assert prefix == "Basic"
    assert credentials == "QWxhZGRpbjpvcGVuIHNlc2FtZQ=="

def test_parse_with_custom_prefixes_and_no_match():
    header = "CustomAuth abcdefg"
    # Provide a custom set of prefixes that does not include 'CustomAuth'
    prefix, credentials = parse_credentials(header, prefixes={"Bearer", "Token"})
    # Since no prefix matches, the function should return None and the original header
    assert prefix is None
    assert credentials == header

def test_parse_none_header_returns_none_and_none():
    # When header is None, the function should return (None, None)
    prefix, credentials = parse_credentials(None)
    assert prefix is None
    assert credentials is None
