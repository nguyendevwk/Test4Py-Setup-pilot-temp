import pytest
from tornado.util import re_unescape


def test_re_unescape_basic():
    # Escape a simple regex pattern and then unescape it
    original = r"foo.bar+b?c*d(e)f|g"
    escaped = re.escape(original)
    # re_unescape should return the original string
    assert re_unescape(escaped) == original


def test_re_unescape_backslash_and_boundary():
    # Test unescaping a string that contains only escaped backslashes
    escaped = r"\\"
    # re.escape would produce r"\\\\"; re_unescape should return a single backslash
    assert re_unescape(escaped) == "\\"


def test_re_unescape_invalid_pattern_raises():
    # Strings containing \d cannot be produced by re.escape and should raise ValueError
    invalid = r"\d+"
    with pytest.raises(ValueError):
        re_unescape(invalid)
