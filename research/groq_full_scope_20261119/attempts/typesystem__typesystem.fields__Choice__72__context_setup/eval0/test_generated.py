import pytest
from typesystem.fields import Choice
from typesystem.base import ValidationError

def test_choice_validates_known_value():
    """A value that is in the choice list should pass validation unchanged."""
    field = Choice(choices=["red", "green", "blue"])
    result = field.validate("green")
    assert result == "green"

def test_choice_allows_null_when_empty_and_allow_null():
    """An empty string should be coerced to None when allow_null is True and coerce_types is True."""
    field = Choice(choices=["red", "green"], allow_null=True, coerce_types=True)
    # Empty string is not in the choices, but should be treated as null
    result = field.validate("")
    assert result is None

def test_choice_raises_error_for_invalid_choice():
    """A value not in the choice list should raise a ValidationError with code 'choice'."""
    field = Choice(choices=[("red", "Red"), ("green", "Green")])
    with pytest.raises(ValidationError) as excinfo:
        field.validate("blue")
    assert excinfo.value.code == "choice"
    assert "Not a valid choice." in str(excinfo.value)
