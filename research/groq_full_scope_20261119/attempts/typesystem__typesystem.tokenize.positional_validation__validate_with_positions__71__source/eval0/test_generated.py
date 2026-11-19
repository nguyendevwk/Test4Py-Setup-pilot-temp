import pytest
from typesystem.tokenize.tokens import Token
from typesystem.fields import Field
from typesystem.schemas import Schema
from typesystem.tokenize.positional_validation import validate_with_positions
from typesystem.base import ValidationError, Message

class DummySchema(Schema):
    name = Field(str, required=True)

def test_validate_with_positions_success():
    token = Token(value="hello", start=0, end=5)
    result = validate_with_positions(token=token, validator=Field(str))
    assert result == "hello"

def test_validate_with_positions_required_field():
    token = Token(value={}, start=10, end=20)
    with pytest.raises(ValidationError) as excinfo:
        validate_with_positions(token=token, validator=DummySchema)
    errors = excinfo.value.messages()
    assert len(errors) == 1
    msg = errors[0]
    assert isinstance(msg, Message)
    assert msg.code == "required"
    assert msg.text == "The field 'name' is required."
    assert msg.start_position == 10
    assert msg.end_position == 20

def test_validate_with_positions_type_error():
    token = Token(value=123, start=30, end=35)
    with pytest.raises(ValidationError) as excinfo:
        validate_with_positions(token=token, validator=Field(str))
    errors = excinfo.value.messages()
    assert len(errors) == 1
    msg = errors[0]
    assert msg.code == "type"
    assert msg.text == "Expected string, got int."
    assert msg.start_position == 30
    assert msg.end_position == 35
