import pytest
from collections import deque, UserList, KeysView, ValuesView
from flutils.objutils import is_list_like


def test_is_list_like_with_various_list_like_objects():
    """Normal case: objects that should be considered list-like."""
    assert is_list_like([1, 2, 3]) is True
    assert is_list_like(set([1, 2])) is True
    assert is_list_like(frozenset([1, 2])) is True
    assert is_list_like((1, 2, 3)) is True
    assert is_list_like(deque([1, 2, 3])) is True
    assert is_list_like(UserList([1, 2, 3])) is True
    # KeysView and ValuesView from a dict
    d = {"a": 1, "b": 2}
    assert isinstance(d.keys(), KeysView)
    assert isinstance(d.values(), ValuesView)
    assert is_list_like(d.keys()) is True
    assert is_list_like(d.values()) is True


def test_is_list_like_boundary_cases():
    """Boundary case: empty containers should still be list-like."""
    assert is_list_like([]) is True
    assert is_list_like(set()) is True
    assert is_list_like(frozenset()) is True
    assert is_list_like(()) is True
    assert is_list_like(deque()) is True
    assert is_list_like(UserList()) is True
    # Empty dict views
    empty_dict = {}
    assert is_list_like(empty_dict.keys()) is True
    assert is_list_like(empty_dict.values()) is True


def test_is_list_like_non_list_like_objects():
    """Error/negative case: objects that should not be considered list-like."""
    assert is_list_like(None) is False
    assert is_list_like(True) is False
    assert is_list_like(False) is False
    assert is_list_like(42) is False
    assert is_list_like(3.14) is False
    assert is_list_like("hello") is False
    assert is_list_like(b"bytes") is False
    # dict itself is not list-like
    assert is_list_like({"a": 1}) is False
    # Counter is not list-like
    from collections import Counter
    assert is_list_like(Counter([1, 2, 3])) is False
