import pytest
from flutils.objutils import is_subclass_of_any
from collections import ValuesView, KeysView, UserList, deque

def test_is_subclass_of_any_normal():
    """Normal case: object is subclass of one of the provided classes."""
    obj = dict(a=1, b=2)
    # obj.keys() returns a KeysView instance
    assert is_subclass_of_any(obj.keys(), ValuesView, KeysView, UserList) is True

def test_is_subclass_of_any_boundary_empty_classes():
    """Boundary case: no classes provided should return False."""
    obj = deque([1, 2, 3])
    # deque is not a subclass of any class in an empty tuple
    assert is_subclass_of_any(obj, *()) is False

def test_is_subclass_of_any_error_nonclass_argument():
    """Error case: passing a non-class in the classes list should raise TypeError."""
    obj = UserList([1, 2, 3])
    with pytest.raises(TypeError):
        # Passing an int instead of a class to issubclass will raise TypeError
        is_subclass_of_any(obj, int, str)
