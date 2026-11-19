import pytest
from flutils.objutils import is_list_like

def test_is_list_like_with_iterable_and_non_iterable():
    # List-like objects should return True
    assert is_list_like([1, 2, 3]) is True
    assert is_list_like((4, 5, 6)) is True
    assert is_list_like({7, 8, 9}) is True
    assert is_list_like(frozenset([10, 11])) is True
    assert is_list_like(deque([12, 13])) is True
    assert is_list_like(iter([14, 15])) is True

    # Non list-like objects should return False
    assert is_list_like("string") is False
    assert is_list_like(42) is False
    assert is_list_like(3.14) is False
    assert is_list_like(None) is False
    assert is_list_like(True) is False

def test_is_list_like_boundary_cases():
    # Empty containers should still be considered list-like
    assert is_list_like([]) is True
    assert is_list_like(()) is True
    assert is_list_like(set()) is True
    assert is_list_like(frozenset()) is True
    assert is_list_like(deque()) is True

    # Objects that are iterable but not list-like per spec
    from collections import Counter, OrderedDict, defaultdict, ChainMap
    assert is_list_like(Counter()) is False
    assert is_list_like(OrderedDict()) is False
    assert is_list_like(defaultdict()) is False
    assert is_list_like(ChainMap()) is False

def test_is_list_like_error_and_edge_behavior():
    # Passing a custom class that inherits from list should be True
    class MyList(list):
        pass
    assert is_list_like(MyList([1, 2, 3])) is True

    # Passing a class that is not an instance but subclass of list-like types
    class MyIterator:
        def __iter__(self):
            return iter([1, 2])
    # Instance of MyIterator is iterable but not list-like per spec
    assert is_list_like(MyIterator()) is False

    # Ensure that passing a non-iterable raises no exception and returns False
    class NonIterable:
        pass
    assert is_list_like(NonIterable()) is False
