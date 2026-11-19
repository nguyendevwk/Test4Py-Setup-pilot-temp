import pytest
from flutils.objutils import is_subclass_of_any
from collections import UserList, deque, ValuesView, KeysView


def test_is_subclass_of_any_with_builtin_and_custom_classes():
    class MyList(UserList):
        pass

    # Instance of MyList should be subclass of UserList
    assert is_subclass_of_any(MyList(), UserList, deque) is True

    # Instance of deque should be subclass of deque
    assert is_subclass_of_any(deque([1, 2, 3]), deque, UserList) is True

    # Instance of dict keys view should be subclass of KeysView
    assert is_subclass_of_any({"a": 1}.keys(), KeysView, ValuesView) is True

    # Instance of dict values view should be subclass of ValuesView
    assert is_subclass_of_any({"a": 1}.values(), ValuesView, KeysView) is True


def test_is_subclass_of_any_with_no_matching_classes_and_empty_tuple():
    class Dummy:
        pass

    # No classes provided should return False
    assert is_subclass_of_any(Dummy(),) is False

    # Empty tuple of classes should also return False
    assert is_subclass_of_any(Dummy(), *()) is False


def test_is_subclass_of_any_with_invalid_class_argument():
    # Passing a non-class as a target should raise a TypeError from issubclass
    with pytest.raises(TypeError):
        is_subclass_of_any(42, int, "not_a_class")
