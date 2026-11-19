import pytest
from flutils.objutils import is_list_like
from collections import UserList, deque, Counter, defaultdict
from collections.abc import Iterator, KeysView, ValuesView
from typing import Any

def test_list_like_with_builtin_and_custom_iterables():
    # Built-in list
    assert is_list_like([1, 2, 3]) is True
    # UserList instance
    assert is_list_like(UserList([4, 5])) is True
    # deque
    assert is_list_like(deque([6, 7])) is True
    # Iterator
    assert is_list_like(iter([8, 9])) is True
    # KeysView and ValuesView from a dict
    d = {'a': 1, 'b': 2}
    assert is_list_like(d.keys()) is True
    assert is_list_like(d.values()) is True
    # Tuple
    assert is_list_like((10, 11)) is True
    # Set
    assert is_list_like({12, 13}) is True
    # frozenset
    assert is_list_like(frozenset({14, 15})) is True

def test_list_like_excludes_non_iterable_and_special_types():
    # None
    assert is_list_like(None) is False
    # bool
    assert is_list_like(True) is False
    # bytes
    assert is_list_like(b'bytes') is False
    # int
    assert is_list_like(42) is False
    # float
    assert is_list_like(3.14) is False
    # str
    assert is_list_like('hello') is False
    # dict
    assert is_list_like({'x': 1}) is False
    # Counter (subclass of dict)
    assert is_list_like(Counter({'a': 1})) is False
    # defaultdict
    assert is_list_like(defaultdict(int)) is False

def test_list_like_with_edge_cases_and_boundary_values():
    # Empty list
    assert is_list_like([]) is True
    # Empty tuple
    assert is_list_like(()) is True
    # Empty set
    assert is_list_like(set()) is True
    # Empty deque
    assert is_list_like(deque()) is True
    # Empty UserList
    assert is_list_like(UserList()) is True
    # Iterator over empty list
    assert is_list_like(iter([])) is True
    # Iterator over empty tuple
    assert is_list_like(iter(())) is True
    # Iterator over empty set
    assert is_list_like(iter(set())) is True
