import pytest
from pysnooper.utils import get_shortish_repr, get_repr_function, normalize_repr, truncate

class CustomRepr:
    def __repr__(self):
        return "CustomReprObject"

class BadRepr:
    def __repr__(self):
        raise ValueError("bad repr")

def test_get_shortish_repr_custom_repr_and_normalize():
    # Custom repr should be used and normalization applied
    obj = CustomRepr()
    # Without normalization, repr is unchanged
    assert get_shortish_repr(obj, custom_repr=(CustomRepr,)) == "CustomReprObject"
    # With normalization, newlines and carriage returns are removed
    obj_with_newlines = "line1\nline2\rline3"
    normalized = get_shortish_repr(obj_with_newlines, normalize=True)
    assert "\n" not in normalized and "\r" not in normalized
    assert normalized == "line1line2line3"

def test_get_shortish_repr_truncate_and_error_handling():
    # Truncate to a specific length
    long_str = "a" * 50
    truncated = get_shortish_repr(long_str, max_length=10)
    assert truncated == "a" * 10
    # When repr raises an exception, fallback string is returned
    bad_obj = BadRepr()
    repr_result = get_shortish_repr(bad_obj)
    assert repr_result == "REPR FAILED"

def test_get_repr_function_with_custom_and_default():
    # get_repr_function should return the custom function when provided
    custom_func = lambda x: f"custom:{x}"
    assert get_repr_function(5, custom_repr=(int,)) == int.__repr__
    # If custom_repr does not match, default repr is used
    assert get_repr_function(5, custom_repr=(str,)) == int.__repr__
    # Custom function passed directly
    assert get_repr_function(5, custom_repr=(custom_func,)) == custom_func
