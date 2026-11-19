import pytest
from flutils.objutils import is_list_like
from collections import UserList, deque, Counter, defaultdict, OrderedDict, UserDict, UserString
from collections.abc import Iterator, KeysView, ValuesView
from decimal import Decimal

def test_list_like_basic_and_iterators(tmp_path):
    # List
    assert is_list_like([1, 2, 3]) is True
    # UserList
    assert is_list_like(UserList([4, 5])) is True
    # deque
    assert is_list_like(deque([6, 7])) is True
    # Iterator
    assert is_list_like(iter([8, 9])) is True
    # KeysView and ValuesView
    d = {'a': 1, 'b': 2}
    assert is_list_like(d.keys()) is True
    assert is_list_like(d.values()) is True
    # frozenset, set, tuple
    assert is_list_like(frozenset([10, 11])) is True
    assert is_list_like(set([12, 13])) is True
    assert is_list_like((14, 15)) is True
    # Empty structures
    assert is_list_like([]) is True
    assert is_list_like(set()) is True
    assert is_list_like(()) is True

def test_list_like_exclusions_and_edge_cases():
    # None, bool, bytes, int, float, str
    for obj in [None, True, False, b'bytes', 42, 3.14, 'string']:
        assert is_list_like(obj) is False
    # Counter, defaultdict, OrderedDict, UserDict, UserString
    for obj in [Counter(), defaultdict(list), OrderedDict(), UserDict(), UserString('test')]:
        assert is_list_like(obj) is False
    # Decimal
    assert is_list_like(Decimal('1.23')) is False
    # dict
    assert is_list_like({'key': 'value'}) is False

def test_list_like_with_non_iterable_and_custom_objects():
    class Custom:
        pass
    # Custom object not iterable
    assert is_list_like(Custom()) is False
    # Custom iterable but not list-like
    class CustomIter:
        def __iter__(self):
            return iter([1, 2, 3])
    assert is_list_like(CustomIter()) is True
