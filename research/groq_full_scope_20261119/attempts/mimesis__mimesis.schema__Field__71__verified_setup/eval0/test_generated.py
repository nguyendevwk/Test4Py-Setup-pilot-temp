import pytest
from mimesis.schema import Field
from mimesis.exceptions import FieldNameError


def test_field_generates_non_empty_value():
    """Field should return a non‑empty value for a known provider name."""
    f = Field(seed=0)
    value = f(name="username")
    assert isinstance(value, str)
    assert value != ""


def test_field_raises_on_invalid_name():
    """Calling Field with an unknown provider name should raise FieldNameError."""
    f = Field(seed=0)
    with pytest.raises(FieldNameError):
        f(name="nonexistent_provider")


def test_field_uses_key_function():
    """Field should return the result of the key function when provided."""
    f = Field(seed=0)
    result = f(name="username", key=lambda: "fixed_value")
    assert result == "fixed_value"
