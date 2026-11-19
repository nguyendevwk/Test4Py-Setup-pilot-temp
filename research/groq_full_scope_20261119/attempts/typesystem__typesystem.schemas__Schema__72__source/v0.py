import pytest
from typesystem.schemas import Schema
from typesystem.fields import IntegerField, StringField
from typesystem.base import ValidationError

def test_schema_normal_validation_and_serialization():
    """Schema validates a correct dict and serializes it back."""
    schema = Schema(
        fields={
            "age": IntegerField(),
            "name": StringField(),
        }
    )
    input_data = {"age": 30, "name": "Alice"}
    validated = schema.validate(input_data)
    assert validated == {"age": 30, "name": "Alice"}
    serialized = schema.serialize(validated)
    assert serialized == {"age": 30, "name": "Alice"}

def test_schema_missing_required_raises_error():
    """Missing a required key triggers a ValidationError with the correct message."""
    schema = Schema(
        fields={
            "age": IntegerField(),
            "name": StringField(),
        }
    )
    input_data = {"age": 25}
    with pytest.raises(ValidationError) as excinfo:
        schema.validate(input_data)
    errors = excinfo.value.messages
    # There should be one error about the missing 'name' key
    assert len(errors) == 1
    assert errors[0].code == "required"
    assert errors[0].index == ["name"]
    assert "required" in errors[0].text

def test_schema_invalid_key_type_raises_error():
    """A non-string key in the input dict triggers an invalid_key error."""
    schema = Schema(
        fields={
            "age": IntegerField(),
            "name": StringField(),
        }
    )
    input_data = {1: 40, "name": "Bob"}  # key 1 is not a string
    with pytest.raises(ValidationError) as excinfo:
        schema.validate(input_data)
    errors = excinfo.value.messages
    # There should be one error about the invalid key
    assert len(errors) == 1
    assert errors[0].code == "invalid_key"
    assert errors[0].index == [1]
    assert "invalid_key" in errors[0].text
