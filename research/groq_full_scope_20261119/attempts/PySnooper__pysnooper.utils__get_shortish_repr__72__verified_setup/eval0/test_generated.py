import pytest
from pysnooper.utils import get_shortish_repr


def test_custom_repr_and_truncation():
    """Custom repr should override default and max_length should truncate."""
    # Custom repr for list objects
    custom_repr = (
        list,
        lambda x: f"CUSTOM LIST with {len(x)} items",
    )
    result = get_shortish_repr([1, 2, 3], custom_repr=custom_repr, max_length=20)
    # The custom repr is used and then truncated if necessary
    assert result == "CUSTOM LIST with 3 items"
    # Ensure that truncation works when the string is longer
    long_custom = lambda x: "X" * 50
    result_long = get_shortish_repr([1], custom_repr=(list, long_custom), max_length=10)
    assert result_long == "XXXXXXXXXX"


def test_repr_failure_handling():
    """If __repr__ raises, the function should return 'REPR FAILED'."""
    class BadRepr:
        def __repr__(self):
            raise ValueError("cannot represent")

    bad = BadRepr()
    result = get_shortish_repr(bad)
    assert result == "REPR FAILED"


def test_newline_and_carriage_return_removal():
    """Newline and carriage return characters in the repr output should be removed."""
    # Custom repr that returns a string containing actual newline and carriage return
    def custom_repr_with_newlines(x):
        return "line1\nline2\rline3"

    result = get_shortish_repr("ignored", custom_repr=(str, custom_repr_with_newlines))
    # The returned string should have all '\n' and '\r' removed
    assert result == "line1line2line3"
