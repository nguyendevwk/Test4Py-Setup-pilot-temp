import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError

def test_schema_validate_invalid_key_and_missing_required():
    schema = Schema(fields={"name": String(), "age": Integer()})
    bad_value = {"name": "Alice", 42: "invalid"}
    with pytest.raises(ValidationError) as excinfo:
        schema.validate(bad_value)
    messages = excinfo.value.messages
    # Expect both an invalid_key and a required error
    assert any(m.code == "invalid_key" for m in messages)
    assert any(m.code == "required" for m in messages)
    # Check that the indices are correct
    invalid_msg = next(m for m in messages if m.code == "invalid_key")
    required_msg = next(m for m in messages if m.code == "required")
    assert invalid_msg.index == [42]
    assert required_msg.index == ["age"]
