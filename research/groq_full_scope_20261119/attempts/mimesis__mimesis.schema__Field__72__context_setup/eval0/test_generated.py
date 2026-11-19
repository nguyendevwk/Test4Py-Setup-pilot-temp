import pytest
from mimesis.schema import Field
from mimesis.exceptions import FieldNameError, FieldError
from mimesis.types import Key


def test_field_generates_value_for_valid_name():
    """Field should return a non‑empty value for a known provider name."""
    field = Field()
    # "username" is a valid provider name in the default locale
    value = field(name="username")
    assert isinstance(value, str)
    assert value != ""


def test_field_raises_error_for_invalid_name():
    """Field should raise FieldNameError when the provider name is unknown."""
    field = Field()
    with pytest.raises(FieldNameError):
        field(name="nonexistent_provider")


def test_field_uses_custom_key_function():
    """Field should accept a custom key function and use it to generate the value."""
    field = Field()
    # Define a key function that always returns the string "fixed_value"
    key_func: Key = lambda: "fixed_value"
    result = field(name="username", key=key_func)
    assert result == "fixed_value"
