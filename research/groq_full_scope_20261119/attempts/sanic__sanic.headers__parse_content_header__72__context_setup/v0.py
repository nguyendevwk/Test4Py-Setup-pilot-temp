import pytest
from sanic.headers import parse_content_header, Options

def test_parse_simple_header():
    """Header without parameters should return the value and empty options."""
    header = "application/json"
    value, options = parse_content_header(header)
    assert value == "application/json"
    assert options == {}

def test_parse_header_with_multiple_params_and_unescaping():
    """Header with several parameters, including percent-encoded quotes and newlines."""
    header = 'form-data; name=upload; filename="%22file%22.txt"; description="%0D%0ANew%20Line"'
    value, options = parse_content_header(header)
    assert value == "form-data"
    # Expected unescaped values
    assert options == {
        "name": "upload",
        "filename": '"file".txt',
        "description": "\nNew Line",
    }

def test_parse_header_with_mixed_case_and_whitespace():
    """Header should be case-insensitive and strip surrounding whitespace."""
    header = '  TEXT/HTML ;  CHARSET= "UTF-8" ;  boundary=abc123  '
    value, options = parse_content_header(header)
    assert value == "text/html"
    assert options == {"charset": "UTF-8", "boundary": "abc123"}
