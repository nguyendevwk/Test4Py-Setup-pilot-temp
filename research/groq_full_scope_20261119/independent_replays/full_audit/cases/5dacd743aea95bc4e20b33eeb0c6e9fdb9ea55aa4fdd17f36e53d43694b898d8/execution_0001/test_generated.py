import pytest
from typesystem.fields import Integer, String, Field
from typesystem.json_schema import get_standard_properties

def test_get_standard_properties_with_default():
    # Create an Integer field with a default value
    field = Integer(default=42)
    props = get_standard_properties(field)
    # The returned dict should contain the default key with the correct value
    assert "default" in props
    assert props["default"] == 42

def test_get_standard_properties_without_default():
    # Create a String field without a default value
    field = String()
    props = get_standard_properties(field)
    # The returned dict should be empty because no default is set
    assert props == {}

def test_get_standard_properties_invalid_input():
    # Passing an object that is not a Field should raise an AttributeError
    class NotAField:
        pass
    with pytest.raises(AttributeError):
        get_standard_properties(NotAField())
