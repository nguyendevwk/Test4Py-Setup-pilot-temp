import pytest
from httpie.utils import parse_content_type_header

def test_parse_simple_content_type():
    header = "application/json"
    content_type, params = parse_content_type_header(header)
    assert content_type == "application/json"
    assert params == {}

def test_parse_with_multiple_params():
    header = "text/html; charset=UTF-8; boundary=\"abc123\";   version=1.0"
    content_type, params = parse_content_type_header(header)
    assert content_type == "text/html"
    assert params == {
        "charset": "UTF-8",
        "boundary": "abc123",
        "version": "1.0",
    }

def test_parse_with_unusual_whitespace_and_quotes():
    header = "  multipart/form-data ;  boundary = 'xyz' ;   charset = \"utf-8\"  "
    content_type, params = parse_content_type_header(header)
    assert content_type == "multipart/form-data"
    assert params == {
        "boundary": "xyz",
        "charset": "utf-8",
    }
