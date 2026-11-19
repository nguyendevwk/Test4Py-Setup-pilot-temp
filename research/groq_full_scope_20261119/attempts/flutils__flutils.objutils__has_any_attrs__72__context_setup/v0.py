import pytest
from flutils.objutils import has_any_attrs


def test_has_any_attrs_returns_true_when_any_attribute_exists():
    """The function should return True if at least one of the requested attributes exists."""
    class Dummy:
        def foo(self): ...
        bar = 42

    dummy = Dummy()
    # 'foo' is a method, 'bar' is a class attribute, 'baz' does not exist
    assert has_any_attrs(dummy, "baz", "foo") is True
    assert has_any_attrs(dummy, "baz", "bar") is True
    # Order does not matter; the first existing attribute triggers True
    assert has_any_attrs(dummy, "foo", "bar", "baz") is True


def test_has_any_attrs_returns_false_when_no_attributes_exist():
    """The function should return False if none of the requested attributes exist."""
    class Dummy:
        pass

    dummy = Dummy()
    # No attributes are present
    assert has_any_attrs(dummy, "nonexistent") is False
    # Even if multiple non-existent attributes are provided
    assert has_any_attrs(dummy, "a", "b", "c") is False
    # Passing no attributes should also return False
    assert has_any_attrs(dummy) is False


def test_has_any_attrs_handles_non_string_attribute_names_and_none_values():
    """The function should not raise errors when attribute names are non‑string or when attributes are None."""
    class Dummy:
        attr = None

    dummy = Dummy()
    # Passing a non‑string attribute name (int) should still work because hasattr accepts any hashable
    assert has_any_attrs(dummy, 123, "attr") is True
    # Passing a string that does not exist should return False
    assert has_any_attrs(dummy, "missing") is False
    # Attribute exists but its value is None; hasattr still returns True
    assert has_any_attrs(dummy, "attr") is True
