import pytest
from isort.exceptions import SortingFunctionDoesNotExist

def test_sorting_function_does_not_exist_initialization():
    """Verify that the exception stores the provided sort order and available list."""
    sort_order = "invalid"
    available = ["ascending", "descending"]
    exc = SortingFunctionDoesNotExist(sort_order, available)
    assert exc.sort_order == sort_order
    assert exc.available_sort_orders == available

def test_sorting_function_does_not_exist_message_content():
    """Check that the exception message contains the sort order and all available options."""
    sort_order = "foo"
    available = ["bar", "baz"]
    exc = SortingFunctionDoesNotExist(sort_order, available)
    expected_msg = (
        f"Specified sort_order of {sort_order} does not exist. "
        f"Available sort_orders: {','.join(available)}."
    )
    assert str(exc) == expected_msg

def test_sorting_function_does_not_exist_inherits_from_ISortError():
    """Ensure the exception is a subclass of ISortError."""
    from isort.exceptions import ISortError
    exc = SortingFunctionDoesNotExist("x", ["y"])
    assert isinstance(exc, ISortError)
