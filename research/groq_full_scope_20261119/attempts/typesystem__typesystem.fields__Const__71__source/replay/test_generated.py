import pytest
from typesystem.fields import Const
from typesystem import ValidationError

def test_const_matches_value():
    """Normal case: value equals the constant."""
    field = Const(const=42)
    result = field.validate(42)
    assert result == 42

def test_const_with_none_value():
    """Boundary case: constant is None and value is None."""
    field = Const(const=None)
    result = field.validate(None)
    assert result is None

def test_const_raises_on_mismatch():
    """Error case: value does not match the constant."""
    field = Const(const="hello")
    with pytest.raises(ValidationError) as excinfo:
        field.validate("world")
    assert "Must be the value 'hello'." in str(excinfo.value)
