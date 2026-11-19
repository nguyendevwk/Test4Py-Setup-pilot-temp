import pytest
from typesystem.schemas import Schema
from typesystem.fields import String
from typesystem.base import ValidationError, Message

def test_schema_validate_required_and_default():
    # Define a schema with a required field `a` and a field `b` that has a default.
    schema = Schema(fields={"a": String(), "b": String(default="hello")})

    # Valid input: `a` provided, `b` omitted -> default should be applied.
    result = schema.validate({"a": "test"})
    assert result == {"a": "test", "b": "hello"}

    # Invalid input: missing required field `a` -> ValidationError with code "required".
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({})
    # The error should contain a Message with code "required" and index ["a"].
    messages = excinfo.value.messages
    assert any(
        isinstance(msg, Message) and msg.code == "required" and msg.index == ["a"]
        for msg in messages
    )
