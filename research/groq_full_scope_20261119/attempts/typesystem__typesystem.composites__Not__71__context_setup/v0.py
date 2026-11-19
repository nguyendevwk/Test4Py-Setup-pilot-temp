import pytest
from typesystem.composites import Not
from typesystem.fields import Int

def test_not_accepts_matching_value():
    """Not should raise a validation error when the value matches the negated field."""
    not_int = Not(Int())
    with pytest.raises(Exception) as excinfo:
        not_int.validate(42)
    # The error message should contain the custom negated error text
    assert "Must not match." in str(excinfo.value)

def test_not_accepts_non_matching_value():
    """Not should accept values that do not match the negated field."""
    not_int = Not(Int())
    # A string does not match Int, so validation should succeed
    result = not_int.validate("hello")
    assert result == "hello"

def test_not_rejects_null_value():
    """Not should reject None values because allow_null is not permitted."""
    not_int = Not(Int())
    with pytest.raises(Exception) as excinfo:
        not_int.validate(None)
    assert "Must not match." in str(excinfo.value)
