import pytest
from typesystem.composites import Not
from typesystem.fields import Int, ValidationError


def test_not_accepts_int():
    """Not(Int) should raise a validation error when an int is provided."""
    field = Not(Int())
    with pytest.raises(ValidationError) as excinfo:
        field.validate(42)
    assert "negated" in str(excinfo.value)


def test_not_rejects_non_int():
    """Not(Int) should accept non-int values."""
    field = Not(Int())
    # Non-int values should pass validation
    assert field.validate("hello") == "hello"
    assert field.validate(3.14) == 3.14
    assert field.validate(None) is None


def test_not_constructor_assertion():
    """Passing allow_null to Not should raise an AssertionError."""
    with pytest.raises(AssertionError):
        Not(Int(), allow_null=True)
