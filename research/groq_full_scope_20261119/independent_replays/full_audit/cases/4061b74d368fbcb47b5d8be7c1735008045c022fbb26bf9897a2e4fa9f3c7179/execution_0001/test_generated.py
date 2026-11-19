import pytest
from httpie.utils import parse_content_type_header

def test_parse_content_type_with_params():
    header = 'application/json; charset=utf-8; version=1.0'
    content_type, params = parse_content_type_header(header)
    assert content_type == 'application/json'
    assert params == {'charset': 'utf-8', 'version': '1.0'}

def test_parse_content_type_without_params():
    header = 'text/plain'
    content_type, params = parse_content_type_header(header)
    assert content_type == 'text/plain'
    assert params == {}

def test_parse_content_type_with_complex_value():
    header = 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW; charset="utf-8"'
    content_type, params = parse_content_type_header(header)
    assert content_type == 'multipart/form-data'
    assert params == {
        'boundary': '----WebKitFormBoundary7MA4YWxkTrZu0gW',
        'charset': 'utf-8'
    }
