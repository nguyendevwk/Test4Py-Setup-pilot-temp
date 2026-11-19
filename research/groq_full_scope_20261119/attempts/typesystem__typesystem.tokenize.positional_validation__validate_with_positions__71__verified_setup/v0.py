import pytest
from typesystem.tokenize.tokens import Token
from typesystem.schemas import Schema
from typesystem.fields import Field
from typesystem.base import ValidationError, Message

# Helper classes for positions
class DummyPosition:
    def __init__(self, char_index: int):
        self.char_index = char_index

# Subclass Token to control lookup behavior
class DummyToken(Token):
    def __init__(self, value, start_index, end_index, nested_lookup=None):
        super().__init__(value=value, start=DummyPosition(start_index), end=DummyPosition(end_index))
        self._nested_lookup = nested_lookup or {}

    def lookup(self, index):
        # Return a token representing the field at the given index
        # For simplicity, use nested_lookup dict mapping index tuple to start/end indices
        key = tuple(index)
        if key in self._nested_lookup:
            start, end = self._nested_lookup[key]
            return DummyToken(value=None, start_index=start, end_index=end)
        # Default to self if not found
        return self

def test_required_field_missing():
    # Schema with a required field
    schema = Schema(name=Field(required=True))
    # Token representing an empty dict, with root start at 0
    token = DummyToken(value={}, start_index=0, end_index=0)
    with pytest.raises(ValidationError) as excinfo:
        validate_with_positions(token=token, validator=schema)
    errors = excinfo.value.messages()
    assert len(errors) == 1
    msg = errors[0]
    assert isinstance(msg, Message)
    assert msg.text == "The field 'name' is required."
    assert msg.code == "required"
    assert msg.start_position.char_index == 0
    assert msg.end_position.char_index == 0

def test_type_mismatch_error():
    # Schema expecting an int
    schema = Schema(age=Field(type=int))
    # Token with wrong type, start at 10
    token = DummyToken(value={"age": "abc"}, start_index=10, end_index=20)
    # Provide lookup mapping for 'age' field
    token._nested_lookup = {('age',): (15, 18)}
    with pytest.raises(ValidationError) as excinfo:
        validate_with_positions(token=token, validator=schema)
    errors = excinfo.value.messages()
    assert len(errors) == 1
    msg = errors[0]
    assert isinstance(msg, Message)
    # The original message text from Field.validate
    assert "must be of type" in msg.text
    assert msg.code == "type"
    assert msg.start_position.char_index == 15
    assert msg.end_position.char_index == 18

def test_nested_field_error_sorted_by_position():
    # Schema with nested fields
    class AddressSchema(Schema):
        street = Field(required=True)
        zip = Field(type=int)
    class PersonSchema(Schema):
        name = Field(required=True)
        address = Field(type=AddressSchema)
    schema = PersonSchema()
    # Token with errors in two nested fields at different positions
    token = DummyToken(value={"address": {"zip": "abc"}}, start_index=0, end_index=30)
    # Map nested indices to positions
    token._nested_lookup = {
        ('address', 'street'): (5, 10),   # missing required
        ('address', 'zip'): (15, 20),     # type mismatch
    }
    with pytest.raises(ValidationError) as excinfo:
        validate_with_positions(token=token, validator=schema)
    errors = excinfo.value.messages()
    # Two messages expected
    assert len(errors) == 2
    # They should be sorted by start_position.char_index
    assert errors[0].start_position.char_index == 5
    assert errors[1].start_position.char_index == 15
    # Check texts
    assert errors[0].text == "The field 'street' is required."
    assert "must be of type" in errors[1].text
