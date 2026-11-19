import pytest
from flutils.objutils import has_any_attrs

def test_has_any_attrs_true():
    """When at least one attribute exists, the function returns True."""
    class Dummy:
        def foo(self): pass
    dummy = Dummy()
    # 'foo' exists, 'bar' does not
    assert has_any_attrs(dummy, "foo", "bar") is True

def test_has_any_attrs_false():
    """When none of the specified attributes exist, the function returns False."""
    class Dummy:
        def foo(self): pass
    dummy = Dummy()
    # 'bar' and 'baz' do not exist
    assert has_any_attrs(dummy, "bar", "baz") is False

def test_has_any_attrs_no_attrs():
    """When no attribute names are provided, the function returns False."""
    dummy = {}
    # No attributes passed to check
    assert has_any_attrs(dummy) is False
