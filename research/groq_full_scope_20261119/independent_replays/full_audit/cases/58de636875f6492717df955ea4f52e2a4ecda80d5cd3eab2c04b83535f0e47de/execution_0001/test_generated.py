import pytest
from typesystem.fields import Any
from typesystem.base import ValidationResult

def test_any_validate_returns_same_value():
    """Any.validate should return the value unchanged for any input."""
    field = Any()
    for value in [42, "hello", [1, 2, 3], {"a": 1}, None, 3.14, True]:
        assert field.validate(value) is value

def test_any_validate_or_error_no_error():
    """validate_or_error should never produce an error for Any."""
    field = Any()
    for value in [0, "", [], {}, None, 1.0, False]:
        result: ValidationResult = field.validate_or_error(value)
        assert result.error is None
        assert result.value is value

def test_any_field_has_no_specific_errors():
    """Any field should not define any error messages."""
    field = Any()
    # The Any class inherits errors from Field, which is empty.
    assert getattr(field, "errors", {}) == {}
