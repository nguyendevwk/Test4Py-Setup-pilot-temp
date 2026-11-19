import pytest
from flutils.objutils import is_subclass_of_any
from collections import UserList, deque, ValuesView, KeysView


def test_is_subclass_of_any_with_valid_subclass(tmp_path):
    """When the object is a subclass of one of the provided classes, the function returns True."""
    # Create a subclass of UserList
    class MyList(UserList):
        pass

    obj = MyList([1, 2, 3])
    # Should be True because MyList is a subclass of UserList
    assert is_subclass_of_any(obj, UserList, deque) is True
    # Should also be True for a subclass of deque
    class MyDeque(deque):
        pass

    obj2 = MyDeque([4, 5])
    assert is_subclass_of_any(obj2, deque, UserList) is True


def test_is_subclass_of_any_with_no_match_and_empty_classes(tmp_path):
    """When the object is not a subclass of any provided classes, or no classes are provided, the function returns False."""
    # Object is a dict; not a subclass of deque or UserList
    obj = {"a": 1}
    assert is_subclass_of_any(obj, deque, UserList) is False
    # No classes provided should also return False
    assert is_subclass_of_any(obj) is False


def test_is_subclass_of_any_with_invalid_class_argument(tmp_path):
    """Passing a non-class as a class argument should raise a TypeError due to issubclass."""
    obj = deque([1, 2, 3])
    with pytest.raises(TypeError):
        # Pass an integer instead of a class; issubclass will raise
        is_subclass_of_any(obj, 42, deque)
