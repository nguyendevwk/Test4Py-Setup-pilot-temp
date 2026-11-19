import pytest
from typesystem.fields import Const
from typesystem.base import ValidationError

def test_const_matches_value():
    """The Const field should accept the exact value it was constructed with."""
    field = Const(const=42)
    # Valid value returns unchanged
    assert field.validate(42) == 42
    # Invalid value raises ValidationError with correct message
    with pytest.raises(ValidationError) as excinfo:
        field.validate(43)
    assert str(excinfo.value) == "Must be the value '42'."

def test_const_with_none_value():
    """When const is None, only None should be accepted."""
    field = Const(const=None)
    # None is accepted
    assert field.validate(None) is None
    # Any other value raises the 'only_null' error
    with pytest.raises(ValidationError) as excinfo:
        field.validate(0)
    assert str(excinfo.value) == "Must be null."

def test_const_error_message_formatting():
    """Error messages should interpolate the const value correctly."""
    field = Const(const="hello")
    with pytest.raises(ValidationError) as excinfo:
        field.validate("world")
    # The message should include the exact const value
    assert "hello" in str(excinfo.value)
    assert str(excinfo.value) == "Must be the value 'hello'."
