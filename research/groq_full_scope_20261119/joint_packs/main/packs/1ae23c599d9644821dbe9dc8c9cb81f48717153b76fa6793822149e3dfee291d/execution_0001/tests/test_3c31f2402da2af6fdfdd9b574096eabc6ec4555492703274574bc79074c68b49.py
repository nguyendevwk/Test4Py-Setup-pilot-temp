import pytest
from flutils.objutils import has_any_attrs

def test_has_any_attrs_detects_existing_attribute(tmp_path):
    """Object has one of the requested attributes."""
    class Dummy:
        def foo(self): pass
    obj = Dummy()
    # 'foo' exists, 'bar' does not
    assert has_any_attrs(obj, "foo", "bar") is True

def test_has_any_attrs_returns_false_when_none_exist(tmp_path):
    """No requested attributes are present."""
    class Dummy:
        def baz(self): pass
    obj = Dummy()
    # 'foo' and 'bar' do not exist
    assert has_any_attrs(obj, "foo", "bar") is False

def test_has_any_attrs_raises_type_error_for_non_string_attr(tmp_path):
    """Passing a non-string attribute name raises TypeError."""
    class Dummy:
        def foo(self): pass
    obj = Dummy()
    with pytest.raises(TypeError):
        # int is not a valid attribute name
        has_any_attrs(obj, 42)
