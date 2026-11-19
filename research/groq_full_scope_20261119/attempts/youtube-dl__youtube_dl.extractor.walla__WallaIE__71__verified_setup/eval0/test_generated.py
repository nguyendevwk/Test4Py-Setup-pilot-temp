import re
import xml.etree.ElementTree as ET
import pytest
from youtube_dl.extractor.walla import WallaIE


def _make_xml(items_xml: str) -> ET.Element:
    """Helper to create a root XML element containing the given items XML."""
    root = ET.Element("root")
    root.append(ET.fromstring(items_xml))
    return root


def test_walla_ie_basic_extraction(monkeypatch):
    """Test normal extraction of title, description, thumbnail, duration, formats and subtitles."""
    xml_content = """
    <items>
        <item>
            <title>Test Title</title>
            <synopsis>Test Description</synopsis>
            <preview_pic>http://example.com/thumb.jpg</preview_pic>
            <duration>120</duration>
            <subtitles>
                <subtitle>
                    <title>עברית</title>
                    <src>http://example.com/subs.heb.srt</src>
                </subtitle>
                <subtitle>
                    <title>English</title>
                    <src>http://example.com/subs.eng.srt</src>
                </subtitle>
            </subtitles>
            <qualities>
                <quality>
                    <title>720p</title>
                    <src>playpath_720</src>
                </quality>
                <quality>
                    <title>480p</title>
                    <src>playpath_480</src>
                </quality>
            </qualities>
        </item>
    </items>
    """
    # Monkeypatch the download method to return our fake XML
    def fake_download_xml(url, display_id):
        return _make_xml(xml_content).find("./items/item")

    ie = WallaIE()
    monkeypatch.setattr(ie, "_download_xml", fake_download_xml)

    url = "http://vod.walla.co.il/movie/123456/test-title"
    result = ie._real_extract(url)

    assert result["id"] == "123456"
    assert result["display_id"] == "test-title"
    assert result["title"] == "Test Title"
    assert result["description"] == "Test Description"
    assert result["thumbnail"] == "http://example.com/thumb.jpg"
    assert result["duration"] == 120

    # Check formats
    formats = result["formats"]
    assert len(formats) == 2
    for fmt in formats:
        assert fmt["url"] == "rtmp://wafla.walla.co.il/vod"
        assert fmt["player_url"] == "http://isc.walla.co.il/w9/swf/video_swf/vod/WallaMediaPlayerAvod.swf"
        assert fmt["page_url"] == url
        assert fmt["ext"] == "flv"
        assert fmt["format_id"] in ("720p", "480p")
        assert fmt["height"] in (720, 480)

    # Check subtitles mapping
    subtitles = result["subtitles"]
    assert "heb" in subtitles
    assert subtitles["heb"][0]["url"] == "http://example.com/subs.heb.srt"
    assert "English" in subtitles
    assert subtitles["English"][0]["url"] == "http://example.com/subs.eng.srt"


def test_walla_ie_no_subtitles(monkeypatch):
    """Test extraction when no subtitles are present."""
    xml_content = """
    <items>
        <item>
            <title>No Subtitles</title>
            <synopsis>Desc</synopsis>
            <preview_pic>http://example.com/thumb.jpg</preview_pic>
            <duration>60</duration>
            <qualities>
                <quality>
                    <title>360p</title>
                    <src>playpath_360</src>
                </quality>
            </qualities>
        </item>
    </items>
    """
    def fake_download_xml(url, display_id):
        return _make_xml(xml_content).find("./items/item")

    ie = WallaIE()
    monkeypatch.setattr(ie, "_download_xml", fake_download_xml)

    url = "http://vod.walla.co.il/movie/654321/no-subtitles"
    result = ie._real_extract(url)

    assert result["subtitles"] == {}
    assert len(result["formats"]) == 1
    fmt = result["formats"][0]
    assert fmt["format_id"] == "360p"
    assert fmt["height"] == 360


def test_walla_ie_invalid_quality_format(monkeypatch):
    """Test that formats without a numeric height are still returned correctly."""
    xml_content = """
    <items>
        <item>
            <title>Invalid Quality</title>
            <synopsis>Desc</synopsis>
            <preview_pic>http://example.com/thumb.jpg</preview_pic>
            <duration>30</duration>
            <qualities>
                <quality>
                    <title>unknown</title>
                    <src>playpath_unknown</src>
                </quality>
            </qualities>
        </item>
    </items>
    """
    def fake_download_xml(url, display_id):
        return _make_xml(xml_content).find("./items/item")

    ie = WallaIE()
    monkeypatch.setattr(ie, "_download_xml", fake_download_xml)

    url = "http://vod.walla.co.il/movie/111111/invalid-quality"
    result = ie._real_extract(url)

    assert len(result["formats"]) == 1
    fmt = result["formats"][0]
    assert fmt["format_id"] == "unknown"
    assert "height" not in fmt
