import pytest
import html
from tornado.escape import xhtml_escape, to_unicode

def test_xhtml_escape_string():
    # Normal string with characters that need escaping
    raw = '<div class="test" data=\'value & more\'></div>'
    escaped = xhtml_escape(raw)
    # html.escape would escape <, >, &, " but not single quotes; xhtml_escape should also escape single quotes
    expected = html.escape(raw, quote=True).replace("'", "&#x27;")
    assert escaped == expected
    assert isinstance(escaped, str)

def test_xhtml_escape_bytes():
    # Bytes input should be decoded to UTF-8 and escaped
    raw_bytes = b'<span title="foo & bar">baz</span>'
    escaped = xhtml_escape(raw_bytes)
    expected = html.escape(raw_bytes.decode('utf-8'), quote=True).replace("'", "&#x27;")
    assert escaped == expected
    assert isinstance(escaped, str)

def test_xhtml_escape_invalid_type():
    # Passing an unsupported type should raise TypeError
    with pytest.raises(TypeError):
        xhtml_escape(123)  # int is not a valid input type
