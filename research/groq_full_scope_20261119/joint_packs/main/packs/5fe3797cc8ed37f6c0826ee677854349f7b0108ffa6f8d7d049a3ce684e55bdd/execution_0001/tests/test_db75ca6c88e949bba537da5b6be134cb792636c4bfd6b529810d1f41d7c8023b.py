import pytest
import html
from tornado.escape import xhtml_escape, to_unicode

def test_xhtml_escape_string():
    # Normal string with characters that need escaping
    raw = '<div class="test" data=\'value & more\'></div>'
    escaped = xhtml_escape(raw)
    # html.escape would produce the same but with &#39; for single quote
    expected = html.escape(raw, quote=True).replace("&#39;", "&#x27;")
    assert escaped == expected
    # Ensure the result is a str, not bytes
    assert isinstance(escaped, str)

def test_xhtml_escape_bytes():
    # Bytes input should be decoded and escaped
    raw_bytes = b'<p id="1">Hello & "world"</p>'
    escaped = xhtml_escape(raw_bytes)
    expected = html.escape(raw_bytes.decode('utf-8'), quote=True).replace("&#39;", "&#x27;")
    assert escaped == expected
    assert isinstance(escaped, str)

def test_xhtml_escape_invalid_type():
    # Passing an unsupported type should raise TypeError
    with pytest.raises(TypeError):
        xhtml_escape(123)  # int is not a valid input type
