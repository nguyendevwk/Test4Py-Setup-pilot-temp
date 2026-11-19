import pytest
from sanic.headers import parse_content_header

def test_parse_simple_header():
    header = "text/html; charset=UTF-8"
    value, options = parse_content_header(header)
    assert value == "text/html"
    assert options == {"charset": "UTF-8"}

def test_parse_header_with_special_characters():
    header = 'form-data; name=upload; filename="%22file%22.txt%0D%0A"'
    value, options = parse_content_header(header)
    assert value == "form-data"
    # %22 should become ", %0D%0A should become newline
    assert options["name"] == "upload"
    assert options["filename"] == '"file".txt\n'

def test_parse_header_without_options():
    header = "application/json"
    value, options = parse_content_header(header)
    assert value == "application/json"
    assert options == {}
