import pytest
from typesystem.schemas import Schema, ValidationError
from typesystem.fields import Integer, Message

def test_schema_validate_missing_required_raises_error():
    # A schema with one required field 'a' and one read‑only field 'b'.
    schema = Schema(fields={"a": Integer(), "b": Integer(read_only=True)})

    # Validate a dict missing the required key 'a'.
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"b": 1})

    # The ValidationError should contain a Message for the missing required key.
    messages = excinfo.value.messages
    assert any(
        isinstance(msg, Message) and msg.code == "required" and msg.index == ["a"]
        for msg in messages
    ), f"Expected a 'required' message for key 'a', got {messages}"
