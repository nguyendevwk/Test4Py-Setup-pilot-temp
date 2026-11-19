import pytest
from typesystem.tokenize.positional_validation import validate_with_positions
from typesystem.fields import Field
from typesystem.schemas import Schema
from typesystem.base import ValidationError, Message


# Minimal token implementation that mimics the required interface
class DummyPosition:
    def __init__(self, char_index: int):
        self.char_index = char_index


class DummyToken:
    def __init__(self, value, start, end, lookup_map=None):
        self.value = value
        self.start = start
        self.end = end
        self._lookup_map = lookup_map or {}

    def lookup(self, index):
        # For simplicity, return the token itself or a mapped token
        return self._lookup_map.get(index, self)


def test_validate_with_positions_success():
    """When the validator succeeds, the original value is returned unchanged."""
    field = Field(int)
    token = DummyToken(value="123", start=DummyPosition(0), end=DummyPosition(3))
    result = validate_with_positions(token=token, validator=field)
    assert result == 123  # int conversion succeeds


def test_validate_with_positions_type_error_positions():
    """A type validation error should propagate a ValidationError with correct positions."""
    field = Field(int)
    token = DummyToken(value="abc", start=DummyPosition(10), end=DummyPosition(13))
    with pytest.raises(ValidationError) as excinfo:
        validate_with_positions(token=token, validator=field)
    # The ValidationError should contain a single message with the token's positions
    messages = excinfo.value.messages()
    assert len(messages) == 1
    msg = messages[0]
    assert isinstance(msg, Message)
    assert msg.start_position.char_index == 10
    assert msg.end_position.char_index == 13
    # The message text should indicate a type error
    assert "type" in msg.text.lower()


def test_validate_with_positions_required_error_sorted():
    """Required field errors should be sorted by start_position and contain correct text."""
    class Person(Schema):
        name = Field(str, required=True)
        age = Field(int, required=True)

    # Create tokens for each field; missing 'age' will trigger required error
    name_token = DummyToken(value="Alice", start=DummyPosition(5), end=DummyPosition(10))
    age_token = DummyToken(value=None, start=DummyPosition(15), end=DummyPosition(18))
    # Outer token that can look up field tokens
    outer_token = DummyToken(
        value={"name": "Alice"},
        start=DummyPosition(0),
        end=DummyPosition(20),
        lookup_map={("name",): name_token, ("age",): age_token},
    )

    with pytest.raises(ValidationError) as excinfo:
        validate_with_positions(token=outer_token, validator=Person)
    messages = excinfo.value.messages()
    # Only the missing 'age' field should produce a message
    assert len(messages) == 1
    msg = messages[0]
    assert msg.text == "The field 'age' is required."
    # The positions should come from the age_token
    assert msg.start_position.char_index == 15
    assert msg.end_position.char_index == 18
