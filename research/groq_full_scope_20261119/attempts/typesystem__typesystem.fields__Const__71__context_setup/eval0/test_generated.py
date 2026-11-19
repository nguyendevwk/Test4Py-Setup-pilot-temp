import pytest
from typesystem.fields import Const
from typesystem.base import ValidationError

def test_const_matches_value():
    """Const should accept the exact value and return it unchanged."""
    field = Const(const=42)
    result = field.validate(42)
    assert result == 42

def test_const_rejects_different_value():
    """Const should raise ValidationError when value differs."""
    field = Const(const="hello")
    with pytest.raises(ValidationError) as excinfo:
        field.validate("world")
    # The error message should mention the expected value
    assert "hello" in str(excinfo.value)
    # The error code should be 'const'
    assert excinfo.value.code == "const"

def test_const_null_behavior():
    """Const should raise a specific error when the constant is None."""
    field = Const(const=None)
    with pytest.raises(ValidationError) as excinfo:
        field.validate(0)
    # The error message should indicate that only null is allowed
    assert "null" in str(excinfo.value)
    # The error code should be 'only_null'
    assert excinfo.value.code == "only_null"
