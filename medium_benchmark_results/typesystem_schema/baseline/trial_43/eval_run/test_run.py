import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError, Message

def test_schema_validate_missing_required_field_raises_error():
    # Define a schema with two required fields: 'name' and 'age'.
    schema = Schema(fields={"name": String(), "age": Integer()})
    # Input missing the 'age' field.
    input_data = {"name": "Alice"}
    # Validate and expect a ValidationError.
    with pytest.raises(ValidationError) as excinfo:
        schema.validate(input_data)
    error = excinfo.value
    # There should be exactly one error message.
    assert len(error.messages) == 1
    # The error message should indicate a missing required field.
    msg: Message = error.messages[0]
    assert msg.code == "required"
    assert msg.index == ["age"]
