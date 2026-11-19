import pytest
from isort.exceptions import SortingFunctionDoesNotExist

def test_sorting_function_does_not_exist_message_and_attributes():
    sort_order = "invalid"
    available = ["ascending", "descending", "alphabetical"]
    exc = SortingFunctionDoesNotExist(sort_order, available)
    # Check that the message contains the sort_order and all available orders
    assert sort_order in str(exc)
    for order in available:
        assert order in str(exc)
    # Check that the attributes are set correctly
    assert exc.sort_order == sort_order
    assert exc.available_sort_orders == available

def test_sorting_function_does_not_exist_empty_available():
    sort_order = "none"
    available = []
    exc = SortingFunctionDoesNotExist(sort_order, available)
    # The message should still mention the sort_order and show empty list
    assert "none" in str(exc)
    assert "Available sort_orders:" in str(exc)
    # The available_sort_orders attribute should be an empty list
    assert exc.available_sort_orders == []

def test_sorting_function_does_not_exist_non_string_sort_order():
    sort_order = 42  # non-string sort_order
    available = ["a", "b"]
    exc = SortingFunctionDoesNotExist(sort_order, available)
    # The message should convert the sort_order to string
    assert "42" in str(exc)
    # The attributes should store the original value
    assert exc.sort_order == 42
    assert exc.available_sort_orders == available
