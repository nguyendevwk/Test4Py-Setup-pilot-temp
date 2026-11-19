import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError

def test_schema_validate_required_and_defaults_and_read_only():
    schema = Schema(
        fields={
            "username": String(max_length=50),
            "age": Integer(default=18),
            "email": String(read_only=True)
        },
        allow_null=False
    )
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"age": 30})
    assert any(msg.code == "required" and msg.index == ["username"] for msg in excinfo.value.messages)

    result = schema.validate({"username": "alice"})
    assert result == {"username": "alice", "age": 18}

    result = schema.validate({"username": "bob", "email": "bob@example.com"})
    assert "email" not in result

    schema_null = Schema(fields={"x": Integer()}, allow_null=True)
    assert schema_null.validate(None) is None
