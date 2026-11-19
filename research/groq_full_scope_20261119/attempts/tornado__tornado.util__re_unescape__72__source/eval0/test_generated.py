import re
import pytest
from tornado.util import re_unescape

def test_re_unescape_normal():
    original = "Hello, World! 123"
    escaped = re.escape(original)
    assert escaped != original
    unescaped = re_unescape(escaped)
    assert unescaped == original

def test_re_unescape_backslashes():
    original = r"Path\to\file"
    escaped = re.escape(original)
    # escaped should contain double backslashes
    assert r"\\\\" in escaped
    unescaped = re_unescape(escaped)
    assert unescaped == original

def test_re_unescape_invalid_pattern():
    # \d cannot be produced by re.escape, should raise ValueError
    with pytest.raises(ValueError):
        re_unescape(r"\d")
