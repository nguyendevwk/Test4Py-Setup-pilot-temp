import pytest
from pysnooper.utils import get_shortish_repr, get_repr_function, normalize_repr, truncate

class CustomRepr:
    def __repr__(self):
        return "CustomReprObject"

class BadRepr:
    def __repr__(self):
        raise ValueError("bad repr")

def test_get_shortish_repr_with_custom_repr_and_truncate():
    # Custom representation should be used
    obj = CustomRepr()
    r = get_shortish_repr(obj, custom_repr=(CustomRepr,))
    assert r == "CustomReprObject"

    # Truncate to a short length
    long_obj = "a" * 50
    truncated = get_shortish_repr(long_obj, max_length=10)
    assert truncated == "aaaaaaaaaa"
    # Ensure truncation does not alter content beyond max_length
    assert len(truncated) == 10
    assert truncated == truncate(long_obj, 10)

def test_get_shortish_repr_normalize_and_newlines():
    # Representation with newlines and carriage returns should be cleaned
    class MultiLine:
        def __repr__(self):
            return "Line1\nLine2\rLine3"
    obj = MultiLine()
    r = get_shortish_repr(obj, normalize=True)
    # normalize_repr removes newlines and carriage returns
    expected = normalize_repr("Line1\nLine2\rLine3")
    assert r == expected
    # Ensure no newline or carriage return remains
    assert "\n" not in r and "\r" not in r

def test_get_shortish_repr_handles_repr_exception():
    # When __repr__ raises, the function should return 'REPR FAILED'
    bad = BadRepr()
    r = get_shortish_repr(bad)
    assert r == "REPR FAILED"
    # Even with max_length, it should still return the failure string
    r2 = get_shortish_repr(bad, max_length=5)
    assert r2 == "REPR FAILED"
