import pytest
from mimesis.schema import Field
from mimesis.exceptions import FieldNameError, FieldError
from mimesis.keys import _call_key_func
from mimesis.types import Key


def test_field_generates_value_for_valid_name(tmp_path):
    """Field should return a non‑empty string for a known provider name."""
    field = Field()
    # Use a provider that is guaranteed to exist in the default locale
    value = field("username")
    assert isinstance(value, str)
    assert value != ""  # non‑empty
    # The value should be deterministic for the same seed
    field2 = Field(seed=123)
    value2 = field2("username")
    assert isinstance(value2, str)
    assert value2 != ""


def test_field_raises_on_invalid_name():
    """Calling Field with an unknown provider name should raise FieldNameError."""
    field = Field()
    with pytest.raises(FieldNameError):
        field("nonexistent_provider")


def test_field_uses_key_function(tmp_path):
    """Field should accept a key function and return its result."""
    field = Field()
    # Define a key function that returns a fixed value
    def key_func(provider, name, **kwargs):
        return f"fixed-{name}"
    result = field("email", key=key_func)
    assert result == "fixed-email"
    # Ensure that the key function receives the provider instance and name
    captured = {}
    def key_func_capture(provider, name, **kwargs):
        captured["provider"] = provider
        captured["name"] = name
        return "captured"
    result2 = field("phone", key=key_func_capture)
    assert result2 == "captured"
    assert isinstance(captured["provider"], type(field))
    assert captured["name"] == "phone"
