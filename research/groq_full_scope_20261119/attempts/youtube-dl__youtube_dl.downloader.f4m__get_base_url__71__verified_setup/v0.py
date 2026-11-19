import io
import pytest
from youtube_dl.downloader.f4m import get_base_url
from youtube_dl.compat import compat_etree_fromstring, compat_etree_Element

def _make_manifest(xml_string: str):
    """Helper to parse XML string into an ElementTree element."""
    return compat_etree_fromstring(xml_string)

def test_get_base_url_returns_first_baseurl():
    xml = """
    <manifest>
        <baseURL>   http://example.com/stream/   </baseURL>
        <baseURL>http://example.com/other/</baseURL>
    </manifest>
    """
    manifest = _make_manifest(xml)
    assert get_base_url(manifest) == "http://example.com/stream/"

def test_get_base_url_returns_second_when_first_missing():
    xml = """
    <manifest>
        <baseURL>http://example.com/other/</baseURL>
    </manifest>
    """
    manifest = _make_manifest(xml)
    assert get_base_url(manifest) == "http://example.com/other/"

def test_get_base_url_returns_none_when_no_baseurl():
    xml = """
    <manifest>
        <mediaSegment>segment1.ts</mediaSegment>
    </manifest>
    """
    manifest = _make_manifest(xml)
    assert get_base_url(manifest) is None
