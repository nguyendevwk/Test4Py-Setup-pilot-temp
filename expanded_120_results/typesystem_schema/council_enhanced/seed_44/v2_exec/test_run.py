import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError

def test_schema_validate_various_cases():
    schema = Schema(
        fields={
            "username": String(max_length=50),
            "age": Integer(),
            "email": String(default="default@example.com"),
            "read_only_field": String(read_only=True),
        }
    )

    # Valid input: defaults applied, read-only omitted
    valid_input = {"username": "bob", "age": 30, "read_only_field": "ignored"}
    result = schema.validate(valid_input)
    assert result == {"username": "bob", "age": 30, "email": "default@example.com"}
    assert "read_only_field" not in result

    # Missing required field 'age'
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"username": "bob"})
    error = excinfo.value
    messages = error.messages() if callable(error.messages) else error.messages
    assert any(msg.code == "required" and msg.index == ["age"] for msg in messages)

    # Non-dict input
    with pytest.raises(ValidationError) as excinfo:
        schema.validate("not a dict")
    error = excinfo.value
    messages = error.messages() if callable(error.messages) else error.messages
    assert any(msg.code == "type" for msg in messages)

    # Null input when allow_null is False
    with pytest.raises(ValidationError) as excinfo:
        schema.validate(None)
    error = excinfo.value
    messages = error.messages() if callable(error.messages) else error.messages
    assert any(msg.code == "null" for msg in messages)

    # Invalid key type
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({1: "bob", "age": 30})
    error = excinfo.value
    messages = error.messages() if callable(error.messages) else error.messages
    assert any(msg.code == "invalid_key" and msg.index == [1] for msg in messages)
