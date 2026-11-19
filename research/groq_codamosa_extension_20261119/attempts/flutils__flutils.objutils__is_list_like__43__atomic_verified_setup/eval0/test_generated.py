import pytest
from flutils.objutils import is_list_like
from collections import UserList, deque, Counter, defaultdict
from collections.abc import Iterator, KeysView, ValuesView
from typing import Iterator as TypingIterator

def test_list_like_with_various_iterables():
    # List-like objects should return True
    assert is_list_like([1, 2, 3]) is True
    assert is_list_like(UserList([4, 5])) is True
    assert is_list_like(deque([6, 7])) is True
    assert is_list_like(set([8, 9])) is True
    assert is_list_like(tuple([10, 11])) is True
    assert is_list_like(ValuesView({12: 'a'})) is True
    assert is_list_like(KeysView({13: 'b'})) is True
    assert is_list_like(reversed([14, 15])) is True
    assert is_list_like(sorted('hello')) is True

def test_non_list_like_objects():
    # Non list-like objects should return False
    assert is_list_like(None) is False
    assert is_list_like(True) is False
    assert is_list_like(b'bytes') is False
    assert is_list_like(Counter({'a': 1})) is False
    assert is_list_like(defaultdict(int)) is False
    assert is_list_like(123) is False
    assert is_list_like(12.34) is False
    assert is_list_like('string') is False

def test_edge_cases_and_boundary_conditions(tmp_path):
    # Empty containers and custom iterators
    empty_list = []
    empty_tuple = ()
    empty_set = set()
    empty_deque = deque()
    assert is_list_like(empty_list) is True
    assert is_list_like(empty_tuple) is True
    assert is_list_like(empty_set) is True
    assert is_list_like(empty_deque) is True

    # Custom iterator that yields nothing
    class EmptyIterator(Iterator):
        def __iter__(self):
            return self
        def __next__(self):
            raise StopIteration

    empty_iter = EmptyIterator()
    assert is_list_like(empty_iter) is True

    # Ensure that a file path object is not considered list-like
    file_path = tmp_path / "file.txt"
    file_path.write_text("content")
    assert is_list_like(file_path) is False
