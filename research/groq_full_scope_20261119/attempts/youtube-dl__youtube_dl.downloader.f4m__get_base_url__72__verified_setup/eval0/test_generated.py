import pytest
from youtube_dl.downloader.f4m import get_base_url
from youtube_dl.compat import compat_etree_fromstring

def test_get_base_url_returns_trimmed_value():
    xml = """
    <manifest>
        <baseURL>   https://example.com/stream/   </baseURL>
    </manifest>
    """
    tree = compat_etree_fromstring(xml)
    assert get_base_url(tree) == "https://example.com/stream/"

def test_get_base_url_returns_none_when_missing():
    xml = """
    <manifest>
        <other>data</other>
    </manifest>
    """
    tree = compat_etree_fromstring(xml)
    assert get_base_url(tree) is None

def test_get_base_url_prefers_first_namespace_variant():
    xml = """
    <manifest xmlns:ns="http://example.com/ns">
        <ns:baseURL>https://ns.example.com/</ns:baseURL>
        <baseURL>https://default.example.com/</baseURL>
    </manifest>
    """
    tree = compat_etree_fromstring(xml)
    # The function should return the first matching element, which is the namespaced one
    assert get_base_url(tree) == "https://ns.example.com/"
