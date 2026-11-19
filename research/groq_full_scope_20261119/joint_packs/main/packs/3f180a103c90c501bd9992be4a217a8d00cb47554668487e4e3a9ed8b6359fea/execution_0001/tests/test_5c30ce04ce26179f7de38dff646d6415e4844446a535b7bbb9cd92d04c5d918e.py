import pytest
from flutils.objutils import has_attrs


def test_has_attrs_with_builtin_and_empty_attrs():
    """has_attrs should return True for an empty attribute list."""
    # Built-in dict has many attributes; empty list should always be True
    assert has_attrs(dict(),) is True
    # Empty attrs on any object should be True
    class Dummy: pass
    dummy = Dummy()
    assert has_attrs(dummy) is True


def test_has_attrs_with_missing_and_present_attributes():
    """has_attrs should correctly detect missing attributes."""
    class Sample:
        def method_a(self): ...
        def method_b(self): ...

    sample = Sample()
    # All present
    assert has_attrs(sample, "method_a", "method_b") is True
    # One missing
    assert has_attrs(sample, "method_a", "non_existent") is False
    # All missing
    assert has_attrs(sample, "x", "y") is False


def test_has_attrs_with_special_and_dunder_attributes():
    """has_attrs should work with dunder and special attributes."""
    lst = [1, 2, 3]
    # List has __len__ and append
    assert has_attrs(lst, "__len__", "append") is True
    # Missing dunder
    assert has_attrs(lst, "__missing__") is False
    # Mixed presence
    assert has_attrs(lst, "__len__", "__missing__") is False
