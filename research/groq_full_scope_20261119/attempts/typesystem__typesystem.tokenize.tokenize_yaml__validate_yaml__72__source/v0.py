import pytest
import typesystem
from typesystem.tokenize.tokenize_yaml import validate_yaml
from typesystem.fields import Field
from typesystem.schemas import Schema
from typesystem.base import ParseError

def test_validate_yaml_success(tmp_path):
    # Create a simple YAML string and validate against a Field
    yaml_content = "name: Alice\nage: 30"
    # Use a Schema to validate the mapping
    class Person(Schema):
        name = Field(str)
        age = Field(int)
    value, errors = validate_yaml(yaml_content, Person)
    assert isinstance(value, dict)
    assert value == {"name": "Alice", "age": 30}
    assert errors == []

def test_validate_yaml_empty_string(tmp_path):
    # Empty YAML string should produce an empty dict with no errors
    yaml_content = ""
    class Empty(Schema):
        pass
    value, errors = validate_yaml(yaml_content, Empty)
    assert value == {}
    assert errors == []

def test_validate_yaml_invalid_syntax(tmp_path):
    # Malformed YAML should raise a ParseError
    yaml_content = "name: Alice\nage: [30, 31"
    with pytest.raises(ParseError):
        validate_yaml(yaml_content, Field(dict))
