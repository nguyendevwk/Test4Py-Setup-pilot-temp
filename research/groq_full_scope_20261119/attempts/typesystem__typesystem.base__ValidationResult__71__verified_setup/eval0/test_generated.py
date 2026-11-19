import pytest
from typesystem.base import ValidationResult, ValidationError

def test_validation_result_value_and_error_exclusivity():
    """A ValidationResult must contain either a value or an error, never both."""
    vr = ValidationResult(value=42)
    assert vr.value == 42
    assert vr.error is None
    assert bool(vr) is True
    with pytest.raises(AssertionError):
        ValidationResult(value=1, error=ValidationError("msg"))

def test_validation_result_error_representation_and_iteration():
    """When an error is present, the object should expose it correctly and iterate properly."""
    err = ValidationError("invalid data")
    vr = ValidationResult(error=err)
    assert vr.value is None
    assert vr.error is err
    assert bool(vr) is False
    # Iteration yields value then error
    assert list(vr) == [None, err]
    # Representation should include the error
    assert repr(vr) == f"ValidationResult(error={err!r})"

def test_validation_result_repr_with_value_and_bool_behavior():
    """Representation should reflect the stored value and bool should be True when no error."""
    vr = ValidationResult(value={"a": 1})
    assert repr(vr) == f"ValidationResult(value={{'a': 1}})"
    assert bool(vr) is True
    # Ensure that accessing error on a successful result raises AttributeError
    with pytest.raises(AttributeError):
        _ = vr.error.__dict__
