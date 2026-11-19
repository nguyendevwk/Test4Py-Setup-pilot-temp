import pytest
from youtube_dl.downloader.f4m import get_base_url
from youtube_dl.compat import compat_etree_fromstring

def test_get_base_url_single_element(tmp_path):
    xml = """<manifest>
                <baseURL>http://example.com/video/</baseURL>
             </manifest>"""
    tree = compat_etree_fromstring(xml)
    assert get_base_url(tree) == "http://example.com/video/"

def test_get_base_url_multiple_elements(tmp_path):
    xml = """<manifest>
                <baseURL>http://first.com/</baseURL>
                <baseURL>http://second.com/</baseURL>
             </manifest>"""
    tree = compat_etree_fromstring(xml)
    # xpath_text returns the first matching element
    assert get_base_url(tree) == "http://first.com/"

def test_get_base_url_no_element(tmp_path):
    xml = """<manifest>
                <other>data</other>
             </manifest>"""
    tree = compat_etree_fromstring(xml)
    assert get_base_url(tree) is None
