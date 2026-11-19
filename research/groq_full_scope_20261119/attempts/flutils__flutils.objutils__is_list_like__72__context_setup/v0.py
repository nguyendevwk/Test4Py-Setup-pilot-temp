import pytest
from flutils.objutils import is_list_like
from collections import deque, UserList, KeysView, ValuesView

def test_is_list_like_with_various_iterables():
    # List
    assert is_list_like([1, 2, 3]) is True
    # Set
    assert is_list_like({1, 2}) is True
    # Frozen set
    assert is_list_like(frozenset([1, 2])) is True
    # Tuple
    assert is_list_like((1, 2, 3)) is True
    # Deque
    assert is_list_like(deque([1, 2, 3])) is True
    # Iterator
    assert is_list_like(iter([1, 2, 3])) is True
    # KeysView
    assert is_list_like(dict(a=1).keys()) is True
    # ValuesView
    assert is_list_like(dict(a=1).values()) is True
    # UserList
    assert is_list_like(UserList([1, 2, 3])) is True

def test_is_list_like_boundary_empty_iterables():
    # Empty list
    assert is_list_like([]) is True
    # Empty set
    assert is_list_like(set()) is True
    # Empty tuple
    assert is_list_like(()) is True
    # Empty deque
    assert is_list_like(deque()) is True
    # Empty UserList
    assert is_list_like(UserList()) is True

def test_is_list_like_non_iterable_and_non_list_like():
    # Primitive types
    assert is_list_like(42) is False
    assert is_list_like(3.14) is False
    assert is_list_like(True) is False
    # String
    assert is_list_like("hello") is False
    # Bytes
    assert is_list_like(b"bytes") is False
    # None
    assert is_list_like(None) is False
