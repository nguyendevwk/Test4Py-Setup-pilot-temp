import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError, Message


def test_schema_validate_missing_required_field():
    """Schema.validate should raise a ValidationError with a 'required' message
    when a required field is omitted from the input dictionary."""
    schema = Schema(fields={"name": String(), "age": Integer()})
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"name": "bob"})
    error = excinfo.value
    # The error should contain exactly one message about the missing 'age' key
    messages = error.messages()
    assert len(messages) == 1
    msg = messages[0]
    assert isinstance(msg, Message)
    assert msg.code == "required"
    assert msg.index == ["age"]
