import pytest
from typesystem.fields import Choice
from typesystem import ValidationError

def test_choice_valid_value():
    """A value that is in the list of choices should pass validation unchanged."""
    field = Choice(choices=["a", "b", "c"])
    result = field.validate("b")
    assert result == "b"

def test_choice_empty_string_with_allow_null_and_coerce():
    """An empty string should be coerced to None when allow_null and coerce_types are True."""
    field = Choice(choices=["a", "b"], allow_null=True, coerce_types=True)
    result = field.validate("")
    assert result is None

def test_choice_invalid_value_raises_error():
    """Providing a value not in the choices should raise a ValidationError with the correct message."""
    field = Choice(choices=["x", "y"])
    with pytest.raises(ValidationError) as excinfo:
        field.validate("z")
    assert "Not a valid choice." in str(excinfo.value)
