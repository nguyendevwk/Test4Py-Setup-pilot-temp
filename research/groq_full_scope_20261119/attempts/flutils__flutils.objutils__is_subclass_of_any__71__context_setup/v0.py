import pytest
from flutils.objutils import is_subclass_of_any
from collections import UserList, deque, ValuesView, KeysView


def test_is_subclass_of_any_with_builtin_and_custom_classes():
    class MyList(UserList):
        pass

    # Instance of MyList should be subclass of UserList
    obj = MyList([1, 2, 3])
    assert is_subclass_of_any(obj, UserList, deque) is True

    # Instance of deque should be subclass of deque
    d = deque([4, 5, 6])
    assert is_subclass_of_any(d, deque, UserList) is True

    # Instance of dict keys view should be subclass of KeysView
    kv = {"a": 1}.keys()
    assert is_subclass_of_any(kv, KeysView, ValuesView) is True

    # Instance of dict values view should be subclass of ValuesView
    vv = {"b": 2}.values()
    assert is_subclass_of_any(vv, ValuesView, KeysView) is True


def test_is_subclass_of_any_with_no_matching_classes_and_empty_tuple():
    # No classes provided should return False
    obj = [1, 2, 3]
    assert is_subclass_of_any(obj) is False

    # Provide classes that do not match the object's type
    assert is_subclass_of_any(obj, dict, set) is False

    # Provide an empty tuple explicitly
    assert is_subclass_of_any(obj, ()) is False


def test_is_subclass_of_any_with_invalid_class_arguments():
    # Passing a non-class (e.g., an integer) should not raise an exception
    # but simply return False because issubclass will fail
    obj = "string"
    assert is_subclass_of_any(obj, 42, None) is False

    # Passing a mix of valid and invalid class-like objects
    class Dummy:
        pass

    assert is_subclass_of_any(Dummy(), Dummy, 123) is True
