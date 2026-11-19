import pytest
from typesystem.base import ValidationError, Message

def test_validation_error_behavior():
    # Canonical single-message construction
    msg = Message(text="Field is required", code="required", index=["field_a"])
    err = ValidationError(messages=[msg])
    assert len(err.messages()) == 1
    m = err.messages()[0]
    assert m.text == "Field is required"
    assert m.code == "required"
    assert m.index == ["field_a"]
    # Mapping view
    assert dict(err) == {"field_a": "Field is required"}
    # Prefixing messages
    prefixed = err.messages(add_prefix="parent")
    assert len(prefixed) == 1
    pm = prefixed[0]
    assert pm.index == ["parent", "field_a"]
    assert pm.text == "Field is required"
    # Iteration yields top-level keys
    assert list(err) == ["field_a"]

    # Single-text construction
    err2 = ValidationError(text="Missing", code="missing", key="username")
    m2 = err2.messages()[0]
    assert m2.text == "Missing"
    assert m2.code == "missing"
    assert m2.index == ["username"]
    # Mapping view for non-empty index
    assert dict(err2) == {"username": "Missing"}
