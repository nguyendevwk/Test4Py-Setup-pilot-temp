import pytest
import typesystem
from typesystem.fields import String
from typesystem.schemas import Schema
from typesystem.tokenize.tokens import ScalarToken
from typesystem.tokenize.tokenize_yaml import validate_yaml

# Test 1: Valid YAML string with a simple Field validator
def test_validate_yaml_valid_string():
    yaml_content = "name: Alice\nage: 30"
    validator = String()
    value, errors = validate_yaml(yaml_content, validator)
    # The validator is a String, so the whole YAML is treated as a string value
    assert isinstance(value, str)
    assert value == yaml_content
    assert errors == []

# Test 2: Valid YAML bytes with a Schema validator
def test_validate_yaml_valid_bytes():
    class Person(Schema):
        name = String()
        age = String()
    yaml_bytes = b"name: Bob\nage: 25"
    value, errors = validate_yaml(yaml_bytes, Person)
    assert isinstance(value, dict)
    assert value == {"name": "Bob", "age": "25"}
    assert errors == []

# Test 3: Invalid YAML content should produce error messages
def test_validate_yaml_invalid_yaml():
    invalid_yaml = "name: Charlie\nage: [unclosed list"
    validator = String()
    value, errors = validate_yaml(invalid_yaml, validator)
    # Value should be None or partial, but errors should not be empty
    assert errors != []
    # Each error message should be a string containing the word 'error'
    assert all(isinstance(err, str) and "error" in err.lower() for err in errors)
