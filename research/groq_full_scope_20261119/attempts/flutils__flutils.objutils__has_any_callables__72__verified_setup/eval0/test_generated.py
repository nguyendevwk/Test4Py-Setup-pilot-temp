import pytest
from flutils.objutils import has_any_callables


def test_has_any_callables_with_callable_attrs():
    """Object has at least one callable attribute among the given names."""
    class Dummy:
        def method(self):  # callable
            pass

        attr = 42  # non-callable

    dummy = Dummy()
    # 'method' is callable, 'attr' is not; function should return True
    assert has_any_callables(dummy, "method", "attr") is True
    # If we ask for a non-existent attribute, still True because 'method' exists
    assert has_any_callables(dummy, "nonexistent", "method") is True
    # If we ask for only non-callable attributes, should be False
    assert has_any_callables(dummy, "attr") is False


def test_has_any_callables_no_attrs():
    """Calling with no attribute names should return False."""
    obj = object()
    # No attrs provided; function should return False
    assert has_any_callables(obj) is False
    # Even if the object has callable attributes, no attrs specified means no check
    class WithMethod:
        def foo(self): pass
    assert has_any_callables(WithMethod(),) is False


def test_has_any_callables_non_callable_attrs():
    """Attributes exist but are not callable; function should return False."""
    class NonCallable:
        value = 123  # not callable
        list_attr = [1, 2, 3]  # not callable

    nc = NonCallable()
    # All provided attributes are non-callable
    assert has_any_callables(nc, "value", "list_attr") is False
    # Mixed case: one callable, one non-callable
    class Mixed:
        def method(self): pass
        data = "text"
    mixed = Mixed()
    assert has_any_callables(mixed, "data", "method") is True
    # Attribute that exists but is not callable should not trigger True
    assert has_any_callables(mixed, "data") is False
