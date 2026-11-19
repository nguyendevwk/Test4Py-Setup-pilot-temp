import pytest
from typesystem.base import ValidationError, Message


def test_validation_error_messages_and_prefix():
    # Create two messages with nested indices
    msg_a = Message(text="Field is required", code="required", index=["field_a"])
    msg_b = Message(text="Invalid value", code="invalid", index=["field_b", "subfield"])

    # Instantiate ValidationError with a list of messages
    error = ValidationError(messages=[msg_a, msg_b])

    # The internal message list should match the input
    assert error._messages == [msg_a, msg_b]

    # The internal dict should map indices to texts, nesting as needed
    expected_dict = {
        "field_a": "Field is required",
        "field_b": {"subfield": "Invalid value"},
    }
    assert error._message_dict == expected_dict

    # messages() should return a copy of the original list
    assert error.messages() == [msg_a, msg_b]

    # messages(add_prefix) should prepend the prefix to each message's index
    prefixed = error.messages(add_prefix="parent")
    assert len(prefixed) == 2
    assert prefixed[0].index == ["parent", "field_a"]
    assert prefixed[0].text == "Field is required"
    assert prefixed[1].index == ["parent", "field_b", "subfield"]
    assert prefixed[1].text == "Invalid value"

    # Instantiating with a single message via keyword arguments
    single_error = ValidationError(text="Single error", code="single", key="k")
    single_msg = single_error.messages()[0]
    assert single_msg.text == "Single error"
    assert single_msg.code == "single"
    # The index should default to an empty list when not provided
    assert single_msg.index == []
