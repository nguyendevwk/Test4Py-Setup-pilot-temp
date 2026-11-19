import pytest
from pysnooper.utils import ensure_tuple
from collections.abc import Iterable

def test_ensure_tuple_with_iterable():
    # A list should be converted to a tuple of its elements
    result = ensure_tuple([1, 2, 3])
    assert isinstance(result, tuple)
    assert result == (1, 2, 3)

def test_ensure_tuple_with_string():
    # Strings are iterable but should be treated as a single element
    result = ensure_tuple("abc")
    assert isinstance(result, tuple)
    assert result == ("abc",)

def test_ensure_tuple_with_non_iterable():
    # Non-iterable objects should be wrapped in a single-element tuple
    class Dummy: pass
    dummy = Dummy()
    result = ensure_tuple(dummy)
    assert isinstance(result, tuple)
    assert result == (dummy,)
