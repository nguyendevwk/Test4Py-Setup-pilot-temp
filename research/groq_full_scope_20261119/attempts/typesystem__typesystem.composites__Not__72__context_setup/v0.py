import pytest
from typesystem.composites import Not
from typesystem.fields import Int, Any


def test_not_accepts_int_value():
    """Not(Int()) should raise a validation error when an int is provided."""
    field = Not(Int())
    with pytest.raises(field.validation_error.__class__) as excinfo:
        field.validate(42)
    assert "negated" in str(excinfo.value)


def test_not_accepts_non_int_value():
    """Not(Int()) should accept non-int values and return them unchanged."""
    field = Not(Int())
    result = field.validate("hello")
    assert result == "hello"


def test_not_disallows_allow_null_kwarg():
    """Constructing Not with allow_null kwarg should raise an AssertionError."""
    with pytest.raises(AssertionError):
        Not(Int(), allow_null=True)
