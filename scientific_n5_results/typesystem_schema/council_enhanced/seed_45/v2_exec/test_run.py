import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError


def test_schema_validate_behavior():
    schema = Schema(
        fields={
            "username": String(max_length=50),
            "age": Integer(default=18),
            "email": String(read_only=True),
        },
        allow_null=True,
    )

    # 1. None is allowed when allow_null=True
    assert schema.validate(None) is None

    # 2. Non-dict input raises a type error
    with pytest.raises(ValidationError) as excinfo:
        schema.validate("not a dict")
    assert excinfo.value.messages()[0].code == "type"

    # 3. Missing required field triggers a required error
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"age": 30})
    assert excinfo.value.messages()[0].code == "required"
    assert excinfo.value.messages()[0].index == ["username"]

    # 4. Valid input with default applied and read-only ignored
    result = schema.validate({"username": "alice"})
    assert result == {"username": "alice", "age": 18}

    # 5. Read-only field present in input is ignored
    result = schema.validate({"username": "bob", "email": "bob@example.com"})
    assert result == {"username": "bob", "age": 18}

    # 6. Non-string key triggers an invalid_key error
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({123: "value"})
    assert excinfo.value.messages()[0].code == "invalid_key"
    assert excinfo.value.messages()[0].index == [123]
