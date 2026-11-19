import pytest
from flutils.objutils import has_attrs

def test_has_attrs_basic():
    """Normal case: object has all requested attributes."""
    d = {}
    # dict has get, keys, items, values
    assert has_attrs(d, "get", "keys", "items", "values") is True
    # missing attribute
    assert has_attrs(d, "get", "missing") is False

def test_has_attrs_empty_and_multiple():
    """Boundary case: no attributes requested and multiple attributes."""
    # Empty attrs should return True
    assert has_attrs(1) is True
    # Multiple attributes on a custom object
    class C:
        a = 1
        b = 2
    c = C()
    assert has_attrs(c, "a", "b") is True
    assert has_attrs(c, "a", "c") is False

def test_has_attrs_invalid_attr_type():
    """Error case: non-string attribute name raises TypeError."""
    with pytest.raises(TypeError):
        has_attrs({}, 123)  # non-string attribute name
