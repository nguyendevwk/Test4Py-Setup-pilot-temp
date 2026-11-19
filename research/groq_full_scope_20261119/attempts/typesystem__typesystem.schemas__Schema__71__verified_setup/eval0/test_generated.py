import pytest
from typesystem.schemas import Schema
from typesystem.fields import IntegerField, StringField
from typesystem.base import ValidationError

def test_schema_normal_validation_and_serialization():
    # Define a simple schema with two required fields
    schema = Schema(
        fields={
            "age": IntegerField(),
            "name": StringField(),
        }
    )
    # Valid input
    input_data = {"age": 30, "name": "Alice"}
    validated = schema.validate(input_data)
    assert validated == {"age": 30, "name": "Alice"}

    # Serialization should preserve the same structure
    serialized = schema.serialize(validated)
    assert serialized == {"age": 30, "name": "Alice"}

def test_schema_missing_required_field():
    schema = Schema(
        fields={
            "age": IntegerField(),
            "name": StringField(),
        }
    )
    # Missing 'name' key
    input_data = {"age": 25}
    with pytest.raises(ValidationError) as excinfo:
        schema.validate(input_data)
    # The error message should indicate the missing required field
    errors = excinfo.value.messages
    assert any(err.code == "required" and err.index == ["name"] for err in errors)

def test_schema_invalid_key_and_non_dict_input():
    schema = Schema(
        fields={
            "age": IntegerField(),
            "name": StringField(),
        }
    )
    # Input with a non-string key
    input_data = {1: 40, "name": "Bob"}
    with pytest.raises(ValidationError) as excinfo:
        schema.validate(input_data)
    errors = excinfo.value.messages
    assert any(err.code == "invalid_key" and err.index == [1] for err in errors)

    # Input that is not a dict or mapping
    with pytest.raises(ValidationError) as excinfo2:
        schema.validate(["not", "a", "dict"])
    assert excinfo2.value.messages[0].code == "type"
