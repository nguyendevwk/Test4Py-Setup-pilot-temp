import pytest
import html
from tornado.escape import xhtml_escape

def test_xhtml_escape_string_and_bytes():
    # Normal string with special characters
    original = '<div class="test" data=\'value & more\'></div>'
    escaped = xhtml_escape(original)
    # html.escape escapes <, >, &, " and ' (as &#x27; in newer versions)
    expected = html.escape(original, quote=True)
    assert escaped == expected
    assert isinstance(escaped, str)

    # Bytes input should be decoded to str and escaped
    original_bytes = b'<span id="1">Hello & "world"</span>'
    escaped_bytes = xhtml_escape(original_bytes)
    expected_bytes = html.escape(original_bytes.decode('utf-8'), quote=True)
    assert escaped_bytes == expected_bytes
    assert isinstance(escaped_bytes, str)

def test_xhtml_escape_boundary_characters():
    # Test that all characters that need escaping are handled
    special_chars = '<>&"\''  # includes single quote
    escaped = xhtml_escape(special_chars)
    # html.escape will convert single quote to &#x27; in newer versions
    expected = html.escape(special_chars, quote=True)
    assert escaped == expected
    # Ensure no unescaped characters remain
    assert all(c not in escaped for c in '<>&"\'')

def test_xhtml_escape_invalid_input():
    # Passing an unsupported type should raise a TypeError
    with pytest.raises(TypeError):
        xhtml_escape(123)  # int is not str or bytes
