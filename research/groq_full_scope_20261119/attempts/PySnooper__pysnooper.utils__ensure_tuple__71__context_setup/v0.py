import pytest
from pysnooper.utils import ensure_tuple

def test_iterable_conversion():
    # List, set, and generator should be converted to a tuple of their elements
    lst = [1, 2, 3]
    st = {4, 5}
    gen = (x for x in range(2))
    assert ensure_tuple(lst) == (1, 2, 3)
    assert ensure_tuple(st) == tuple(st)  # order may vary but tuple conversion is deterministic
    assert ensure_tuple(gen) == (0, 1)

def test_string_and_bytes_preserved():
    # Strings and bytes should not be expanded into tuples of characters
    s = "hello"
    b = b"bytes"
    assert ensure_tuple(s) == ("hello",)
    assert ensure_tuple(b) == (b"bytes",)

def test_non_iterable_singleton():
    # Non-iterable objects should be wrapped in a single-element tuple
    assert ensure_tuple(42) == (42,)
    assert ensure_tuple(None) == (None,)
    class Custom:
        pass
    assert ensure_tuple(Custom()) == (Custom(),)
