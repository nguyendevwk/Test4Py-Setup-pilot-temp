import pytest
from youtube_dl.downloader.f4m import get_base_url
from youtube_dl.compat import compat_etree_fromstring

def _make_manifest(xml: str):
    """Helper to create an ElementTree element from XML string."""
    return compat_etree_fromstring(xml)

def test_get_base_url_single():
    """When a single <baseURL> element is present, its text is returned."""
    xml = """
    <manifest xmlns="http://ns.adobe.com/f4m/1.0">
        <baseURL>http://example.com/stream/</baseURL>
    </manifest>
    """
    manifest = _make_manifest(xml)
    assert get_base_url(manifest) == "http://example.com/stream/"

def test_get_base_url_second():
    """When a <baseURL> element with version 2 is present, its text is returned."""
    xml = """
    <manifest xmlns="http://ns.adobe.com/f4m/2.0">
        <baseURL>http://example.com/stream/</baseURL>
        <baseURL>http://example.com/stream2/</baseURL>
    </manifest>
    """
    manifest = _make_manifest(xml)
    # The function prefers the first matching element; here it should return the first one.
    assert get_base_url(manifest) == "http://example.com/stream/"

def test_get_base_url_none():
    """When no <baseURL> element is present, None is returned."""
    xml = """
    <manifest xmlns="http://ns.adobe.com/f4m/1.0">
        <media>
            <duration>1000</duration>
        </media>
    </manifest>
    """
    manifest = _make_manifest(xml)
    assert get_base_url(manifest) is None
