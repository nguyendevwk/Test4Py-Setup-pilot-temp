import pytest
from typesystem.fields import Choice
from typesystem import ValidationError

def test_choice_valid_value():
    """A valid choice value passes validation unchanged."""
    field = Choice(choices=["a", "b", "c"])
    result = field.validate("b")
    assert result == "b"

def test_choice_empty_string_with_allow_null_and_coerce():
    """An empty string is coerced to None when allow_null and coerce_types are True."""
    field = Choice(choices=["a", "b"], allow_null=True, coerce_types=True)
    result = field.validate("")
    assert result is None

def test_choice_invalid_value_raises_error():
    """Providing a value not in the choices raises a ValidationError with the correct message."""
    field = Choice(choices=[("x", "X"), ("y", "Y")])
    with pytest.raises(ValidationError) as excinfo:
        field.validate("z")
    assert "Not a valid choice." in str(excinfo.value)
