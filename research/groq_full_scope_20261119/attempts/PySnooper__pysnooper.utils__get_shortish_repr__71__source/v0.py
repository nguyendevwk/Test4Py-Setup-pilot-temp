import pytest
from pysnooper.utils import get_shortish_repr, get_repr_function, truncate, normalize_repr


def test_custom_repr_and_normalization(tmp_path):
    """Verify that a custom representation is used and that normalization
    does not alter the output when the custom repr is already short."""
    # Custom representation for integers
    custom_repr = (int, lambda x: f"int:{x}")
    result = get_shortish_repr(42, custom_repr=custom_repr, normalize=True)
    # The custom repr should be applied
    assert result == "int:42"
    # Normalization should not change the already short string
    assert normalize_repr(result) == result


def test_repr_failure_returns_placeholder():
    """When an object's __repr__ raises an exception, the function should
    return the placeholder string 'REPR FAILED'."""
    class BadRepr:
        def __repr__(self):
            raise RuntimeError("bad repr")

    bad_obj = BadRepr()
    result = get_shortish_repr(bad_obj)
    assert result == "REPR FAILED"


def test_truncation_of_long_string(tmp_path):
    """Ensure that the representation is truncated to the specified maximum
    length and that newlines are removed."""
    long_string = "a" * 100 + "\n" + "b" * 100
    # Use max_length to truncate to 10 characters
    result = get_shortish_repr(long_string, max_length=10)
    # The result should be the first 10 characters of the string without newlines
    assert result == ("a" * 10)
    # Verify that the newline was removed
    assert "\n" not in result
