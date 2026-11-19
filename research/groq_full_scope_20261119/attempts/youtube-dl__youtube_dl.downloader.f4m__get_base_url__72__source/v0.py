import pytest
from youtube_dl.downloader.f4m import get_base_url
from youtube_dl.compat import compat_etree_fromstring

# Helper to create an XML element from a string
def make_element(xml_str):
    return compat_etree_fromstring(xml_str)

def test_get_base_url_returns_stripped_value():
    xml = """
    <manifest>
        <baseURL>   http://example.com/video/   </baseURL>
    </manifest>
    """
    elem = make_element(xml)
    assert get_base_url(elem) == "http://example.com/video/"

def test_get_base_url_returns_none_when_missing():
    xml = """
    <manifest>
        <otherTag>value</otherTag>
    </manifest>
    """
    elem = make_element(xml)
    assert get_base_url(elem) is None

def test_get_base_url_handles_multiple_baseURL_tags():
    xml = """
    <manifest>
        <baseURL>http://first.com/</baseURL>
        <baseURL>http://second.com/</baseURL>
    </manifest>
    """
    elem = make_element(xml)
    # xpath_text returns the first matching element
    assert get_base_url(elem) == "http://first.com/"
