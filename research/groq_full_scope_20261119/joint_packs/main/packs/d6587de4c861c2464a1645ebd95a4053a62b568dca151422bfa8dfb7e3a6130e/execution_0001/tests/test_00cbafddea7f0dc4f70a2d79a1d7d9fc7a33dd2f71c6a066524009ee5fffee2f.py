import pytest
from typesystem.base import Message


def test_message_initialization_and_repr():
    """Normal construction with all optional arguments and repr formatting."""
    msg = Message(
        text="Error occurred",
        code="err_code",
        key="username",
        start_position=5,
        end_position=10,
    )
    # key overrides index, index should be ['username']
    assert msg.index == ["username"]
    # code is preserved
    assert msg.code == "err_code"
    # start and end positions set correctly
    assert msg.start_position == 5
    assert msg.end_position == 10
    # repr includes all fields
    expected_repr = (
        "Message(text='Error occurred', code='err_code', index=['username'], "
        "start_position=5, end_position=10)"
    )
    assert repr(msg) == expected_repr


def test_message_position_overrides_and_hash():
    """Position argument overrides start/end and hash depends on code and index."""
    # Using position argument
    msg1 = Message(
        text="Pos error",
        position=3,
    )
    # start_position and end_position should both be 3
    assert msg1.start_position == 3
    assert msg1.end_position == 3
    # Using explicit start/end
    msg2 = Message(
        text="Range error",
        start_position=1,
        end_position=4,
    )
    assert msg2.start_position == 1
    assert msg2.end_position == 4
    # Hash should be based on code and index
    msg3 = Message(text="Same", code="dup", index=[1, 2])
    msg4 = Message(text="Same", code="dup", index=[1, 2])
    assert hash(msg3) == hash(msg4)
    # Different index yields different hash
    msg5 = Message(text="Diff", code="dup", index=[2, 1])
    assert hash(msg3) != hash(msg5)


def test_message_invalid_initialization_raises():
    """Providing both key and index should raise an AssertionError."""
    with pytest.raises(AssertionError):
        Message(text="Invalid", key="k", index=[1, 2])
    # Providing both position and start_position/end_position should also raise
    with pytest.raises(AssertionError):
        Message(text="Invalid", position=0, start_position=1)
    with pytest.raises(AssertionError):
        Message(text="Invalid", position=0, end_position=2)
