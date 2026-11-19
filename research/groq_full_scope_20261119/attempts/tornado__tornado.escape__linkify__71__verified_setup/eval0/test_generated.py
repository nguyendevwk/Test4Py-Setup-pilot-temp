import pytest
from tornado.escape import linkify

def test_basic_linkify_and_html_escape():
    # Plain URL should be converted to an <a> tag and HTML escaped
    raw = 'Visit http://example.com?x=1&y=2 and <b>bold</b> text.'
    result = linkify(raw)
    assert '<a href="http://example.com?x=1&y=2">http://example.com?x=1&y=2</a>' in result
    # Ensure that the <b> tag is escaped
    assert '&lt;b&gt;bold&lt;/b&gt;' in result
    # No extra params should be added
    assert 'rel=' not in result

def test_shorten_long_url_and_title_attribute():
    # A very long URL should be shortened when shorten=True
    long_url = 'http://example.com/' + 'a'*100 + '?q=' + 'b'*50
    raw = f'Check this out: {long_url}'
    result = linkify(raw, shorten=True)
    # The displayed URL should be truncated and end with "..."
    assert result.count('...') == 1
    # The href should contain the full URL
    assert f'href="{long_url}"' in result
    # The title attribute should be present with the full href
    assert f'title="{long_url}"' in result

def test_require_protocol_and_callable_extra_params():
    # URLs without protocol should not be linkified when require_protocol=True
    raw = 'Visit www.example.com and http://good.com'
    result = linkify(raw, require_protocol=True)
    assert 'www.example.com' in result  # not linkified
    assert '<a href="http://good.com">http://good.com</a>' in result

    # Test callable extra_params that adds class based on domain
    def extra_cb(url):
        return 'class="internal"' if 'good.com' in url else 'class="external"'

    result = linkify(raw, require_protocol=True, extra_params=extra_cb)
    assert '<a href="http://good.com" class="internal">http://good.com</a>' in result
    # The non-protocol URL remains plain text
    assert 'www.example.com' in result
