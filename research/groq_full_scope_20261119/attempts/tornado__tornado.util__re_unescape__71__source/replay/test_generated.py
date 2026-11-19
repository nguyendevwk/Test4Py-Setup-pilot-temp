import re
import pytest
from tornado.util import re_unescape

def test_re_unescape_roundtrip():
    # Escape a complex string and ensure unescaping restores the original
    original = r"Hello, (world)! 100% \[test\] \d+"
    escaped = re.escape(original)
    # The escaped string should contain only literal characters and escaped metacharacters
    assert escaped != original
    # Unescape should return the original string
    unescaped = re_unescape(escaped)
    assert unescaped == original

def test_re_unescape_invalid_pattern():
    # Patterns containing \d, \w, etc. cannot be produced by re.escape
    invalid = r"foo\dbar"
    with pytest.raises(ValueError):
        re_unescape(invalid)

def test_re_unescape_empty_string():
    # Unescaping an empty string should simply return an empty string
    assert re_unescape("") == ""
