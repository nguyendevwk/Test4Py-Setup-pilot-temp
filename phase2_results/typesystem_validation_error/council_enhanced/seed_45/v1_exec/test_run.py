import pytest
from typesystem.base import ValidationError, Message

def test_validation_error_messages_and_state():
    # Instantiate with a list of messages
    msg = Message(text="Field is required", code="required", index=["field_a"])
    err = ValidationError(messages=[msg])

    # messages() returns the original list of Message objects
    msgs = err.messages()
    assert isinstance(msgs, list)
    assert len(msgs) == 1
    m = msgs[0]
    assert m.text == "Field is required"
    assert m.code == "required"
    assert m.index == ["field_a"]

    # add_prefix prepends a key to each message index
    prefixed = err.messages(add_prefix="parent")
    assert prefixed[0].index == ["parent", "field_a"]

    # Instantiate with single message via keyword arguments
    err_single = ValidationError(text="Missing", code="missing")
    msgs_single = err_single.messages()
    assert len(msgs_single) == 1
    m_single = msgs_single[0]
    assert m_single.text == "Missing"
    assert m_single.code == "missing"
    assert m_single.index == []

    # Ensure messages() returns a new list each call
    assert msgs is not msgs_single
