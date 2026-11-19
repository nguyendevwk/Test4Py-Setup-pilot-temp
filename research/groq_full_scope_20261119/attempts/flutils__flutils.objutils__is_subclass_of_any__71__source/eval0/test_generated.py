import pytest
from flutils.objutils import is_subclass_of_any
from collections import UserList, deque, ValuesView, KeysView


def test_is_subclass_of_any_true_for_multiple_classes():
    """The function should return True when the object is a subclass of any provided class."""
    obj = dict(a=1, b=2).keys()  # KeysView instance
    assert is_subclass_of_any(obj, ValuesView, KeysView, UserList) is True
    # Also test with a deque instance against deque and list
    d = deque([1, 2, 3])
    assert is_subclass_of_any(d, list, deque) is True


def test_is_subclass_of_any_false_when_no_match():
    """The function should return False when the object is not a subclass of any provided class."""
    obj = UserList([1, 2, 3])  # UserList instance
    # Provide classes that do not match UserList
    assert is_subclass_of_any(obj, dict, list, tuple) is False
    # Also test with a plain int
    assert is_subclass_of_any(42, str, float, complex) is False


def test_is_subclass_of_any_empty_class_list_returns_false():
    """When no classes are provided, the function should return False."""
    obj = deque([1, 2, 3])
    assert is_subclass_of_any(obj) is False
