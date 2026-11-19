import pytest
from flutils.objutils import has_any_attrs


def test_has_any_attrs_true():
    """When at least one attribute exists, the function returns True."""
    class Dummy:
        def foo(self): ...
        bar = 42

    dummy = Dummy()
    # 'foo' is a method, 'bar' is a class attribute, 'baz' does not exist
    assert has_any_attrs(dummy, "baz", "foo", "nonexistent") is True
    # Only checking for a non-existent attribute should return False
    assert has_any_attrs(dummy, "nonexistent") is False


def test_has_any_attrs_boundary_no_attrs():
    """If no attribute names are supplied, the function should return False."""
    obj = {}
    # No attrs passed: should not raise and return False
    assert has_any_attrs(obj) is False


def test_has_any_attrs_invalid_attr_type():
    """Passing a non-string attribute name should raise a TypeError."""
    obj = {}
    with pytest.raises(TypeError):
        has_any_attrs(obj, 123)  # non-string attribute name
