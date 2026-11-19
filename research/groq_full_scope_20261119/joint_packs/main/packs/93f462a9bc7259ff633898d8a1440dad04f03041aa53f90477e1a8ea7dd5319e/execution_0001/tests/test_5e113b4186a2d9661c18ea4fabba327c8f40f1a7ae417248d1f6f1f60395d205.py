import pytest
from httpie.utils import parse_content_type_header

def test_parse_content_type_header_basic():
    header = "application/json; charset=utf-8; version=1.0"
    content_type, params = parse_content_type_header(header)
    assert content_type == "application/json"
    assert params == {"charset": "utf-8", "version": "1.0"}

def test_parse_content_type_header_no_params():
    header = "text/plain"
    content_type, params = parse_content_type_header(header)
    assert content_type == "text/plain"
    assert params == {}

def test_parse_content_type_header_whitespace_and_quotes():
    header = "  multipart/form-data ; boundary=\"abc123\" ;   charset = 'utf-8'  "
    content_type, params = parse_content_type_header(header)
    assert content_type == "multipart/form-data"
    assert params == {"boundary": "abc123", "charset": "utf-8"}
