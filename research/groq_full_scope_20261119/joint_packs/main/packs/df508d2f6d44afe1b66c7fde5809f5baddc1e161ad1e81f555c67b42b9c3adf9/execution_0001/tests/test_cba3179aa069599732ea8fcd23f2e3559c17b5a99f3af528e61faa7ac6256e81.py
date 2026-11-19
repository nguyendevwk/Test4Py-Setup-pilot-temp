import pytest
import html
from tornado.escape import xhtml_escape

def test_xhtml_escape_string_and_bytes():
    # Normal string with special characters
    raw = '<div class="test" data=\'value & more\'></div>'
    escaped = xhtml_escape(raw)
    # Ensure all special characters are escaped
    assert escaped == '&lt;div class=&quot;test&quot; data=&#x27;value &amp; more&#x27;&gt;&lt;/div&gt;'
    # Bytes input should also return a string
    raw_bytes = b'<p>hello & world</p>'
    escaped_bytes = xhtml_escape(raw_bytes)
    assert isinstance(escaped_bytes, str)
    assert escaped_bytes == '&lt;p&gt;hello &amp; world&lt;/p&gt;'

def test_xhtml_escape_boundary_characters():
    # Test boundary characters: < > " ' &
    boundary = '<>"\'&'
    expected = '&lt;&gt;&quot;&#x27;&amp;'
    assert xhtml_escape(boundary) == expected

def test_xhtml_escape_invalid_input():
    # Passing an unsupported type should raise a TypeError
    with pytest.raises(TypeError):
        xhtml_escape(12345)
