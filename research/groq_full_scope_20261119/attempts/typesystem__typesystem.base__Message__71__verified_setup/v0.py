import pytest
from typesystem.base import Message, Position


def test_message_initialization_and_repr(tmp_path):
    """Normal construction with all optional arguments and representation."""
    pos = Position(line=2, column=5)
    msg = Message(
        text="Error occurred",
        code="E001",
        key="username",
        position=pos,
    )
    # key overrides index
    assert msg.index == ["username"]
    assert msg.start_position is pos
    assert msg.end_position is pos
    # code defaults to provided value
    assert msg.code == "E001"
    # repr contains all fields
    rep = repr(msg)
    assert "Message(text='Error occurred'" in rep
    assert "code='E001'" in rep
    assert "index=['username']" in rep
    assert "position=Position(line=2, column=5)" in rep


def test_message_position_conflict_raises():
    """Providing both position and start_position/end_position should raise."""
    pos = Position(line=1, column=1)
    with pytest.raises(AssertionError):
        Message(
            text="Conflict",
            position=pos,
            start_position=pos,
        )
    with pytest.raises(AssertionError):
        Message(
            text="Conflict",
            position=pos,
            end_position=pos,
        )


def test_message_equality_and_hashing():
    """Messages with same code and index hash equal and hash consistent."""
    msg1 = Message(text="A", code="C", key="k")
    msg2 = Message(text="B", code="C", key="k")
    # Different text but same code and index => equal
    assert msg1 == msg2
    # Hash based on code and index only
    assert hash(msg1) == hash(msg2)
    # Different key leads to different index
    msg3 = Message(text="A", code="C", key="other")
    assert msg1 != msg3
    assert hash(msg1) != hash(msg3)
