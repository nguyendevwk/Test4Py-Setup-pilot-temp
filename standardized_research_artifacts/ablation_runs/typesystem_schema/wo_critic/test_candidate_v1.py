import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError

def test_schema_validate_behavior():
    # Setup a schema with required, default, and read-only fields
    schema = Schema(
        fields={
            "username": String(max_length=50),
            "age": Integer(default=18),
            "id": Integer(read_only=True),
        }
    )

    # 1. Missing required field 'username' should raise a ValidationError
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"age": 25})
    error = excinfo.value
    assert any(m.code == "required" and m.index == ["username"] for m in error.messages)
    assert len(error.messages) == 1

    # 2. Providing only 'username' should apply default for 'age' and ignore read-only 'id'
    validated = schema.validate({"username": "alice"})
    assert validated == {"username": "alice", "age": 18}
    assert "id" not in validated

    # 3. Non-string key should trigger an 'invalid_key' error
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"username": "bob", 123: "oops"})
    error = excinfo.value
    assert any(m.code == "invalid_key" and m.index == [123] for m in error.messages)
    assert len(error.messages) == 1

    # 4. Providing all fields including read-only should ignore the read-only value
    validated = schema.validate({"username": "carol", "age": 30, "id": 42})
    assert validated == {"username": "carol", "age": 30}
    assert "id" not in validated
