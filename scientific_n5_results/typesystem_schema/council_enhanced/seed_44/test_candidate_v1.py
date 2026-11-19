import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer

def test_schema_validate_applies_defaults_and_excludes_read_only():
    schema = Schema(
        fields={
            "username": String(max_length=50),
            "age": Integer(),
            "read_only_field": String(read_only=True),
            "default_field": Integer(default=10),
        }
    )

    # Basic validation with required fields present
    input_data = {"username": "bob", "age": 25}
    result = schema.validate(input_data)
    assert result == {"username": "bob", "age": 25, "default_field": 10}
    assert "read_only_field" not in result

    # Provided read_only field should be ignored
    input_data_with_readonly = {"username": "bob", "age": 25, "read_only_field": "secret"}
    result2 = schema.validate(input_data_with_readonly)
    assert result2 == {"username": "bob", "age": 25, "default_field": 10}
    assert "read_only_field" not in result2

    # Provided default field overrides default
    input_data_with_default = {"username": "bob", "age": 25, "default_field": 42}
    result3 = schema.validate(input_data_with_default)
    assert result3 == {"username": "bob", "age": 25, "default_field": 42}
