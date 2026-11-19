import pytest
from typesystem.base import ValidationError, Message

def test_validation_error_messages_and_dict():
    # Create two distinct messages with nested indices
    msg1 = Message(text="Field is required", code="required", index=["field_a"])
    msg2 = Message(text="Invalid type", code="type_error", index=["field_b", "subfield"])

    # Instantiate ValidationError with a list of messages
    err = ValidationError(messages=[msg1, msg2])

    # messages() returns a list of Message objects
    msgs = err.messages()
    assert isinstance(msgs, list)
    assert len(msgs) == 2
    assert msgs[0].text == "Field is required"
    assert msgs[1].index == ["field_b", "subfield"]

    # messages() returns a new list each call
    msgs2 = err.messages()
    assert msgs is not msgs2

    # Modifying the returned list does not affect the internal state
    msgs2.append(Message(text="Extra", code="extra", index=["extra"]))
    assert len(err.messages()) == 2

    # add_prefix correctly prepends to each message index
    prefixed = err.messages(add_prefix="parent")
    assert prefixed[0].index == ["parent", "field_a"]
    assert prefixed[1].index == ["parent", "field_b", "subfield"]

    # __iter__ yields a nested dictionary representation
    mapping = dict(err)
    expected = {
        "field_a": "Field is required",
        "field_b": {"subfield": "Invalid type"},
    }
    assert mapping == expected
