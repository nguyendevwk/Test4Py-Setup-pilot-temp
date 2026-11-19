import pytest
from typesystem.fields import Any

def test_any_validate_returns_same_value():
    """Any.validate should return the value unchanged for any input."""
    field = Any()
    for value in [42, "hello", 3.14, None, {"a": 1}, [1, 2, 3]]:
        assert field.validate(value) is value

def test_any_validate_or_error_no_error():
    """validate_or_error should never produce an error for Any."""
    field = Any()
    for value in [0, "", False, [], {}, None]:
        result = field.validate_or_error(value)
        assert result.error is None
        assert result.value is value

def test_any_has_default_behavior():
    """Any should correctly report default presence and value."""
    # No default provided
    field_no_default = Any()
    assert not field_no_default.has_default()
    assert field_no_default.get_default_value() is None

    # Default provided
    field_with_default = Any(default=123)
    assert field_with_default.has_default()
    assert field_with_default.get_default_value() == 123
