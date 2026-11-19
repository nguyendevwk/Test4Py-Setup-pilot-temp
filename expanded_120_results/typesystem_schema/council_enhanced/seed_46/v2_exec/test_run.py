import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError


def test_schema_validate_defaults_and_readonly_and_required():
    # Schema with a default value for a required field
    schema_default = Schema(
        fields={"username": String(max_length=50), "age": Integer(default=18)}
    )
    result = schema_default.validate({"username": "bob"})
    assert result == {"username": "bob", "age": 18}

    # Schema with a read‑only field that should be ignored during validation
    schema_readonly = Schema(
        fields={
            "username": String(max_length=50),
            "age": Integer(),
            "token": String(read_only=True),
        }
    )
    result = schema_readonly.validate(
        {"username": "alice", "age": 30, "token": "secret"}
    )
    assert result == {"username": "alice", "age": 30}
    assert "token" not in result

    # Schema that raises a ValidationError when a required field is missing
    schema_missing = Schema(
        fields={"username": String(max_length=50), "age": Integer()}
    )
    with pytest.raises(ValidationError) as excinfo:
        schema_missing.validate({"username": "charlie"})
    error = excinfo.value
    assert any(
        msg.code == "required" and msg.index == ["age"] for msg in error.messages()
    )

    # Schema that allows None to be returned unchanged
    schema_null = Schema(fields={"username": String(max_length=50)}, allow_null=True)
    assert schema_null.validate(None) is None
