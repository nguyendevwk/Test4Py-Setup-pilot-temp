import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError

def test_schema_validate_behavior():
    schema = Schema(
        fields={
            "username": String(max_length=50),
            "age": Integer(default=18),
        },
        allow_null=True,
    )
    # Valid input returns the same dict
    assert schema.validate({"username": "alice", "age": 30}) == {"username": "alice", "age": 30}
    # Missing optional field uses default
    assert schema.validate({"username": "bob"}) == {"username": "bob", "age": 18}
    # Missing required field raises a ValidationError with a 'required' message
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"age": 25})
    messages = excinfo.value.messages()
    assert any(msg.code == "required" and msg.index == ["username"] for msg in messages)
    # Null value is allowed when allow_null=True
    assert schema.validate(None) is None
    # Null value is not allowed when allow_null=False
    schema_no_null = Schema(fields={"username": String()})
    with pytest.raises(ValidationError) as excinfo:
        schema_no_null.validate(None)
    messages = excinfo.value.messages()
    assert messages[0].code == "null"
    # Invalid key type triggers an 'invalid_key' message
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({1: "invalid"})
    messages = excinfo.value.messages()
    assert any(msg.code == "invalid_key" for msg in messages)
