import pytest
from typesystem import Schema, fields
from typesystem.tokenize.json import validate_json


class Person(Schema):
    name = fields.String()
    age = fields.Integer()


def test_validate_json_success():
    """Valid JSON string should return the parsed value and no errors."""
    json_str = '{"name": "Alice", "age": 30}'
    value, errors = validate_json(json_str, Person)
    assert errors == []
    assert value == {"name": "Alice", "age": 30}
    # The returned value should be a dict matching the schema
    assert isinstance(value, dict)
    assert value["name"] == "Alice"
    assert value["age"] == 30


def test_validate_json_invalid_syntax():
    """Malformed JSON should produce a parse error message."""
    bad_json = '{"name": "Bob", "age": 25'  # missing closing brace
    value, errors = validate_json(bad_json, Person)
    # No value should be returned on parse failure
    assert value is None
    # There should be at least one error message
    assert errors
    # The error message should mention a JSON parsing issue
    assert any("JSON" in err for err in errors)


def test_validate_json_validation_error():
    """JSON that fails schema validation should return appropriate error."""
    json_str = '{"name": "Charlie", "age": "not_a_number"}'
    value, errors = validate_json(json_str, Person)
    # Value should be None because validation failed
    assert value is None
    # There should be an error about the age field type
    assert errors
    assert any("age" in err and "int" in err for err in errors)
