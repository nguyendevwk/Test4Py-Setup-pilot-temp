import pytest
from typesystem.base import ValidationError, Message


def test_validation_error_messages_and_dict_structure():
    # Create a single message with an index
    msg = Message(text="Field is required", code="required", index=["field_a"])
    err = ValidationError(messages=[msg])

    # messages() should return the original message unchanged
    msgs = err.messages()
    assert isinstance(msgs, list)
    assert len(msgs) == 1
    assert msgs[0] is msg  # same instance

    # messages(add_prefix) should prepend the prefix to the index
    prefixed_msgs = err.messages(add_prefix="parent")
    assert isinstance(prefixed_msgs, list)
    assert len(prefixed_msgs) == 1
    pref_msg = prefixed_msgs[0]
    assert pref_msg.text == "Field is required"
    assert pref_msg.code == "required"
    assert pref_msg.index == ["parent", "field_a"]

    # The error should be iterable as a mapping of indices to texts
    # Converting to dict should give the nested structure
    error_dict = dict(err)
    assert error_dict == {"field_a": "Field is required"}

    # Test with multiple messages and nested indices
    msg2 = Message(text="Invalid value", code="invalid", index=["parent", "child"])
    err_multi = ValidationError(messages=[msg, msg2])

    # messages() returns both messages
    multi_msgs = err_multi.messages()
    assert len(multi_msgs) == 2
    texts = {m.text for m in multi_msgs}
    assert texts == {"Field is required", "Invalid value"}

    # dict conversion should nest accordingly
    multi_dict = dict(err_multi)
    assert multi_dict == {"field_a": "Field is required", "parent": {"child": "Invalid value"}}
