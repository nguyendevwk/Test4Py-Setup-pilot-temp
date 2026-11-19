import pickle
import pytest
from isort.exceptions import SortingFunctionDoesNotExist, ISortError


def test_sorting_function_does_not_exist_initialization():
    """Verify that the exception stores the sort order and available orders."""
    sort_order = "invalid"
    available = ["py", "py3", "py2"]
    exc = SortingFunctionDoesNotExist(sort_order, available)

    assert isinstance(exc, ISortError)
    assert exc.sort_order == sort_order
    assert exc.available_sort_orders == available


def test_sorting_function_does_not_exist_message():
    """Check that the error message contains the provided sort order and list."""
    sort_order = "unknown"
    available = ["py", "py3"]
    exc = SortingFunctionDoesNotExist(sort_order, available)

    expected_msg = (
        f"Specified sort_order of {sort_order} does not exist. "
        f"Available sort_orders: {','.join(available)}."
    )
    assert str(exc) == expected_msg
    assert expected_msg in exc.args[0]


def test_sorting_function_does_not_exist_pickle_roundtrip():
    """Ensure the exception can be pickled and unpickled correctly."""
    sort_order = "bad"
    available = ["py", "py3"]
    exc = SortingFunctionDoesNotExist(sort_order, available)

    data = pickle.dumps(exc)
    loaded = pickle.loads(data)

    assert isinstance(loaded, SortingFunctionDoesNotExist)
    assert loaded.sort_order == sort_order
    assert loaded.available_sort_orders == available
    assert str(loaded) == str(exc)
