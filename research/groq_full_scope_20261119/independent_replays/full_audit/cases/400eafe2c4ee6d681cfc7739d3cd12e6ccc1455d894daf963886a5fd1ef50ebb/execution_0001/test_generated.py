import pytest
from typesystem.base import ValidationResult, ValidationError, Message


def test_validation_result_success_and_repr_and_bool():
    # Create a successful ValidationResult with a value
    vr = ValidationResult(value={"ok": True})
    # The value should be accessible and error should be None
    assert vr.value == {"ok": True}
    assert vr.error is None
    # Boolean conversion should be True
    assert bool(vr) is True
    # Representation should include the value
    assert repr(vr) == "ValidationResult(value={'ok': True})"
    # Iteration yields value then error (None)
    assert list(vr) == [{"ok": True}, None]


def test_validation_result_error_and_repr_and_bool():
    # Create a ValidationError with a single message
    err = ValidationError(text="Something went wrong", code="error_code")
    # Wrap it in a ValidationResult
    vr = ValidationResult(error=err)
    # Value should be None and error should be the ValidationError instance
    assert vr.value is None
    assert vr.error is err
    # Boolean conversion should be False
    assert bool(vr) is False
    # Representation should include the error
    assert repr(vr) == f"ValidationResult(error={err!r})"
    # Iteration yields None then the error
    assert list(vr) == [None, err]


def test_validation_result_assertion_on_both_parameters():
    # Providing both value and error should raise an AssertionError
    with pytest.raises(AssertionError):
        ValidationResult(value=1, error=ValidationError(text="err"))
