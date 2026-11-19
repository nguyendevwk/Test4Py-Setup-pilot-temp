import pytest
from sanic.headers import parse_content_header, Options

def test_parse_simple_header():
    """Verify that a simple header with no parameters returns the type and empty options."""
    header = "text/html"
    content_type, options = parse_content_header(header)
    assert content_type == "text/html"
    assert isinstance(options, dict)
    assert options == {}

def test_parse_header_with_parameters_and_percent_encoding():
    """Verify that parameters are parsed correctly and percent-encoded characters are decoded."""
    header = 'multipart/form-data; name=upload; filename="%22file.txt%22"; description="Line%0D%0Abreak"'
    content_type, options = parse_content_header(header)
    assert content_type == "multipart/form-data"
    # Parameters should be lowercased keys
    assert options == {
        "name": "upload",
        "filename": '"file.txt"',
        "description": "Line\nbreak",
    }

def test_parse_header_with_unquoted_and_special_characters():
    """Verify that unquoted values and special characters are handled correctly."""
    header = 'application/json; charset=utf-8; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
    content_type, options = parse_content_header(header)
    assert content_type == "application/json"
    assert options == {
        "charset": "utf-8",
        "boundary": "----WebKitFormBoundary7MA4YWxkTrZu0gW",
    }
