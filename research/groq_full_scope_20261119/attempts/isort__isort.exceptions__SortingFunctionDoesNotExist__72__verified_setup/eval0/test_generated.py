import pytest
from isort.exceptions import SortingFunctionDoesNotExist

def test_sorting_function_does_not_exist_message_and_attributes():
    sort_order = "invalid_order"
    available = ["ascending", "descending", "alphabetical"]
    exc = SortingFunctionDoesNotExist(sort_order, available)

    # Assert the message contains the sort_order and all available orders
    assert sort_order in str(exc)
    for order in available:
        assert order in str(exc)

    # Assert the attributes are set correctly
    assert exc.sort_order == sort_order
    assert exc.available_sort_orders == available

def test_sorting_function_does_not_exist_empty_available():
    sort_order = "none"
    available = []
    exc = SortingFunctionDoesNotExist(sort_order, available)

    # Message should still be informative even with no available orders
    assert "Specified sort_order of none does not exist." in str(exc)
    assert "Available sort_orders:" in str(exc)

    # Attributes should reflect the inputs
    assert exc.sort_order == "none"
    assert exc.available_sort_orders == []

def test_sorting_function_does_not_exist_with_non_string_sort_order():
    # sort_order can be any type; the message should convert it to string
    sort_order = 123
    available = ["asc", "desc"]
    exc = SortingFunctionDoesNotExist(sort_order, available)

    # The string representation of the sort_order should appear in the message
    assert "123" in str(exc)
    # Attributes should store the original value
    assert exc.sort_order == 123
    assert exc.available_sort_orders == available
