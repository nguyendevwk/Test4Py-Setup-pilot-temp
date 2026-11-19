import pytest
from typesystem.base import ValidationResult, ValidationError, Message


def test_validation_result_truthiness_and_iteration():
    # Successful validation: value present, error None
    vr_success = ValidationResult(value={"ok": True})
    assert bool(vr_success) is True
    assert vr_success.value == {"ok": True}
    assert vr_success.error is None
    # Iteration yields value then error
    assert list(iter(vr_success)) == [{"ok": True}, None]

    # Failure validation: error present, value None
    err = ValidationError(text="Invalid data")
    vr_fail = ValidationResult(error=err)
    assert bool(vr_fail) is False
    assert vr_fail.value is None
    assert vr_fail.error is err
    # Iteration yields value then error
    assert list(iter(vr_fail)) == [None, err]


def test_validation_result_repr_single_error():
    # Single error without index
    err = ValidationError(text="Missing field", code="required")
    vr = ValidationResult(error=err)
    # __repr__ should include text and code
    assert repr(vr) == "ValidationResult(error=ValidationError(text='Missing field', code='required'))"
    # __str__ of the error should be the message text
    assert str(err) == "Missing field"


def test_validation_result_repr_success_and_error_dict():
    # Successful result with complex value
    vr = ValidationResult(value={"a": 1, "b": 2})
    assert repr(vr) == "ValidationResult(value={'a': 1, 'b': 2})"

    # Error with multiple messages and nested indices
    msg1 = Message(text="First error", code="e1", index=["field1"])
    msg2 = Message(text="Second error", code="e2", index=["field2", 0])
    err = ValidationError(messages=[msg1, msg2])
    vr_err = ValidationResult(error=err)
    # __repr__ should show the list of messages
    expected_repr = (
        "ValidationResult(error=ValidationError(["
        "Message(text='First error', code='e1', index=['field1']), "
        "Message(text='Second error', code='e2', index=['field2', 0])"
        "]))"
    )
    assert repr(vr_err) == expected_repr
    # The error's dict representation should reflect nested structure
    assert dict(err) == {"field1": "First error", "field2": {0: "Second error"}}
