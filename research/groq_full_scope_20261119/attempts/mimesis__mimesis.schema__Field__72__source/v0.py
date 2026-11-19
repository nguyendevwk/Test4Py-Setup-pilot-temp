import inspect
import pytest
from mimesis.schema import Field
from mimesis.exceptions import FieldNameError

def test_field_call_signature():
    """Field.__call__ should accept name, key, and arbitrary kwargs."""
    sig = inspect.signature(Field.__call__)
    params = sig.parameters
    assert "name" in params
    assert "key" in params
    # kwargs should be accepted
    assert params["kwargs"].kind == inspect.Parameter.VAR_KEYWORD

def test_field_call_without_name_raises():
    """Calling Field without a name should raise FieldNameError."""
    field = Field()
    with pytest.raises(FieldNameError):
        field()

def test_field_call_with_known_provider_returns_value(tmp_path):
    """Calling Field with a known provider name should return a non‑None value."""
    field = Field()
    # Use a common provider name that exists in mimesis (e.g., 'name')
    value = field("name")
    assert value is not None
    # The value should be a string (typical for name provider)
    assert isinstance(value, str)
