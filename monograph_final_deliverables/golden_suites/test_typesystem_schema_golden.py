import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError

def test_schema_validate_behavior():
    # Schema with a required string and an optional integer default
    schema = Schema(fields={"username": String(max_length=50), "age": Integer(default=18)})

    # Valid input: all fields present
    valid_input = {"username": "alice", "age": 30}
    assert schema.validate(valid_input) == {"username": "alice", "age": 30}

    # Missing optional field: default should be applied
    missing_age = {"username": "bob"}
    assert schema.validate(missing_age) == {"username": "bob", "age": 18}

    # Missing required field: ValidationError with code 'required'
    missing_username = {"age": 25}
    with pytest.raises(ValidationError) as excinfo:
        schema.validate(missing_username)
    messages = excinfo.value.messages()
    assert any(m.code == "required" and m.index == ["username"] for m in messages)

    # Non‑string key: ValidationError with code 'invalid_key'
    non_string_key = {123: "value", "username": "charlie"}
    with pytest.raises(ValidationError) as excinfo:
        schema.validate(non_string_key)
    messages = excinfo.value.messages()
    assert any(m.code == "invalid_key" and m.index == [123] for m in messages)

    # Wrong type for username: ValidationError with code 'type'
    wrong_type = {"username": 123, "age": 20}
    with pytest.raises(ValidationError) as excinfo:
        schema.validate(wrong_type)
    messages = excinfo.value.messages()
    assert any(m.code == "type" and m.index == ["username"] for m in messages)
