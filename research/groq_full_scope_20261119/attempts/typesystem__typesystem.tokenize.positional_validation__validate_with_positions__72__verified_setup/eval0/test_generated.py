import pytest
from typesystem.tokenize.positional_validation import validate_with_positions
from typesystem.fields import Field
from typesystem.schemas import Schema
from typesystem.tokenize.tokens import Token
from typesystem.base import ValidationError, Message

# Helper classes to mimic Position objects with a char_index attribute
class DummyPosition:
    def __init__(self, char_index: int):
        self.char_index = char_index

# Helper Token subclass that allows custom lookup behavior
class DummyToken(Token):
    def __init__(self, value, start, end, children=None):
        super().__init__(value, start, end)
        self._children = children or {}

    def lookup(self, index):
        # index is a tuple of keys; for simplicity, return the child token
        return self._children.get(index[0], self)

# Test 1: Successful validation passes through unchanged
def test_validate_with_positions_success(tmp_path):
    start = DummyPosition(0)
    end = DummyPosition(5)
    token = DummyToken(value=42, start=start, end=end)
    validator = Field(type=int, required=True)
    result = validate_with_positions(token=token, validator=validator)
    assert result == 42

# Test 2: Required field missing triggers a positional error message
def test_validate_with_positions_required_error(tmp_path):
    start = DummyPosition(10)
    end = DummyPosition(15)
    token = DummyToken(value=None, start=start, end=end)
    validator = Field(type=int, required=True)
    with pytest.raises(ValidationError) as excinfo:
        validate_with_positions(token=token, validator=validator)
    errors = excinfo.value.messages()
    assert len(errors) == 1
    msg = errors[0]
    assert isinstance(msg, Message)
    assert msg.code == "required"
    assert msg.text == "The field 'value' is required."
    assert msg.start_position == start
    assert msg.end_position == end

# Test 3: Type mismatch error preserves original token positions
def test_validate_with_positions_type_error(tmp_path):
    start = DummyPosition(20)
    end = DummyPosition(25)
    token = DummyToken(value="not-an-int", start=start, end=end)
    validator = Field(type=int, required=True)
    with pytest.raises(ValidationError) as excinfo:
        validate_with_positions(token=token, validator=validator)
    errors = excinfo.value.messages()
    assert len(errors) == 1
    msg = errors[0]
    assert isinstance(msg, Message)
    assert msg.code == "type"
    # The default message text for a type error includes the expected type
    assert "int" in msg.text
    assert msg.start_position == start
    assert msg.end_position == end
