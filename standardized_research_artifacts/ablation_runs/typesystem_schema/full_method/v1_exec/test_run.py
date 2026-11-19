import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError, Message

def test_schema_validate_required_default_and_readonly():
    # Setup schema with required, default, and read‑only fields
    schema = Schema(
        fields={
            "username": String(max_length=50),
            "age": Integer(),
            "bio": String(default="No bio"),
            "id": Integer(read_only=True),
        }
    )

    # 1. Valid input: defaults applied, read‑only ignored
    validated = schema.validate({"username": "alice", "age": 30})
    assert validated == {"username": "alice", "age": 30, "bio": "No bio"}

    # 2. Missing required field triggers ValidationError
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"age": 30})
    messages = excinfo.value.messages
    assert any(m.code == "required" and m.index == ["username"] for m in messages)

    # 3. Non‑string key triggers ValidationError
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({123: "value", "username": "bob", "age": 25})
    messages = excinfo.value.messages
    assert any(m.code == "invalid_key" and m.index == [123] for m in messages)

    # 4. allow_null=True returns None for None input
    nullable_schema = Schema(
        fields={"username": String()}, allow_null=True
    )
    assert nullable_schema.validate(None) is None
