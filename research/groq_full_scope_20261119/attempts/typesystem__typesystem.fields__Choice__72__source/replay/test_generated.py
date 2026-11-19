import pytest
from typesystem.fields import Choice
from typesystem.base import ValidationError

def test_valid_choice_returns_value():
    field = Choice(choices=["a", "b", "c"])
    result = field.validate("b")
    assert result == "b"

def test_empty_string_with_allow_null_and_coerce_types_returns_none():
    field = Choice(choices=["a", "b"], allow_null=True, coerce_types=True)
    result = field.validate("")
    assert result is None

def test_invalid_choice_raises_validation_error():
    field = Choice(choices=["a", "b"])
    with pytest.raises(ValidationError) as excinfo:
        field.validate("c")
    assert "Not a valid choice." in str(excinfo.value)
