import pytest
from typesystem.tokenize.tokens import Token
from typesystem.base import Message, ValidationError
from typesystem.tokenize.positional_validation import validate_with_positions


class SimplePosition:
    def __init__(self, char_index: int):
        self.char_index = char_index


def test_validate_with_positions_success():
    """Validator returns value unchanged when validation succeeds."""
    class DummyValidator:
        def validate(self, value):
            return value

    token = Token(value="ok", start=SimplePosition(0), end=SimplePosition(2))
    result = validate_with_positions(token=token, validator=DummyValidator())
    assert result == "ok"


def test_validate_with_positions_error_positions():
    """ValidationError messages receive correct start and end positions from token.lookup."""
    class DummyValidator:
        def validate(self, value):
            raise ValidationError(
                messages=[Message(text="error", code="test", index=())]
            )

    token = Token(value=None, start=SimplePosition(5), end=SimplePosition(10))
    # Ensure lookup returns the same token for any index
    token.lookup = lambda idx: token

    with pytest.raises(ValidationError) as excinfo:
        validate_with_positions(token=token, validator=DummyValidator())

    messages = excinfo.value.messages()
    assert len(messages) == 1
    msg = messages[0]
    assert msg.text == "error"
    assert msg.code == "test"
    assert msg.start_position.char_index == 5
    assert msg.end_position.char_index == 10


def test_validate_with_positions_sorting_by_position():
    """Multiple messages are sorted by start_position.char_index."""
    class DummyValidator:
        def validate(self, value):
            raise ValidationError(
                messages=[
                    Message(text="first", code="a", index=("first",)),
                    Message(text="second", code="b", index=("second",)),
                ]
            )

    token = Token(value=None, start=SimplePosition(0), end=SimplePosition(0))
    # Map index to start position for sorting
    def lookup(idx):
        # Use the first character of the index string as the position
        pos = SimplePosition(ord(idx[0][0]))
        return Token(value=None, start=pos, end=pos)
    token.lookup = lookup

    with pytest.raises(ValidationError) as excinfo:
        validate_with_positions(token=token, validator=DummyValidator())

    messages = excinfo.value.messages()
    # Messages should be sorted by start_position.char_index
    sorted_texts = [m.text for m in messages]
    assert sorted_texts == ["first", "second"]
    assert messages[0].start_position.char_index == ord("f")
    assert messages[1].start_position.char_index == ord("s")
