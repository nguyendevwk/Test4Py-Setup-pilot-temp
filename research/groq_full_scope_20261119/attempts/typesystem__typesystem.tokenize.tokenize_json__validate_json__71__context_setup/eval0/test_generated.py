import pytest
from typesystem.tokenize.tokenize_json import validate_json, tokenize_json
from typesystem.fields import String
from typesystem.schemas import Schema
from typesystem.base import ParseError, Position

class SimpleSchema(Schema):
    name = String(required=True)

def test_validate_json_success():
    # Valid JSON string should return the parsed value and no errors
    json_str = '{"name": "Alice"}'
    value, errors = validate_json(json_str, SimpleSchema)
    assert value == {"name": "Alice"}
    assert errors is None

def test_validate_json_empty_string_raises_parse_error():
    # Empty string should raise ParseError with specific code and position
    with pytest.raises(ParseError) as excinfo:
        tokenize_json("")
    err = excinfo.value
    assert err.code == "no_content"
    assert isinstance(err.position, Position)
    assert err.position.column_no == 1
    assert err.position.line_no == 1
    assert err.position.char_index == 0

def test_validate_json_invalid_syntax_raises_parse_error():
    # Malformed JSON should raise ParseError with correct position info
    bad_json = '{"name": "Bob",}'  # trailing comma causes parse error
    with pytest.raises(ParseError) as excinfo:
        tokenize_json(bad_json)
    err = excinfo.value
    assert err.code == "parse_error"
    # The error should point to the position of the trailing comma
    assert err.position.column_no == 18
    assert err.position.line_no == 1
    assert err.position.char_index == 17
