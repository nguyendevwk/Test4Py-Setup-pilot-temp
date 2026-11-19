import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer, Field


def test_schema_validates_and_serializes_correctly():
    # Define a simple schema with a required string and an optional integer with default
    schema = Schema(
        fields={
            "name": String(required=True),
            "age": Integer(default=30),
        }
    )

    # Valid input: all required keys present, types match
    input_data = {"name": "Alice", "age": 25}
    validated = schema.validate(input_data)
    assert validated == {"name": "Alice", "age": 25}

    # Missing optional key should use default
    input_data_missing = {"name": "Bob"}
    validated_missing = schema.validate(input_data_missing)
    assert validated_missing == {"name": "Bob", "age": 30}

    # Serialization should preserve the same structure
    serialized = schema.serialize(validated_missing)
    assert serialized == {"name": "Bob", "age": 30}


def test_schema_raises_error_for_missing_required_key():
    schema = Schema(
        fields={
            "title": String(required=True),
            "description": String(),
        }
    )

    # Input missing the required 'title' key
    bad_input = {"description": "A test"}
    with pytest.raises(Exception) as excinfo:
        schema.validate(bad_input)

    # The exception should be a ValidationError with a message about the missing key
    assert hasattr(excinfo.value, "messages")
    messages = excinfo.value.messages
    assert any(msg.code == "required" and msg.index == ["title"] for msg in messages)


def test_schema_detects_non_string_keys_and_raises_error():
    schema = Schema(
        fields={
            "id": Integer(required=True),
            "name": String(),
        }
    )

    # Input with a non-string key (e.g., an integer key)
    bad_input = {1: 123, "name": "Test"}
    with pytest.raises(Exception) as excinfo:
        schema.validate(bad_input)

    # The exception should contain an error about the invalid key
    assert hasattr(excinfo.value, "messages")
    messages = excinfo.value.messages
    assert any(msg.code == "invalid_key" and msg.index == [1] for msg in messages)
