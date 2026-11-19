import pytest
from typesystem.base import Message, ValidationError
from typesystem.tokenize.tokens import Token, Position


class DummyValidator:
    """A minimal validator that simply returns the value."""
    def validate(self, value):
        return value


class DummyToken(Token):
    """Token subclass that returns itself for any lookup."""
    def lookup(self, index):
        return self


def test_validate_with_positions_normal(tmp_path):
    """validate_with_positions should return the value when validation succeeds."""
    token = DummyToken(value=42, start=Position(0, 0), end=Position(0, 0))
    validator = DummyValidator()
    result = validate_with_positions(token=token, validator=validator)
    assert result == 42


def test_validate_with_positions_required_error(tmp_path):
    """validate_with_positions should transform a 'required' ValidationError into a positional message."""
    token = DummyToken(value={}, start=Position(10, 0), end=Position(10, 0))
    # Create a ValidationError with a 'required' message
    msg = Message(
        text="",
        code="required",
        index=[0],
        start_position=None,
        end_position=None,
    )
    error = ValidationError(messages=[msg])

    class RequiredValidator:
        def validate(self, value):
            raise error

    validator = RequiredValidator()
    with pytest.raises(ValidationError) as excinfo:
        validate_with_positions(token=token, validator=validator)

    raised = excinfo.value
    assert len(raised.messages) == 1
    raised_msg = raised.messages[0]
    assert raised_msg.text == "The field '0' is required."
    assert raised_msg.code == "required"
    assert raised_msg.start_position == token.start
    assert raised_msg.end_position == token.end


def test_validate_with_positions_other_error(tmp_path):
    """validate_with_positions should preserve non-required error messages with positions."""
    token = DummyToken(value={}, start=Position(20, 0), end=Position(20, 0))
    # Create a ValidationError with a non-required message
    msg = Message(
        text="Invalid value",
        code="invalid",
        index=[0],
        start_position=None,
        end_position=None,
    )
    error = ValidationError(messages=[msg])

    class InvalidValidator:
        def validate(self, value):
            raise error

    validator = InvalidValidator()
    with pytest.raises(ValidationError) as excinfo:
        validate_with_positions(token=token, validator=validator)

    raised = excinfo.value
    assert len(raised.messages) == 1
    raised_msg = raised.messages[0]
    assert raised_msg.text == "Invalid value"
    assert raised_msg.code == "invalid"
    assert raised_msg.start_position == token.start
    assert raised_msg.end_position == token.end
