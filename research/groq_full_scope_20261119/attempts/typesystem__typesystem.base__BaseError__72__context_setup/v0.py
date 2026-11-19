import pytest
from typesystem.base import ValidationError, Message, Position


def test_single_message_initialization_and_dict_representation():
    # Create a ValidationError with a single message
    error = ValidationError(text="Invalid value", code="invalid", key="age")
    # The internal message list should contain one Message instance
    assert len(error._messages) == 1
    msg = error._messages[0]
    assert isinstance(msg, Message)
    assert msg.text == "Invalid value"
    assert msg.code == "invalid"
    # The key should be stored as the sole index element
    assert msg.index == ["age"]
    # The dict representation should map the key to the message text
    assert dict(error) == {"age": "Invalid value"}
    # Length of the error (number of top-level keys) should be 1
    assert len(error) == 1
    # Accessing the key should return the message text
    assert error["age"] == "Invalid value"
    # String representation for single message without index
    single_error = ValidationError(text="Only one")
    assert str(single_error) == "Only one"
    # Representation includes class name and text
    assert repr(single_error).startswith("ValidationError(text='Only one'")


def test_multiple_messages_and_prefixing():
    # Create multiple messages with nested indices
    m1 = Message(text="Missing field", key="name")
    m2 = Message(text="Too short", index=["user", 0, "email"])
    m3 = Message(text="Invalid format", index=["user", 1, "email"])
    error = ValidationError(messages=[m1, m2, m3])

    # The dict representation should nest keys appropriately
    expected_dict = {
        "name": "Missing field",
        "user": {
            0: {"email": "Too short"},
            1: {"email": "Invalid format"},
        },
    }
    assert dict(error) == expected_dict
    # Length should count top-level keys
    assert len(error) == 2

    # messages() without prefix returns original messages
    msgs = error.messages()
    assert msgs == [m1, m2, m3]

    # messages() with prefix adds the prefix to each message index
    prefixed = error.messages(add_prefix="root")
    assert all(msg.index[0] == "root" for msg in prefixed)
    # The rest of the index should remain unchanged
    assert prefixed[1].index == ["root", "user", 0, "email"]
    assert prefixed[2].index == ["root", "user", 1, "email"]


def test_error_on_invalid_initialization_and_equality():
    # Instantiating with both text and messages should raise an AssertionError
    with pytest.raises(AssertionError):
        ValidationError(text="foo", messages=[Message(text="bar")])

    # Instantiating with messages but missing required fields should raise an AssertionError
    with pytest.raises(AssertionError):
        ValidationError(messages=[])

    # Two ValidationError instances with identical messages should be equal
    e1 = ValidationError(messages=[Message(text="A", code="c1")])
    e2 = ValidationError(messages=[Message(text="A", code="c1")])
    assert e1 == e2

    # Different messages should not be equal
    e3 = ValidationError(messages=[Message(text="B", code="c1")])
    assert e1 != e3

    # Hash consistency
    assert hash(e1) == hash(e2)
    assert hash(e1) != hash(e3)
