import pytest
from flutils.objutils import has_any_callables


def test_callable_attribute_returns_true():
    """When the object has a callable attribute among the requested ones,
    the function should return True."""
    class Dummy:
        def method(self):
            return 42

    assert has_any_callables(Dummy(), "method", "nonexistent") is True
    # Ensure that the function does not falsely return True for non-callable attrs
    assert has_any_callables(Dummy(), "nonexistent") is False


def test_non_callable_attribute_returns_false():
    """If the object has the attribute but it is not callable, the function
    should return False even if other attributes are callable."""
    class Dummy:
        value = 10  # non-callable attribute

    # 'value' exists but is not callable; 'method' does not exist
    assert has_any_callables(Dummy(), "value", "method") is False


def test_no_matching_attributes_returns_false():
    """When none of the requested attributes exist on the object, the
    function should return False."""
    class Dummy:
        pass

    assert has_any_callables(Dummy(), "missing1", "missing2") is False
