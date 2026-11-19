import pytest
from typesystem.fields import Integer, String, NO_DEFAULT
from typesystem.json_schema import get_standard_properties

def test_default_included_for_field_with_default():
    # Integer field with a default value
    field = Integer(default=42)
    props = get_standard_properties(field)
    assert "default" in props
    assert props["default"] == 42

def test_no_default_for_field_without_default():
    # String field without a default value
    field = String()
    props = get_standard_properties(field)
    assert "default" not in props

def test_default_is_none_when_explicitly_set_to_none():
    # Integer field explicitly set to default None
    field = Integer(default=None)
    props = get_standard_properties(field)
    # has_default should consider None as a valid default
    assert "default" in props
    assert props["default"] is None
