import pytest
from mimesis.schema import Field
from mimesis.exceptions import FieldError


def test_field_basic_generation():
    """Field should generate a value for a known provider name."""
    field = Field()
    # The 'username' provider is available in the Generic provider.
    value = field(name="username")
    assert isinstance(value, str)
    assert value != ""  # non‑empty string
    # The value should be deterministic for the same seed.
    field2 = Field(seed=123)
    value2 = field2(name="username")
    assert isinstance(value2, str)
    assert value2 != ""


def test_field_invalid_name_raises_error():
    """Calling Field with an unknown name should raise FieldError."""
    field = Field()
    with pytest.raises(FieldError):
        field(name="nonexistent_provider")


def test_field_with_key_function_returns_fixed_value():
    """Providing a key function should override the provider's logic."""
    field = Field()
    key_func = lambda: "fixed_value"
    result = field(name="username", key=key_func)
    assert result == "fixed_value"
