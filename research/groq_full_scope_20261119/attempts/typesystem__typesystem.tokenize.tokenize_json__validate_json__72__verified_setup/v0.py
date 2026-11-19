import pytest
from typesystem.tokenize.tokenize_json import validate_json
from typesystem.fields import Field
from typesystem.schemas import Schema
from typesystem.base import ParseError

def test_validate_json_success():
    """Valid JSON string against a simple Field should return the parsed value and no errors."""
    content = "123"
    validator = Field(int)
    value, errors = validate_json(content, validator)
    assert value == 123
    assert errors == []

def test_validate_json_syntax_error():
    """Malformed JSON should produce a non‑empty error message list."""
    content = '{"key": "value"'  # missing closing brace
    validator = Field(dict)
    value, errors = validate_json(content, validator)
    # The value should be None or an empty structure when parsing fails
    assert value is None or value == {}
    assert isinstance(errors, list)
    assert len(errors) > 0
    # Error message should mention a JSON parsing issue
    assert any("JSON" in err for err in errors)

def test_validate_json_type_error():
    """JSON that parses but fails type validation should return errors."""
    content = '"not an int"'
    validator = Field(int)
    value, errors = validate_json(content, validator)
    # The parsed value is a string, but validator expects int
    assert value == "not an int"
    assert isinstance(errors, list)
    assert len(errors) > 0
    # Error message should indicate a type mismatch
    assert any("type" in err.lower() for err in errors)
