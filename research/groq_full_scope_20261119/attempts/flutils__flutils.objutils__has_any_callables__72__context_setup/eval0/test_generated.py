import pytest
from flutils.objutils import has_any_callables, has_any_attrs

def test_has_any_callables_true_for_callable_attribute():
    # A dict has a callable method 'get'
    assert has_any_callables(dict(), 'get', 'nonexistent') is True
    # A custom object with a callable attribute
    class C:
        def method(self): pass
    obj = C()
    assert has_any_callables(obj, 'method') is True

def test_has_any_callables_false_when_no_callable_or_attr():
    # A dict has no attribute 'foo' and 'bar' is not callable
    class Dummy:
        foo = 42
    dummy = Dummy()
    assert has_any_callables(dummy, 'foo', 'bar') is False
    # Empty list has no callable attributes
    assert has_any_callables([], 'append', 'pop', 'nonexistent') is False

def test_has_any_callables_raises_type_error_on_non_string_attrs():
    # Passing a non-string attribute name should raise a TypeError
    with pytest.raises(TypeError):
        has_any_callables(dict(), 123, 'get')
