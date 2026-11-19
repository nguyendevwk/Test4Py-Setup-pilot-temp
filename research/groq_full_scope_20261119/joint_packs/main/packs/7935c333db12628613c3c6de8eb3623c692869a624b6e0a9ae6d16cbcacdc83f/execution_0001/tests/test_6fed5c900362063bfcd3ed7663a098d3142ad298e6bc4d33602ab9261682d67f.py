import pytest
import html
from tornado.escape import xhtml_escape

def test_xhtml_escape_string_and_bytes():
    # Normal string with special characters
    s = '<div class="test" id=\'foo\' & bar>'
    escaped = xhtml_escape(s)
    # html.escape escapes <, >, &, " and ' (as &#x27; in newer versions)
    expected = html.escape(s)
    assert escaped == expected
    assert isinstance(escaped, str)

    # Bytes input should be decoded to str and escaped
    b = b'<span data=\'value\' & more>'
    escaped_bytes = xhtml_escape(b)
    expected_bytes = html.escape(b.decode('utf-8'))
    assert escaped_bytes == expected_bytes
    assert isinstance(escaped_bytes, str)

def test_xhtml_escape_boundary_characters():
    # Test that all characters that need escaping are handled
    raw = '<>&"\''  # includes all special chars
    escaped = xhtml_escape(raw)
    # html.escape will convert < > & to &lt; &gt; &amp; and " to &quot;
    # Single quote is converted to &#x27; in newer versions
    expected = '&lt;&gt;&amp;&quot;&#x27;'
    assert escaped == expected

def test_xhtml_escape_invalid_input():
    # Passing an unsupported type should raise a TypeError
    with pytest.raises(TypeError):
        xhtml_escape(123)  # int is not str or bytes
