import pytest
from flutils.objutils import has_attrs

def test_has_attrs_true_for_existing_methods():
    """has_attrs should return True when all requested attributes exist."""
    d = {}
    # dict has these methods
    assert has_attrs(d, "get", "keys", "items", "values") is True

def test_has_attrs_false_for_missing_attribute():
    """has_attrs should return False if any requested attribute is missing."""
    lst = [1, 2, 3]
    # list does not have 'keys' attribute
    assert has_attrs(lst, "append", "keys") is False

def test_has_attrs_true_when_no_attributes_specified():
    """has_attrs should return True when no attributes are provided."""
    obj = object()
    assert has_attrs(obj) is True
