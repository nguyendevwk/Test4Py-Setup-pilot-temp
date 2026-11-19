import builtins
import pytest
from pysnooper.utils import get_shortish_repr

# Helper class to trigger repr exception
class BadRepr:
    def __repr__(self):
        raise ValueError("bad repr")

# Helper class with custom repr
class CustomRepr:
    def __repr__(self):
        return "original"

def test_get_shortish_repr_normal_and_truncate():
    # Normal repr of a string
    s = "Hello, world!"
    r = get_shortish_repr(s, max_length=5)
    # Should truncate to first 5 characters
    assert r == "Hello"

    # Custom repr should override default
    obj = CustomRepr()
    r_custom = get_shortish_repr(obj, custom_repr=(CustomRepr,))
    # The custom repr returns "original", truncated to 4
    assert r_custom == "orig"

def test_get_shortish_repr_normalize_and_exception():
    # Repr containing newlines and carriage returns
    class MultiLine:
        def __repr__(self):
            return "Line1\r\nLine2\nLine3"
    ml = MultiLine()
    r_norm = get_shortish_repr(ml, normalize=True)
    # Newlines and carriage returns removed
    assert r_norm == "Line1Line2Line3"

    # Repr that raises exception
    bad = BadRepr()
    r_bad = get_shortish_repr(bad)
    assert r_bad == "REPR FAILED"

def test_get_shortish_repr_edge_cases():
    # Empty string with max_length 0
    empty = ""
    r_empty = get_shortish_repr(empty, max_length=0)
    assert r_empty == ""

    # None value should use default repr
    none_val = None
    r_none = get_shortish_repr(none_val)
    assert r_none == "None"

    # Large object with no max_length should not truncate
    large = "x" * 1000
    r_large = get_shortish_repr(large)
    assert r_large == large
