import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError

def test_schema_missing_required_field_raises_validation_error():
    schema = Schema(fields={"username": String(max_length=50), "age": Integer()})
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"username": "alice"})
    error = excinfo.value
    assert hasattr(error, "messages")
    messages = error.messages
    assert isinstance(messages, list)
    assert len(messages) == 1
    msg = messages[0]
    assert msg.code == "required"
    assert msg.index == ["age"]
