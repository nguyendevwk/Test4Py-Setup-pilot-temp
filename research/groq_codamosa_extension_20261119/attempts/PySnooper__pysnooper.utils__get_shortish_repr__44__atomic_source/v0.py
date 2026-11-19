import pytest
from pysnooper.utils import get_shortish_repr

# Helper class whose __repr__ raises an exception
class BadRepr:
    def __repr__(self):
        raise ValueError("bad repr")

def test_custom_repr_overrides_default():
    # Custom representation for list type
    custom_func = lambda x: f"LIST({len(x)})"
    result = get_shortish_repr([1, 2, 3], custom_repr=((list, custom_func),))
    assert result == "LIST(3)", "Custom repr should override default for list"

def test_truncate_and_normalize_behavior():
    long_string = "a" * 50
    # Without max_length, should return full string
    full = get_shortish_repr(long_string)
    assert full == long_string, "Full string should be returned when no max_length"

    # With max_length, output should be truncated
    truncated = get_shortish_repr(long_string, max_length=10)
    assert len(truncated) <= 10, "Output should be truncated to max_length"
    assert truncated == "a" * 10, "Truncation should keep the first characters"

    # normalize=True should not alter a plain string of 'a's
    normalized = get_shortish_repr(long_string, normalize=True)
    assert normalized == long_string, "Normalization should not change plain string"

def test_repr_failure_returns_placeholder():
    # Object whose __repr__ raises an exception
    bad = BadRepr()
    result = get_shortish_repr(bad)
    assert result == "REPR FAILED", "Failed repr should return placeholder string"
