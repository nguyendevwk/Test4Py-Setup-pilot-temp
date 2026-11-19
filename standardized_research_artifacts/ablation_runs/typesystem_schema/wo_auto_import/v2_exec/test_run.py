import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError


def test_schema_validate_behavior():
    schema = Schema(
        fields={
            "username": String(max_length=50),
            "age": Integer(),
            "status": String(default="active"),
            "id": Integer(read_only=True),
        },
        allow_null=True,
    )

    # Valid input with all fields
    input_data = {"username": "alice", "age": 30, "status": "inactive", "id": 1}
    validated = schema.validate(input_data)
    assert validated == {"username": "alice", "age": 30, "status": "inactive"}

    # Default applied when omitted
    validated_default = schema.validate({"username": "bob", "age": 25})
    assert validated_default["status"] == "active"

    # Missing required field
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"age": 20})
    messages = excinfo.value.messages()
    assert any(m.code == "required" and m.index == ["username"] for m in messages)

    # Invalid key type
    with pytest.raises(ValidationError) as excinfo2:
        schema.validate({"username": "charlie", 123: "oops", "age": 22})
    messages2 = excinfo2.value.messages()
    assert any(m.code == "invalid_key" for m in messages2)

    # Null handling
    assert schema.validate(None) is None
    schema_no_null = Schema(fields={"username": String()})
    with pytest.raises(ValidationError) as excinfo3:
        schema_no_null.validate(None)
    messages3 = excinfo3.value.messages()
    assert any(m.code == "null" for m in messages3)
