import re
import pytest
from tornado.util import re_unescape

def test_re_unescape_roundtrip():
    original = "Hello, World! 123 + *?^$"
    escaped = re.escape(original)
    unescaped = re_unescape(escaped)
    assert unescaped == original, "re_unescape should return the original string after escaping"

def test_re_unescape_invalid_pattern():
    # \d is not produced by re.escape, should raise ValueError
    invalid = r"\d"
    with pytest.raises(ValueError):
        re_unescape(invalid)

def test_re_unescape_empty_string():
    assert re_unescape("") == "", "Empty string should be returned unchanged"
