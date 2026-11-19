import pytest
from httpie.utils import parse_content_type_header

def test_parse_content_type_with_multiple_params():
    header = 'application/json; charset=utf-8; boundary="abc123"; version=1.0'
    content_type, params = parse_content_type_header(header)
    assert content_type == 'application/json'
    assert params == {
        'charset': 'utf-8',
        'boundary': 'abc123',
        'version': '1.0'
    }

def test_parse_content_type_without_params():
    header = 'text/plain'
    content_type, params = parse_content_type_header(header)
    assert content_type == 'text/plain'
    assert params == {}

def test_parse_content_type_with_malformed_param():
    header = 'image/png; invalidparam'
    content_type, params = parse_content_type_header(header)
    assert content_type == 'image/png'
    assert params == {'invalidparam': True}
