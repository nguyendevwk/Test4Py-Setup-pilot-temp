import re
import pytest
from tornado.util import re_unescape

def test_re_unescape_basic():
    # Escape a simple string and then unescape it
    original = "Hello, World! 123"
    escaped = re.escape(original)
    assert escaped != original  # ensure escaping actually changed the string
    unescaped = re_unescape(escaped)
    assert unescaped == original

def test_re_unescape_non_alphanum():
    # Escape a string containing a non-alphanumeric character (e.g., a dot)
    original = "file.name"
    escaped = re.escape(original)  # becomes 'file\\.name'
    assert escaped == r"file\.name"
    unescaped = re_unescape(escaped)
    assert unescaped == original
    # Ensure that the dot was correctly unescaped
    assert "." in unescaped and "\\" not in unescaped

def test_re_unescape_invalid_pattern():
    # A string containing an escaped digit cannot be produced by re.escape
    # and should raise ValueError when unescaped.
    invalid = r"\d"
    with pytest.raises(ValueError, match=r"cannot unescape '\\d'"):
        re_unescape(invalid)
