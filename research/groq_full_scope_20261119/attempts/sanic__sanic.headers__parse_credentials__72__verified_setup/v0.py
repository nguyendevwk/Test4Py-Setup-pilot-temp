import pytest
from sanic.headers import parse_credentials

def test_parse_basic_credentials(tmp_path):
    header = "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    prefix, credentials = parse_credentials(header)
    assert prefix == "Basic"
    assert credentials == "QWxhZGRpbjpvcGVuIHNlc2FtZQ=="

def test_parse_with_custom_prefixes(tmp_path):
    header = "Token abcdef123456"
    custom_prefixes = ("Token", "Bearer")
    prefix, credentials = parse_credentials(header, prefixes=custom_prefixes)
    assert prefix == "Token"
    assert credentials == "abcdef123456"

def test_parse_none_header_returns_none_and_none(tmp_path):
    header = None
    prefix, credentials = parse_credentials(header)
    assert prefix is None
    assert credentials is None
