import pytest
from typesystem.base import ValidationError, Message, Position


def test_single_message_initialization_and_str():
    """Test that a single message is stored correctly and string representation works."""
    error = ValidationError(text="Invalid input", code="invalid")
    # The error should contain exactly one message
    assert len(error.messages()) == 1
    msg = error.messages()[0]
    assert isinstance(msg, Message)
    assert msg.text == "Invalid input"
    assert msg.code == "invalid"
    # No index for a top‑level message
    assert msg.index == []

    # __str__ should return the message text
    assert str(error) == "Invalid input"

    # __repr__ should include the class name and message details
    rep = repr(error)
    assert rep.startswith("ValidationError(")
    assert "text='Invalid input'" in rep
    assert "code='invalid'" in rep


def test_multiple_messages_and_dict_access():
    """Test that multiple messages are stored and accessible via dict interface."""
    msgs = [
        Message(text="Missing field", key="username"),
        Message(text="Too short", key="password", code="short"),
        Message(text="Invalid format", index=["profile", "email"]),
    ]
    error = ValidationError(messages=msgs)

    # messages() should return the same list
    assert error.messages() == msgs

    # The internal dict should map keys to message texts
    assert error["username"] == "Missing field"
    assert error["password"] == "Too short"
    # Nested key should be represented as a dict
    assert isinstance(error["profile"], dict)
    assert error["profile"]["email"] == "Invalid format"

    # Length of the error should be number of top‑level keys
    assert len(error) == 3

    # Iteration should yield top‑level keys
    assert set(iter(error)) == {"username", "password", "profile"}


def test_add_prefix_and_position_handling():
    """Test that add_prefix works and position attributes are preserved."""
    pos = Position(1, 5, 4)
    msgs = [
        Message(text="Error A", key="field1", position=pos),
        Message(text="Error B", index=["nested", 0], code="bad"),
    ]
    error = ValidationError(messages=msgs)

    # add_prefix should prepend the given key to each message's index
    prefixed = error.messages(add_prefix="root")
    assert len(prefixed) == 2
    assert prefixed[0].index == ["root", "field1"]
    assert prefixed[1].index == ["root", "nested", 0]

    # Position should be stored correctly
    assert prefixed[0].start_position == pos
    assert prefixed[0].end_position == pos
    # The second message has no position
    assert prefixed[1].start_position is None
    assert prefixed[1].end_position is None
