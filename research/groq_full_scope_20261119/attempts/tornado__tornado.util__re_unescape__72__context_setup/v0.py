import re
import pytest
from tornado.util import re_unescape

def test_re_unescape_basic():
    # re.escape turns "a.b" into "a\\.b". re_unescape should reverse it.
    escaped = re.escape("a.b")
    assert escaped == r"a\.b"
    unescaped = re_unescape(escaped)
    assert unescaped == "a.b"

def test_re_unescape_backslash():
    # Escaping a backslash results in "\\\\"; unescape should return a single backslash.
    escaped = re.escape("\\")
    assert escaped == r"\\"
    unescaped = re_unescape(escaped)
    assert unescaped == "\\"

def test_re_unescape_invalid():
    # Strings containing escaped alphanumerics cannot be produced by re.escape,
    # so re_unescape should raise ValueError.
    with pytest.raises(ValueError, match=r"cannot unescape '\\d'"):
        re_unescape(r"\d")
