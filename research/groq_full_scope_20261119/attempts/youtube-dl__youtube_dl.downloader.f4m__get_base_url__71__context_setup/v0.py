import pytest
from youtube_dl.downloader.f4m import get_base_url, _add_ns
from youtube_dl.compat import compat_etree_fromstring

def test_get_base_url_returns_stripped_value():
    xml = f"""
    <manifest xmlns="http://ns.adobe.com/f4m/1.0">
        <baseURL>   https://example.com/video/   </baseURL>
    </manifest>
    """
    manifest = compat_etree_fromstring(xml)
    assert get_base_url(manifest) == "https://example.com/video/"

def test_get_base_url_returns_none_when_missing():
    xml = """
    <manifest xmlns="http://ns.adobe.com/f4m/1.0">
        <media>
            <duration>120000</duration>
        </media>
    </manifest>
    """
    manifest = compat_etree_fromstring(xml)
    assert get_base_url(manifest) is None

def test_get_base_url_prefers_first_baseURL_element():
    xml = f"""
    <manifest xmlns="http://ns.adobe.com/f4m/1.0">
        <baseURL>https://first.example.com/</baseURL>
        <baseURL>https://second.example.com/</baseURL>
    </manifest>
    """
    manifest = compat_etree_fromstring(xml)
    assert get_base_url(manifest) == "https://first.example.com/"
