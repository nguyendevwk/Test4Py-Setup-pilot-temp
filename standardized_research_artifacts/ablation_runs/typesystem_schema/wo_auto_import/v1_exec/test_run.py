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
    assert any(
        msg.code == "required" and msg.index == ["username"]
        for msg in excinfo.value.messages
    )

    # Invalid key type
    with pytest.raises(ValidationError) as excinfo2:
        schema.validate({"username": "charlie", 123: "oops", "age": 22})
    assert any(msg.code == "invalid_key" for msg in excinfo2.value.messages)

    # Null handling
    assert schema.validate(None) is None
    schema_no_null = Schema(fields={"username": String()})
    with pytest.raises(ValidationError) as excinfo3:
        schema_no_null.validate(None)
    assert any(msg.code == "null" for msg in excinfo3.value.messages)
