import pytest
from typesystem.composites import Not
from typesystem.fields import Int, String


def test_not_accepts_value_when_negated_fails():
    """Not should return the value when the negated field validation fails."""
    not_int = Not(Int())
    # Int validation fails for a string, so Not should return the string unchanged
    result = not_int.validate("not an int")
    assert result == "not an int"


def test_not_rejects_value_when_negated_passes():
    """Not should raise a validation error when the negated field validation succeeds."""
    not_int = Not(Int())
    with pytest.raises(Exception) as excinfo:
        not_int.validate(42)
    # The error message should contain the key 'negated'
    assert "negated" in str(excinfo.value)


def test_not_init_raises_on_allow_null():
    """Not's constructor should assert that 'allow_null' is not provided."""
    with pytest.raises(AssertionError):
        Not(Int(), allow_null=True)
