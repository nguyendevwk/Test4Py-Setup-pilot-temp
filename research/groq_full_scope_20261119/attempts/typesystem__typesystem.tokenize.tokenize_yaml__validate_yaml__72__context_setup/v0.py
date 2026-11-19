import pytest
from typesystem.tokenize.tokenize_yaml import validate_yaml
from typesystem.base import ParseError
from typesystem.fields import Field
from typesystem.schemas import Schema

def test_validate_yaml_valid_scalar(tmp_path):
    # A simple scalar that should validate against a Field
    yaml_content = "42"
    field = Field(int)
    value, errors = validate_yaml(yaml_content, field)
    assert value == 42
    assert errors == []

def test_validate_yaml_empty_content_raises(tmp_path):
    # Empty string should raise ParseError with code "no_content"
    yaml_content = ""
    field = Field(int)
    with pytest.raises(ParseError) as excinfo:
        validate_yaml(yaml_content, field)
    err = excinfo.value
    assert err.code == "no_content"
    assert err.text == "No content."
    assert err.position.line_no == 1
    assert err.position.column_no == 1
    assert err.position.char_index == 0

def test_validate_yaml_syntax_error(tmp_path):
    # Malformed YAML should raise ParseError with code "parse_error"
    yaml_content = "key: [unclosed list"
    field = Field(dict)
    with pytest.raises(ParseError) as excinfo:
        validate_yaml(yaml_content, field)
    err = excinfo.value
    assert err.code == "parse_error"
    assert "while parsing a block collection" in err.text or "mapping" in err.text
    # Position should point to the problematic character
    assert err.position.line_no == 1
    assert err.position.column_no > 0
    assert err.position.char_index > 0
