import pytest
from pysnooper.utils import get_shortish_repr

def test_basic_repr_and_normalize(tmp_path):
    # A simple object with a custom repr that includes newlines and carriage returns
    class Obj:
        def __repr__(self):
            return "Line1\r\nLine2\nLine3"

    obj = Obj()
    # Without normalization, newlines and carriage returns should be removed
    assert get_shortish_repr(obj) == "Line1Line2Line3"
    # With normalization, the string should be lowercased and spaces removed
    # (normalize_repr lowercases and removes spaces)
    assert get_shortish_repr(obj, normalize=True) == "line1line2line3"

def test_truncate_behavior():
    # A long string that will be truncated
    long_str = "a" * 50
    # max_length 10 should cut to 10 characters
    assert get_shortish_repr(long_str, max_length=10) == "a" * 10
    # If max_length is None, the string should remain unchanged
    assert get_shortish_repr(long_str, max_length=None) == long_str

def test_error_in_repr_and_custom_repr():
    # A class whose __repr__ raises an exception
    class BadRepr:
        def __repr__(self):
            raise ValueError("bad repr")

    bad = BadRepr()
    # get_shortish_repr should catch the exception and return 'REPR FAILED'
    assert get_shortish_repr(bad) == "REPR FAILED"

    # Custom repr functions can also raise; they should be tried before the default
    def bad_custom_repr(item):
        raise RuntimeError("custom fail")

    # Provide a custom_repr tuple that includes the failing function
    assert get_shortish_repr(bad, custom_repr=(bad_custom_repr,)) == "REPR FAILED"
