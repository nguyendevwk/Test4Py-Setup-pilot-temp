import pytest
from isort.exceptions import SortingFunctionDoesNotExist, ISortError


def test_sorting_function_does_not_exist_message_and_attributes():
    """Verify that the exception message contains the sort order and available orders,
    and that the attributes are set correctly."""
    sort_order = "unknown"
    available = ["ascending", "descending", "alphabetical"]
    exc = SortingFunctionDoesNotExist(sort_order, available)

    # Message should mention the requested sort order and list available orders
    assert sort_order in str(exc)
    for order in available:
        assert order in str(exc)

    # Attributes should match the constructor arguments
    assert exc.sort_order == sort_order
    assert exc.available_sort_orders == available


def test_sorting_function_does_not_exist_inherits_from_isort_error_and_exception():
    """Ensure the exception inherits from ISortError and the built‑in Exception."""
    exc = SortingFunctionDoesNotExist("foo", ["bar"])
    assert isinstance(exc, ISortError)
    assert isinstance(exc, Exception)


def test_sorting_function_does_not_exist_can_be_caught_and_rethrown():
    """Test that the exception can be caught and re‑raised, preserving its type and message."""
    sort_order = "invalid"
    available = ["valid"]
    try:
        raise SortingFunctionDoesNotExist(sort_order, available)
    except SortingFunctionDoesNotExist as e:
        # Re‑raise the same exception instance
        raise e
    except Exception as e:
        # If any other exception type is raised, the test should fail
        pytest.fail(f"Unexpected exception type: {type(e)}")
