import pytest
from typesystem.tokenize.tokenize_json import validate_json
from typesystem.schemas import Schema
from typesystem.fields import Integer, String


class Person(Schema):
    name = String()
    age = Integer()


def test_validate_json_success(tmp_path):
    """Validate a correct JSON string against a schema."""
    json_content = '{"name": "Alice", "age": 30}'
    value, errors = validate_json(json_content, Person)
    assert errors == []
    assert value == {"name": "Alice", "age": 30}


def test_validate_json_invalid_syntax(tmp_path):
    """Validate a malformed JSON string and ensure an error is reported."""
    bad_json = '{"name": "Bob", "age": 25'  # missing closing brace
    value, errors = validate_json(bad_json, Person)
    assert value is None
    assert errors, "Expected at least one error for malformed JSON"
    assert any("Expecting" in e or "JSON" in e for e in errors)


def test_validate_json_validation_error(tmp_path):
    """Validate JSON that fails schema validation."""
    bad_json = '{"name": "Charlie", "age": "not a number"}'
    value, errors = validate_json(bad_json, Person)
    assert value is None
    assert errors, "Expected validation errors for incorrect field type"
    assert any("age" in e for e in errors)
