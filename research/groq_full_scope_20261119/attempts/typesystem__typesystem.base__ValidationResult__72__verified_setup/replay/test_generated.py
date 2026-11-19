import pytest
from typesystem.base import ValidationResult

class DummyError(Exception):
    """Simple error type for testing."""
    pass

def test_validation_result_with_value():
    """ValidationResult should store a value and have no error."""
    vr = ValidationResult(value=42)
    assert vr.value == 42
    assert vr.error is None
    # Boolean context should be True when no error
    assert bool(vr) is True
    # Iteration yields value then error
    val, err = tuple(vr)
    assert val == 42
    assert err is None
    # Representation includes the value
    assert repr(vr) == "ValidationResult(value=42)"

def test_validation_result_with_error():
    """ValidationResult should store an error and no value."""
    err = DummyError("invalid data")
    vr = ValidationResult(error=err)
    assert vr.value is None
    assert vr.error is err
    # Boolean context should be False when error present
    assert bool(vr) is False
    # Iteration yields value then error
    val, err_out = tuple(vr)
    assert val is None
    assert err_out is err
    # Representation includes the error
    assert repr(vr) == f"ValidationResult(error={err!r})"

def test_validation_result_assertion_on_both():
    """Providing both value and error should raise an AssertionError."""
    with pytest.raises(AssertionError):
        ValidationResult(value=1, error=DummyError("oops"))
