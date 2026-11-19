import pytest
import html
from tornado.escape import xhtml_escape

def test_xhtml_escape_string_and_bytes():
    # Normal string with special characters
    raw = '<div class="test" data=\'value & more\'></div>'
    escaped = xhtml_escape(raw)
    # All special characters should be escaped
    assert escaped == html.escape(raw)
    assert escaped == '&lt;div class=&quot;test&quot; data=&#x27;value &amp; more&#x27;&gt;&lt;/div&gt;'
    # Bytes input should be decoded and escaped, result is str
    raw_bytes = b'<span>foo & bar</span>'
    escaped_bytes = xhtml_escape(raw_bytes)
    assert isinstance(escaped_bytes, str)
    assert escaped_bytes == '&lt;span&gt;foo &amp; bar&lt;/span&gt;'

def test_xhtml_escape_boundary_characters():
    # Test that single quotes are escaped as &#x27; and ampersand as &amp;
    boundary = "'&<>\""
    escaped = xhtml_escape(boundary)
    assert escaped == '&#x27;&amp;&lt;&gt;&quot;'
    # Ensure that no double escaping occurs
    double_escaped = xhtml_escape(escaped)
    assert double_escaped == escaped

def test_xhtml_escape_invalid_input():
    # Passing an unsupported type should raise a TypeError
    with pytest.raises(TypeError):
        xhtml_escape(123)
