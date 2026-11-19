import builtins
import pytest
from pysnooper.utils import get_shortish_repr, get_repr_function, normalize_repr, truncate


def test_custom_repr_overrides_default():
    """Custom representation should be used when provided."""
    class Dummy:
        def __repr__(self):
            return "original_repr"

    # Custom repr function that returns a different string
    def custom_repr(obj):
        return f"custom:{obj.__class__.__name__}"

    result = get_shortish_repr(Dummy(), custom_repr=(custom_repr,))
    assert result == "custom:Dummy", "Custom repr function was not applied correctly"

    # Ensure that the default repr is not used
    assert result != "original_repr", "Default repr was incorrectly used"


def test_normalize_and_truncate_behavior():
    """normalize=True should replace newlines and tabs; max_length truncates correctly."""
    long_string = "Line1\nLine2\tLine3\rLine4"
    # normalize should remove newlines and tabs, keep carriage returns removed
    normalized = normalize_repr(long_string)
    assert "\n" not in normalized
    assert "\t" not in normalized
    assert "\r" not in normalized
    assert normalized == "Line1Line2Line3Line4"

    # truncate should cut the string to the specified length
    truncated = truncate("abcdefghij", 5)
    assert truncated == "abcde", "truncate did not cut to the correct length"

    # Combined usage in get_shortish_repr
    combined = get_shortish_repr(long_string, max_length=10, normalize=True)
    # After normalization, length is 16; truncating to 10 should give first 10 chars
    assert combined == "Line1Line2", "Combined normalize and truncate did not produce expected result"


def test_repr_failure_handling():
    """If the repr function raises an exception, the function should return 'REPR FAILED'."""
    class BadRepr:
        def __repr__(self):
            raise RuntimeError("cannot represent")

    # Use the default repr function (which will call __repr__ and raise)
    result = get_shortish_repr(BadRepr())
    assert result == "REPR FAILED", "Failed repr did not return the expected placeholder"

    # Ensure that even with normalize or max_length, the placeholder is returned unchanged
    result_norm = get_shortish_repr(BadRepr(), normalize=True, max_length=5)
    assert result_norm == "REPR FAILED", "Placeholder altered by normalize or max_length"
