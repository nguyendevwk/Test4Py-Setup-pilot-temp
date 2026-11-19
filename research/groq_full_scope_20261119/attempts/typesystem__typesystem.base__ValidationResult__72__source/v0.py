import pytest
from typesystem.base import ValidationResult, ValidationError


def test_validation_result_success_and_bool():
    """A ValidationResult with a value is truthy and exposes the value."""
    vr = ValidationResult(value=42)
    # The object should be truthy because error is None
    assert bool(vr) is True
    # The value attribute should be accessible
    assert vr.value == 42
    # The error attribute should be None
    assert vr.error is None
    # Iteration yields value then error
    assert list(vr) == [42, None]
    # Representation should include the value
    assert repr(vr) == "ValidationResult(value=42)"


def test_validation_result_error_and_repr():
    """A ValidationResult with an error is falsy and exposes the error."""
    err = ValidationError("invalid data")
    vr = ValidationResult(error=err)
    # The object should be falsy because error is set
    assert bool(vr) is False
    # The value attribute should be None
    assert vr.value is None
    # The error attribute should be the ValidationError instance
    assert vr.error is err
    # Iteration yields None then the error
    assert list(vr) == [None, err]
    # Representation should include the error
    assert repr(vr) == f"ValidationResult(error={err!r})"


def test_validation_result_assertion_on_both_fields():
    """Providing both value and error raises an AssertionError."""
    with pytest.raises(AssertionError):
        ValidationResult(value=1, error=ValidationError("oops"))
