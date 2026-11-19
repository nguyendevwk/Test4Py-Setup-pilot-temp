import pytest
from flutils.objutils import has_attrs

def test_has_attrs_all_present(tmp_path):
    """All requested attributes exist on the object."""
    d = {}
    # dict has get, keys, items, values
    assert has_attrs(d, "get", "keys", "items", "values") is True
    # list has __len__ and __iter__
    l = [1, 2, 3]
    assert has_attrs(l, "__len__", "__iter__") is True

def test_has_attrs_missing_attribute(tmp_path):
    """Return False when at least one attribute is missing."""
    d = {}
    # dict does not have 'nonexistent'
    assert has_attrs(d, "get", "nonexistent") is False
    # list does not have 'append' attribute on a tuple
    t = (1, 2)
    assert has_attrs(t, "append") is False

def test_has_attrs_invalid_attribute_name(tmp_path):
    """Passing a non-string attribute name raises TypeError."""
    with pytest.raises(TypeError):
        has_attrs({}, 123)  # non-string attribute name
