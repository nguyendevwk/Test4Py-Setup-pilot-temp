import pytest
from pysnooper.utils import get_shortish_repr, truncate, normalize_repr


def test_custom_repr_and_truncate(tmp_path):
    # Custom representation for int type
    custom_repr = (int, lambda x: f"int:{x}")
    # Value that will be represented by custom function
    value = 42
    # Without max_length, representation should use custom function
    assert get_shortish_repr(value, custom_repr=custom_repr) == "int:42"

    # With max_length smaller than the custom representation length
    short_repr = get_shortish_repr(value, custom_repr=custom_repr, max_length=5)
    # The result must be truncated to at most 5 characters
    assert len(short_repr) <= 5
    # Since the original representation is "int:42" (6 chars), truncation should cut it
    assert short_repr == "int:4"


def test_normalize_and_newline_handling():
    # String containing newlines and carriage returns
    raw = "line1\r\nline2\nline3"
    # Normalization should remove all newlines and carriage returns
    normalized = normalize_repr(raw.replace('\r', '').replace('\n', ''))
    # The normalized representation should be a single line without any newline characters
    assert '\n' not in normalized
    assert '\r' not in normalized
    # Using get_shortish_repr with normalize=True should produce the same result
    assert get_shortish_repr(raw, normalize=True) == normalized


def test_repr_failure_returns_placeholder():
    class BadRepr:
        def __repr__(self):
            raise ValueError("bad repr")

    bad_obj = BadRepr()
    # When the object's __repr__ raises an exception, get_shortish_repr should return the placeholder
    assert get_shortish_repr(bad_obj) == "REPR FAILED"
