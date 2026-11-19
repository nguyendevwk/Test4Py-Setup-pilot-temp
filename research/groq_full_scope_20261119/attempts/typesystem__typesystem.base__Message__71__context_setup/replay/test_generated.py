import pytest
from typesystem.base import Message, Position


def test_message_initialization_with_key_and_position(tmp_path):
    """Normal construction using key and position."""
    pos = Position(1, 5, 10)
    msg = Message(text="Error", key="username", position=pos)
    assert msg.text == "Error"
    assert msg.code == "custom"
    assert msg.index == ["username"]
    assert msg.start_position is pos
    assert msg.end_position is pos
    # repr should include position
    rep = repr(msg)
    assert "position=Position(line_no=1" in rep
    # equality with identical message
    same = Message(text="Error", key="username", position=pos)
    assert msg == same
    # hash depends only on code and index
    assert hash(msg) == hash(same)


def test_message_start_end_positions_and_hash(tmp_path):
    """Construction using start_position and end_position separately."""
    start = Position(2, 3, 20)
    end = Position(2, 8, 25)
    msg = Message(
        text="Range error",
        code="range",
        index=[1, "field"],
        start_position=start,
        end_position=end,
    )
    assert msg.text == "Range error"
    assert msg.code == "range"
    assert msg.index == [1, "field"]
    assert msg.start_position is start
    assert msg.end_position is end
    # hash should be same for messages with same code and index
    other = Message(
        text="Different",
        code="range",
        index=[1, "field"],
        start_position=start,
        end_position=end,
    )
    assert hash(msg) == hash(other)
    # equality requires all fields match
    assert msg != other
    # repr should show start and end positions
    rep = repr(msg)
    assert "start_position=Position(line_no=2" in rep
    assert "end_position=Position(line_no=2" in rep


def test_message_invalid_combinations_raises():
    """Providing both key and index or both position and start_position should raise."""
    pos = Position(1, 1, 0)
    start = Position(1, 1, 0)
    end = Position(1, 2, 1)
    # key and index both provided
    with pytest.raises(AssertionError):
        Message(text="Bad", key="k", index=[1])
    # position and start_position both provided
    with pytest.raises(AssertionError):
        Message(text="Bad", position=pos, start_position=start, end_position=end)
    # position and end_position both provided
    with pytest.raises(AssertionError):
        Message(text="Bad", position=pos, end_position=end)
