import pytest
from typesystem.tokenize.tokenize_json import validate_json
from typesystem.fields import String
from typesystem.schemas import Schema
from typesystem.base import ParseError, Position

class SimpleSchema(Schema):
    name = String(min_length=1)

def test_validate_json_success():
    """Valid JSON should return parsed value and no errors."""
    json_str = '{"name": "Alice"}'
    value, errors = validate_json(json_str, SimpleSchema)
    assert value == {"name": "Alice"}
    assert errors == []

def test_validate_json_empty_string_error():
    """Empty string should raise ParseError with correct position."""
    with pytest.raises(ParseError) as excinfo:
        validate_json("", SimpleSchema)
    err = excinfo.value
    assert err.code == "no_content"
    assert err.text == "No content."
    assert isinstance(err.position, Position)
    assert err.position.line_no == 1
    assert err.position.column_no == 1
    assert err.position.char_index == 0

def test_validate_json_invalid_syntax_error():
    """Malformed JSON should raise ParseError with position from JSONDecodeError."""
    bad_json = '{"name": "Bob",}'  # trailing comma causes parse error
    with pytest.raises(ParseError) as excinfo:
        validate_json(bad_json, SimpleSchema)
    err = excinfo.value
    assert err.code == "parse_error"
    # The message should include the JSONDecodeError message
    assert "Expecting property name enclosed in double quotes" in err.text
    # Position should reflect the error location (column 18, line 1, char index 17)
    assert err.position.line_no == 1
    assert err.position.column_no == 18
    assert err.position.char_index == 17
