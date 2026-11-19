import pytest
from typesystem.base import ValidationResult


def test_success_value_and_iteration():
    """A ValidationResult with a value should iterate over the value and None."""
    vr = ValidationResult(value="ok")
    # Iteration yields value then error (None)
    iterated = list(vr)
    assert iterated == ["ok", None]
    # Boolean context should be True when no error
    assert bool(vr) is True
    # Representation should include the value
    assert repr(vr) == "ValidationResult(value='ok')"


def test_error_and_iteration():
    """A ValidationResult with an error should iterate over None and the error."""
    err = ValueError("invalid")
    vr = ValidationResult(error=err)
    # Iteration yields None then the error
    iterated = list(vr)
    assert iterated == [None, err]
    # Boolean context should be False when an error is present
    assert bool(vr) is False
    # Representation should include the error
    assert repr(vr) == f"ValidationResult(error={err!r})"


def test_assertion_on_invalid_initialization():
    """Initializing with both value and error should raise an AssertionError."""
    with pytest.raises(AssertionError):
        ValidationResult(value="data", error=RuntimeError("oops"))
