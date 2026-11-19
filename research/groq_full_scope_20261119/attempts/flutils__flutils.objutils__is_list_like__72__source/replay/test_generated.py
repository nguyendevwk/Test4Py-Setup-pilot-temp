import pytest
from flutils.objutils import is_list_like
from collections import UserList, deque, Counter, defaultdict
from collections.abc import Iterator, KeysView, ValuesView
from typing import Iterator as TypingIterator

def test_is_list_like_with_various_iterables():
    # List-like objects
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
    # Iterator from a generator
    gen = (x for x in range(3))
    assert isinstance(gen, Iterator)
    assert is_list_like(gen) is True

def test_is_list_like_excludes_non_iterables_and_special_types():
    # Non-list-like types
    assert is_list_like(None) is False
    assert is_list_like(True) is False
    assert is_list_like(False) is False
    assert is_list_like(42) is False
    assert is_list_like(3.14) is False
    assert is_list_like('hello') is False
    assert is_list_like(b'bytes') is False
    # Collections that are not list-like
    assert is_list_like(Counter({'a': 1})) is False
    assert is_list_like(defaultdict(int)) is False
    assert is_list_like(dict({'a': 1})) is False

def test_is_list_like_with_custom_iterator_and_edge_cases(tmp_path):
    # Custom iterator class
    class MyIter:
        def __iter__(self):
            return self
        def __next__(self):
            raise StopIteration
    assert is_list_like(MyIter()) is True
    # Empty iterable
    assert is_list_like([]) is True
    assert is_list_like(set()) is True
    assert is_list_like(tuple()) is True
    # Temporary file path as an object (not iterable)
    assert is_list_like(tmp_path) is False
