import pytest
from typesystem.schemas import Schema
from typesystem.fields import IntegerField
from typesystem.exceptions import ValidationError


def test_schema_validate_applies_defaults_and_validates_fields():
    # Define a schema with one required integer field and one optional field with a default.
    schema = Schema(
        fields={
            "a": IntegerField(),
            "b": IntegerField(default=5),
        }
    )

    # Validate input missing the optional field; default should be applied.
    result = schema.validate({"a": 10})
    assert result == {"a": 10, "b": 5}

    # Validate input providing both fields; defaults should not override provided values.
    result = schema.validate({"a": 20, "b": 30})
    assert result == {"a": 20, "b": 30}

    # Validate input missing the required field; a ValidationError should be raised.
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"b": 10})
    # The error message should indicate the missing required key.
    assert any(msg.code == "required" and msg.index == ["a"] for msg in excinfo.value.messages)
