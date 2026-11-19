import pytest
from pysnooper.utils import get_shortish_repr

def test_default_repr_and_truncate():
    # Normal object: repr is short enough, no truncation
    result = get_shortish_repr(12345)
    assert result == "12345"

    # Long string triggers truncation
    long_str = "a" * 50
    truncated = get_shortish_repr(long_str, max_length=10)
    # Should keep first 4 and last 3 characters with ellipsis
    assert truncated == "aaaa...aaa"
    assert len(truncated) == 10
    # Ensure no newlines or carriage returns
    assert "\n" not in truncated and "\r" not in truncated

def test_custom_repr_function():
    # Custom repr for int that returns hex
    custom = [(int, lambda x: f"0x{x:x}")]
    result = get_shortish_repr(255, custom_repr=custom)
    assert result == "0xff"

    # Custom repr for a specific instance
    class Dummy: pass
    dummy = Dummy()
    custom = [(lambda x: isinstance(x, Dummy), lambda x: "DUMMY")]
    result = get_shortish_repr(dummy, custom_repr=custom)
    assert result == "DUMMY"

def test_normalize_and_error_handling(tmp_path):
    # Object whose repr contains a memory address
    class WithAddr:
        def __repr__(self):
            return f"<WithAddr at 0x1234>"
    obj = WithAddr()
    # Without normalization, address remains
    raw = get_shortish_repr(obj)
    assert "0x1234" in raw
    # With normalization, address is removed
    norm = get_shortish_repr(obj, normalize=True)
    assert "0x1234" not in norm
    assert norm == "<WithAddr >"

    # Repr that raises an exception
    class BadRepr:
        def __repr__(self):
            raise ValueError("bad repr")
    bad = BadRepr()
    result = get_shortish_repr(bad)
    assert result == "REPR FAILED"
