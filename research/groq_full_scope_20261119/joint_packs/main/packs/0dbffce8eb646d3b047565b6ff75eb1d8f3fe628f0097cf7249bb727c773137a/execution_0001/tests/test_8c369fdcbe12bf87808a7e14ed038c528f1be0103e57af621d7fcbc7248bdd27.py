import pytest
from typesystem.base import Message, Position


def test_message_initialization_with_key_and_index_conflict():
    """When a key is supplied, index must be None and index is set to [key]."""
    msg = Message(text="error", key="username")
    assert msg.text == "error"
    assert msg.code == "custom"
    assert msg.index == ["username"]
    assert msg.start_position is None
    assert msg.end_position is None
    # Providing both key and index should raise an AssertionError
    with pytest.raises(AssertionError):
        Message(text="error", key="username", index=[1, 2])


def test_message_position_handling_and_repr():
    """Position arguments are mutually exclusive and repr reflects them."""
    pos = Position(1, 5, 10)
    # Using position sets both start and end to the same value
    msg1 = Message(text="err", position=pos)
    assert msg1.start_position == pos
    assert msg1.end_position == pos
    # Using start_position and end_position separately
    msg2 = Message(text="err", start_position=pos, end_position=pos)
    assert msg2.start_position == pos
    assert msg2.end_position == pos
    # repr should include position when start==end
    assert "position=Position(line_no=1, column_no=5, char_index=10)" in repr(msg1)
    # repr should include start and end when they differ
    pos2 = Position(2, 3, 20)
    msg3 = Message(text="err", start_position=pos, end_position=pos2)
    assert "start_position=Position(line_no=1, column_no=5, char_index=10)" in repr(msg3)
    assert "end_position=Position(line_no=2, column_no=3, char_index=20)" in repr(msg3)


def test_message_equality_and_hashing():
    """Messages with same content are equal and hash consistently."""
    msg_a = Message(text="dup", code="code1", index=[1, 2])
    msg_b = Message(text="dup", code="code1", index=[1, 2])
    msg_c = Message(text="dup", code="code2", index=[1, 2])
    assert msg_a == msg_b
    assert msg_a != msg_c
    # Hash depends only on code and index
    assert hash(msg_a) == hash(msg_b)
    assert hash(msg_a) != hash(msg_c)
