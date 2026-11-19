import pytest
from typesystem.fields import Const
from typesystem import ValidationError

def test_const_matches_value():
    """Const should accept the exact value it was initialized with."""
    field = Const(42)
    assert field.validate(42) == 42

def test_const_rejects_different_value():
    """Const should raise ValidationError when value differs."""
    field = Const("hello")
    with pytest.raises(ValidationError) as excinfo:
        field.validate("world")
    # The error message should reference the expected constant
    assert "hello" in str(excinfo.value)

def test_const_null_behavior():
    """Const initialized with None should only accept None."""
    field = Const(None)
    assert field.validate(None) is None
    with pytest.raises(ValidationError) as excinfo:
        field.validate("not null")
    # The error message should indicate that only null is allowed
    assert "Must be null." in str(excinfo.value)
