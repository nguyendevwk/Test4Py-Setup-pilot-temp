import pytest
from typesystem.base import BaseError, Message

def test_single_message_initialization_and_str():
    # Instantiate with a single message
    err = BaseError(text="Invalid input", code="invalid", key="field")
    # The internal message list should contain one Message instance
    assert len(err._messages) == 1
    msg = err._messages[0]
    assert msg.text == "Invalid input"
    assert msg.code == "invalid"
    assert msg.key == "field"
    # __str__ should return the message text when no index
    assert str(err) == "Invalid input"
    # __repr__ should include text and code
    assert repr(err) == "BaseError(text='Invalid input', code='invalid')"

def test_multiple_messages_and_dict_access():
    msgs = [
        Message(text="Missing field", code="required", key="username"),
        Message(text="Too short", code="min_length", key="password", index=["user", "password"]),
    ]
    err = BaseError(messages=msgs)
    # __len__ should count top-level keys in message dict
    assert len(err) == 2
    # __iter__ should iterate over top-level keys
    assert set(iter(err)) == {"username", "user"}
    # Access by key should return either string or nested dict
    assert err["username"] == "Missing field"
    assert isinstance(err["user"], dict)
    assert err["user"]["password"] == "Too short"
    # messages() should return the original list
    assert err.messages() == msgs

def test_messages_add_prefix_and_equality():
    msgs = [
        Message(text="Invalid email", code="email", key="email"),
        Message(text="Too long", code="max_length", key="bio", index=["profile", "bio"]),
    ]
    err1 = BaseError(messages=msgs)
    # Add prefix to all messages
    prefixed = err1.messages(add_prefix="user")
    # Each returned Message should have the prefix added to its index
    assert all(msg.index[0] == "user" for msg in prefixed)
    # The original error should remain unchanged
    assert err1.messages() == msgs
    # Equality should compare message lists
    err2 = BaseError(messages=msgs.copy())
    assert err1 == err2
    # Different order should not be equal
    err3 = BaseError(messages=[msgs[1], msgs[0]])
    assert err1 != err3
