import pytest
from typesystem.fields import Const
from typesystem.base import ValidationError

def test_const_valid_value():
    """When the value matches the constant, validate returns the value unchanged."""
    field = Const(const=42)
    result = field.validate(42)
    assert result == 42, "validate should return the matching value"

def test_const_invalid_value_and_error_message():
    """When the value does not match the constant, a ValidationError is raised with the correct message."""
    field = Const(const="hello")
    with pytest.raises(ValidationError) as excinfo:
        field.validate("world")
    # The error message should include the expected constant value
    assert "hello" in str(excinfo.value), "Error message should mention the expected constant"

def test_const_none_and_allow_null_assertion():
    """Const with None as the constant should raise a ValidationError when a non‑None value is provided.
    Passing allow_null in kwargs should raise an AssertionError during construction."""
    # Test that a non‑None value raises ValidationError
    field_none = Const(const=None)
    with pytest.raises(ValidationError) as excinfo:
        field_none.validate("not null")
    assert "Must be null." in str(excinfo.value), "Error message should indicate null requirement"

    # Test that providing allow_null in kwargs triggers an AssertionError
    with pytest.raises(AssertionError):
        Const(const=1, allow_null=True)
