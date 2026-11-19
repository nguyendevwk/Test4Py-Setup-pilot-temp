import pytest
from typesystem.base import BaseError, Message, Position

def test_single_message_initialization_and_representation():
    # Create a single message error
    err = BaseError(text="Invalid value", code="invalid", key="age")
    # The error should contain one message
    assert len(err.messages()) == 1
    msg = err.messages()[0]
    assert isinstance(msg, Message)
    assert msg.text == "Invalid value"
    assert msg.code == "invalid"
    # The dict representation should be empty because no index
    assert dict(err) == {}
    # __str__ should return the message text
    assert str(err) == "Invalid value"
    # __repr__ should show the text and code
    assert repr(err) == "BaseError(text='Invalid value', code='invalid')"

def test_multiple_messages_and_dict_access():
    # Create multiple messages with nested indices
    m1 = Message(text="Missing field", code="required", index=["user", "name"])
    m2 = Message(text="Too short", code="min_length", index=["user", "name"])
    m3 = Message(text="Invalid email", code="format", index=["user", "email"])
    err = BaseError(messages=[m1, m2, m3])
    # The error should expose a nested dict structure
    assert len(err) == 1  # top-level key 'user'
    assert "user" in err
    user_dict = err["user"]
    assert isinstance(user_dict, dict)
    # The nested dict should contain keys 'name' and 'email'
    assert set(user_dict.keys()) == {"name", "email"}
    # The 'name' key should map to the last message text (overwritten)
    assert user_dict["name"] == "Too short"
    # The 'email' key should map to its message text
    assert user_dict["email"] == "Invalid email"
    # __str__ should return the dict representation
    assert str(err) == "{'user': {'name': 'Too short', 'email': 'Invalid email'}}"

def test_equality_and_hashing_of_errors():
    # Two errors with identical messages should be equal
    m1 = Message(text="Error A", code="a", index=["x"])
    m2 = Message(text="Error B", code="b", index=["y"])
    err1 = BaseError(messages=[m1, m2])
    err2 = BaseError(messages=[m1, m2])
    assert err1 == err2
    # Their hashes should match
    assert hash(err1) == hash(err2)
    # Changing message order should affect equality
    err3 = BaseError(messages=[m2, m1])
    assert err1 != err3
    # Hashes of different order should differ
    assert hash(err1) != hash(err3)
