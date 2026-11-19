import pytest
from typesystem.base import Message, Position


def test_message_basic_initialization_and_equality():
    """Verify that a Message with only required arguments behaves correctly."""
    msg1 = Message(text="Error occurred")
    msg2 = Message(text="Error occurred")
    # Default code should be 'custom'
    assert msg1.code == "custom"
    # Index should be empty list
    assert msg1.index == []
    # Positions should be None
    assert msg1.start_position is None and msg1.end_position is None
    # Equality should hold for identical messages
    assert msg1 == msg2
    # Hash should be deterministic and based on code and index
    assert hash(msg1) == hash(msg2)


def test_message_with_key_and_position():
    """Test that providing a key sets index correctly and that position overrides start/end."""
    pos = Position(1, 5)
    msg = Message(text="Key error", key="username", position=pos)
    # Key should set index to ['username']
    assert msg.index == ["username"]
    # Position should set both start and end to the same Position instance
    assert msg.start_position == pos and msg.end_position == pos
    # Code defaults to 'custom'
    assert msg.code == "custom"
    # Equality with a manually constructed equivalent message
    expected = Message(text="Key error", key="username", position=pos)
    assert msg == expected


def test_message_invalid_argument_combination_raises():
    """Providing both key and index should raise an AssertionError."""
    with pytest.raises(AssertionError):
        Message(text="Invalid", key="id", index=[1, 2])
