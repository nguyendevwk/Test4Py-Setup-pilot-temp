import pytest
from pysnooper.utils import ensure_tuple

def test_ensure_tuple_with_iterable_and_non_string():
    # Iterable that is not a string should be converted to a tuple
    result = ensure_tuple([1, 2, 3])
    assert isinstance(result, tuple)
    assert result == (1, 2, 3)

def test_ensure_tuple_with_string_and_none():
    # Strings and None should be wrapped in a single-element tuple
    assert ensure_tuple("hello") == ("hello",)
    assert ensure_tuple(None) == (None,)

def test_ensure_tuple_with_generator_and_empty_iterable():
    # Generators and empty iterables should be converted correctly
    gen = (x for x in range(2))
    assert ensure_tuple(gen) == (0, 1)
    assert ensure_tuple([]) == ()
