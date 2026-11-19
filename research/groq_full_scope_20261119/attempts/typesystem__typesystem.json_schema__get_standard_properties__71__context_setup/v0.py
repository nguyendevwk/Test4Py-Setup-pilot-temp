import pytest
from typesystem.fields import Integer, String, Field
from typesystem.json_schema import get_standard_properties

def test_get_standard_properties_with_default():
    """Field with a default value should return a dict containing that default."""
    field = Integer(default=42)
    result = get_standard_properties(field)
    assert isinstance(result, dict)
    assert result == {"default": 42}

def test_get_standard_properties_without_default():
    """Field without a default should return an empty dict."""
    field = String()
    result = get_standard_properties(field)
    assert isinstance(result, dict)
    assert result == {}

def test_get_standard_properties_invalid_input():
    """Passing an object that is not a Field should raise an AttributeError."""
    with pytest.raises(AttributeError):
        get_standard_properties("not a field")
