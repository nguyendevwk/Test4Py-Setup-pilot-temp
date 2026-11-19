import pytest
from pysnooper.utils import get_shortish_repr

def test_get_shortish_repr_basic():
    # Basic integer representation should be unchanged
    assert get_shortish_repr(42) == "42"
    # Custom representation for a specific type
    custom = [(int, lambda x: f"int:{x}")]
    assert get_shortish_repr(7, custom_repr=custom) == "int:7"

def test_get_shortish_repr_truncate():
    long_str = "abcdefghijklmnopqrstuvwxyz"
    # Truncate to 10 characters
    truncated = get_shortish_repr(long_str, max_length=10)
    # Should contain first 3 and last 3 characters with ellipsis
    assert truncated == "abc...xyz"
    # Truncate to length equal to string length should return original
    assert get_shortish_repr(long_str, max_length=len(long_str)) == long_str

def test_get_shortish_repr_normalize():
    # Create an object with a default repr containing a memory address
    class Dummy:
        def __repr__(self):
            return f"<Dummy at 0x1234abcd>"
    dummy = Dummy()
    # Without normalization, address remains
    raw = get_shortish_repr(dummy)
    assert "0x1234abcd" in raw
    # With normalization, address is removed
    normalized = get_shortish_repr(dummy, normalize=True)
    assert "0x1234abcd" not in normalized
    assert normalized == "<Dummy >"
