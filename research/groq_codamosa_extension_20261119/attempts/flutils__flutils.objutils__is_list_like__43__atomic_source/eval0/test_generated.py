import pytest
from flutils.objutils import is_list_like
from collections import UserList, deque, Counter, OrderedDict, defaultdict, ChainMap
from collections.abc import Iterator, KeysView, ValuesView
from typing import Any

def test_is_list_like_with_various_list_like_objects():
    # List-like objects should return True
    assert is_list_like([1, 2, 3]) is True
    assert is_list_like(UserList([4, 5])) is True
    assert is_list_like(deque([6, 7])) is True
    assert is_list_like(set([8, 9])) is True
    assert is_list_like(frozenset([10, 11])) is True
    assert is_list_like(tuple([12, 13])) is True
    assert is_list_like(reversed([14, 15])) is True
    assert is_list_like(sorted('abc')) is True
    # KeysView and ValuesView from a dict
    d = {'a': 1, 'b': 2}
    assert isinstance(d.keys(), KeysView)
    assert isinstance(d.values(), ValuesView)
    assert is_list_like(d.keys()) is True
    assert is_list_like(d.values()) is True

def test_is_list_like_with_non_list_like_objects():
    # Non-list-like objects should return False
    assert is_list_like(None) is False
    assert is_list_like(True) is False
    assert is_list_like(False) is False
    assert is_list_like(b'bytes') is False
    assert is_list_like(123) is False
    assert is_list_like(3.14) is False
    assert is_list_like('string') is False
    assert is_list_like(dict({'x': 1})) is False
    assert is_list_like(OrderedDict([('x', 1)])) is False
    assert is_list_like(UserDict({'x': 1})) is False
    assert is_list_like(UserString('x')) is False
    assert is_list_like(defaultdict(int)) is False
    assert is_list_like(ChainMap({'x': 1})) is False
    assert is_list_like(Counter({'x': 1})) is False

def test_is_list_like_boundary_and_error_behavior():
    # Boundary: empty list-like objects
    assert is_list_like([]) is True
    assert is_list_like(set()) is True
    assert is_list_like(tuple()) is True
    assert is_list_like(deque()) is True
    # Error: passing a custom object that mimics iterable but not list-like
    class MyIterable:
        def __iter__(self):
            return iter([1, 2, 3])
    assert is_list_like(MyIterable()) is False
