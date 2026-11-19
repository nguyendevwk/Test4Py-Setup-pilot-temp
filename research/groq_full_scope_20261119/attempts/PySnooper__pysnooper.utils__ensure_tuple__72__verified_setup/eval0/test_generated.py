import pytest
from pysnooper.utils import ensure_tuple

def test_ensure_tuple_with_iterable():
    """ensure_tuple should convert a list to a tuple."""
    result = ensure_tuple([1, 2, 3])
    assert isinstance(result, tuple)
    assert result == (1, 2, 3)

def test_ensure_tuple_with_string():
    """ensure_tuple should treat a string as a single element, not iterate over it."""
    result = ensure_tuple("abc")
    assert isinstance(result, tuple)
    assert result == ("abc",)

def test_ensure_tuple_with_non_iterable():
    """ensure_tuple should wrap a non-iterable (e.g., int) in a tuple."""
    result = ensure_tuple(42)
    assert isinstance(result, tuple)
    assert result == (42,)
