import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError, Message

def test_schema_missing_required_field_raises_validation_error():
    # Arrange: schema with two required fields
    schema = Schema(fields={"name": String(), "age": Integer()})
    # Act & Assert: missing 'age' triggers ValidationError with correct message
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"name": "Alice"})
    messages = excinfo.value.messages
    assert len(messages) == 1
    msg = messages[0]
    assert isinstance(msg, Message)
    assert msg.code == "required"
    assert msg.index == ["age"]
