import json
import pytest
from typesystem.tokenize.tokenize_json import validate_json
from typesystem.schemas import Schema
from typesystem.fields import Field
from json.decoder import JSONDecodeError

class Person(Schema):
    name = Field(str)
    age = Field(int)

def test_validate_json_success():
    """Valid JSON should return the parsed value and no error messages."""
    content = json.dumps({"name": "Alice", "age": 30})
    value, errors = validate_json(content, Person)
    assert value == {"name": "Alice", "age": 30}
    assert errors == []

def test_validate_json_missing_field():
    """Missing required field should produce a validation error."""
    content = json.dumps({"name": "Bob"})
    value, errors = validate_json(content, Person)
    assert value == {"name": "Bob"}
    # The error message should mention the missing 'age' field
    assert any("age" in err for err in errors)

def test_validate_json_invalid_syntax():
    """Malformed JSON should raise a JSONDecodeError."""
    content = '{"name": "Charlie", "age": 25'  # missing closing brace
    with pytest.raises(JSONDecodeError):
        validate_json(content, Person)
