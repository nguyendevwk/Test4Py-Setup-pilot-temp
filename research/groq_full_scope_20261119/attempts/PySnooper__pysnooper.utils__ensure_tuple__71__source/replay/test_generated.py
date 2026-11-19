import pytest
from pysnooper.utils import ensure_tuple

def test_ensure_tuple_with_iterable_and_non_string():
    # Iterable that is not a string should be converted to a tuple
    lst = [1, 2, 3]
    result = ensure_tuple(lst)
    assert isinstance(result, tuple)
    assert result == (1, 2, 3)

def test_ensure_tuple_with_string_and_empty_iterable():
    # Strings should not be treated as iterables for this function
    s = "abc"
    result_str = ensure_tuple(s)
    assert result_str == ("abc",)

    # Empty iterable should return an empty tuple
    empty_list = []
    result_empty = ensure_tuple(empty_list)
    assert result_empty == ()

def test_ensure_tuple_with_non_iterable_and_generator():
    # Non-iterable objects should be wrapped in a tuple
    num = 42
    result_num = ensure_tuple(num)
    assert result_num == (42,)

    # Generators are iterables and should be converted to tuples
    gen = (x for x in range(3))
    result_gen = ensure_tuple(gen)
    assert result_gen == (0, 1, 2)
