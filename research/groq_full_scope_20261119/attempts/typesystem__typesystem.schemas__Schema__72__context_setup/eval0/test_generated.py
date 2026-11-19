import pytest
from typesystem.schemas import Schema
from typesystem.fields import IntegerField, StringField
from typesystem.base import ValidationError


def test_schema_validates_and_serializes_correctly():
    """Schema should validate a correct dict and serialize it back."""
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


def test_schema_missing_required_key_raises_error():
    """Schema should raise ValidationError when a required key is missing."""
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
    assert any(err.code == "required" and err.index == ["name"] for err in errors)


def test_schema_invalid_key_type_raises_error():
    """Schema should raise ValidationError when a key is not a string."""
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
    assert any(err.code == "invalid_key" and err.index == [1] for err in errors)
