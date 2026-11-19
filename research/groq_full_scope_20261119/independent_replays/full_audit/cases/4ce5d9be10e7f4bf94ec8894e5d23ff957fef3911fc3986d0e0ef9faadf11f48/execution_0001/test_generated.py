import pytest
from typesystem.fields import Const
from typesystem.base import ValidationError

def test_const_matches_value():
    """When the value equals the constant, validate returns the value unchanged."""
    field = Const(const=42)
    result = field.validate(42)
    assert result == 42

def test_const_none_error():
    """If the constant is None, a non‑null value raises a ValidationError with the correct message."""
    field = Const(const=None)
    with pytest.raises(ValidationError) as excinfo:
        field.validate(1)
    assert "Must be null." in str(excinfo.value)

def test_const_mismatch_error():
    """A mismatched value raises a ValidationError with the constant in the message."""
    field = Const(const="hello")
    with pytest.raises(ValidationError) as excinfo:
        field.validate("world")
    assert "Must be the value 'hello'." in str(excinfo.value)
