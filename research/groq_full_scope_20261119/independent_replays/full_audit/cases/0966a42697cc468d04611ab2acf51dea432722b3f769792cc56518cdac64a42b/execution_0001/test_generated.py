import pytest
from typesystem.base import Message


def test_message_initialization_with_all_fields():
    """Verify that all fields are stored correctly when provided."""
    msg = Message(
        text="Error occurred",
        code="E001",
        key="username",
        position="pos1",
    )
    assert msg.text == "Error occurred"
    assert msg.code == "E001"
    assert msg.index == ["username"]
    assert msg.start_position == "pos1"
    assert msg.end_position == "pos1"


def test_message_index_and_start_end_positions():
    """Check that index and separate start/end positions are handled."""
    msg = Message(
        text="Another error",
        index=[1, "field"],
        start_position="start",
        end_position="end",
    )
    assert msg.text == "Another error"
    assert msg.code == "custom"
    assert msg.index == [1, "field"]
    assert msg.start_position == "start"
    assert msg.end_position == "end"


def test_message_invalid_combination_raises():
    """Providing both position and start_position should raise an AssertionError."""
    with pytest.raises(AssertionError):
        Message(
            text="Invalid",
            position="pos",
            start_position="start",
        )
