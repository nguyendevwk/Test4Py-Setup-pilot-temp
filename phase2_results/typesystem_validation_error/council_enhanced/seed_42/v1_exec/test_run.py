import pytest
from typesystem.base import ValidationError, Message


def test_validation_error_messages_and_prefix_and_initialization():
    # Canonical single-message construction
    msg = Message(text="Field is required", code="required", index=["field_a"])
    err = ValidationError(messages=[msg])

    # Basic message retrieval
    messages = err.messages()
    assert len(messages) == 1
    assert messages[0].text == "Field is required"
    assert messages[0].code == "required"
    assert messages[0].index == ["field_a"]

    # Prefixing messages for nested contexts
    prefixed = err.messages(add_prefix="parent")
    assert len(prefixed) == 1
    assert prefixed[0].index == ["parent", "field_a"]
    assert prefixed[0].text == "Field is required"

    # Single-message constructor via text/code
    err_single = ValidationError(text="Missing", code="missing")
    single_messages = err_single.messages()
    assert len(single_messages) == 1
    assert single_messages[0].text == "Missing"
    assert single_messages[0].code == "missing"
    # Index defaults to empty list when not provided
    assert single_messages[0].index == []

    # Mixing text and messages should raise an assertion error
    with pytest.raises(AssertionError):
        ValidationError(text="Error", messages=[msg])
