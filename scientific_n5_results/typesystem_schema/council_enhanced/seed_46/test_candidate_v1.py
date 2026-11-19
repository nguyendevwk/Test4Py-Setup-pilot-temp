import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError, Message

def test_schema_validate_behavior():
    schema = Schema(
        fields={
            "username": String(max_length=50),
            "age": Integer(default=18),
            "id": Integer(read_only=True),
        }
    )
    # Missing required field should raise ValidationError with code "required"
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"age": 30})
    err = excinfo.value
    assert any(m.code == "required" and m.index == ["username"] for m in err.messages)

    # Valid input should apply default and ignore read-only field
    result = schema.validate({"username": "alice"})
    assert result == {"username": "alice", "age": 18}

    # Non-string key should raise ValidationError with code "invalid_key"
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"username": "bob", 123: "oops"})
    err = excinfo.value
    assert any(m.code == "invalid_key" and m.index == [123] for m in err.messages)
