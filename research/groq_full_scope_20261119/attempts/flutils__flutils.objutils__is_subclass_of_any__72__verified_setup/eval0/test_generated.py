import pytest
from flutils.objutils import is_subclass_of_any
from collections import UserList, deque, ValuesView, KeysView


def test_is_subclass_of_any_normal(tmp_path):
    """Verify that the function returns True for a valid subclass match."""
    # Create a list-like object that is a subclass of UserList
    class MyList(UserList):
        pass

    obj = MyList([1, 2, 3])
    # Should detect subclass relationship
    assert is_subclass_of_any(obj, UserList, deque) is True
    # Should also detect subclass relationship with a more specific class
    assert is_subclass_of_any(obj, MyList) is True
    # Should return False when no match
    assert is_subclass_of_any(obj, deque, ValuesView) is False


def test_is_subclass_of_any_boundary(tmp_path):
    """Verify that passing no classes returns False."""
    obj = deque([1, 2, 3])
    # No classes to check against
    assert is_subclass_of_any(obj) is False
    # Passing a non-matching class
    assert is_subclass_of_any(obj, UserList) is False


def test_is_subclass_of_any_error(tmp_path):
    """Verify that passing a non-class argument raises TypeError."""
    obj = deque([1, 2, 3])
    # Passing a string instead of a class should raise TypeError
    with pytest.raises(TypeError):
        is_subclass_of_any(obj, "not_a_class")
