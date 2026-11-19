import pytest
from sanic.headers import parse_content_header

def test_parse_simple_header():
    """Header without parameters should return empty options."""
    header = "application/json"
    value, options = parse_content_header(header)
    assert value == "application/json"
    assert options == {}

def test_parse_header_with_parameters_and_percent_encoding():
    """Parameters should be parsed and percent-encoded values decoded."""
    header = 'form-data; name=upload; filename="%22file.txt%22"'
    value, options = parse_content_header(header)
    assert value == "form-data"
    assert options == {"name": "upload", "filename": '"file.txt"'}
    # Ensure percent-encoded newline is decoded correctly
    header_with_newline = 'text/plain; description="Line1%0D%0ALine2"'
    _, opts = parse_content_header(header_with_newline)
    assert opts["description"] == "Line1\nLine2"

def test_parse_header_with_mixed_case_and_whitespace():
    """Header name should be lowercased and stripped; options keys lowercased."""
    header = '  TEXT/HTML  ;  Charset=ISO-8859-1 ;  Boundary = "abc123"  '
    value, options = parse_content_header(header)
    assert value == "text/html"
    assert options == {"charset": "ISO-8859-1", "boundary": "abc123"}
