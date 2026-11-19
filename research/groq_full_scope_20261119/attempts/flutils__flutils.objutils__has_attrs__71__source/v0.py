import pytest
from flutils.objutils import has_attrs

def test_has_attrs_all_present():
    """All requested attributes exist on the object."""
    obj = {'a': 1}
    # dict has get, keys, items, values
    assert has_attrs(obj, 'get', 'keys', 'items', 'values') is True

def test_has_attrs_missing_attribute():
    """Return False when at least one attribute is missing."""
    obj = [1, 2, 3]
    # list has append but not pop
    assert has_attrs(obj, 'append', 'pop') is False

def test_has_attrs_no_attributes_specified():
    """When no attributes are provided, the function should return True."""
    obj = object()
    assert has_attrs(obj) is True
