import pytest
from typesystem.base import ValidationError, Message


def test_validation_error_behavior():
    # Canonical single-message construction
    msg = Message(text="Field is required", code="required", index=["field_a"])
    err = ValidationError(messages=[msg])
    assert len(err.messages()) == 1
    m = err.messages()[0]
    assert isinstance(m, Message)
    assert m.text == "Field is required"
    assert m.code == "required"
    assert m.index == ["field_a"]

    # Dict-like iteration yields top-level keys
    assert list(err) == ["field_a"]

    # add_prefix prepends to each message index
    prefixed = err.messages(add_prefix="parent")
    assert len(prefixed) == 1
    assert prefixed[0].index == ["parent", "field_a"]
    assert prefixed[0].text == "Field is required"

    # Single-message initialization via keyword arguments
    err2 = ValidationError(text="Missing", code="missing", key="username")
    assert len(err2.messages()) == 1
    m2 = err2.messages()[0]
    assert m2.text == "Missing"
    assert m2.code == "missing"
    # The key is used as the index for the message
    assert m2.index == ["username"]

    # Invalid construction: both text and messages provided
    with pytest.raises(AssertionError):
        ValidationError(text="x", messages=[msg])
