import pytest
from typesystem.fields import Integer, String, Field

from typesystem.json_schema import get_standard_properties


def test_get_standard_properties_with_default():
    """When a field has a default value, the returned dict contains it."""
    field = Integer(default=42)
    props = get_standard_properties(field)
    assert isinstance(props, dict)
    assert "default" in props
    assert props["default"] == 42


def test_get_standard_properties_without_default():
    """When a field has no default, the returned dict is empty."""
    field = String()
    props = get_standard_properties(field)
    assert isinstance(props, dict)
    assert props == {}


def test_get_standard_properties_invalid_input():
    """Passing an object that is not a Field should raise an AttributeError."""
    with pytest.raises(AttributeError):
        get_standard_properties(None)
