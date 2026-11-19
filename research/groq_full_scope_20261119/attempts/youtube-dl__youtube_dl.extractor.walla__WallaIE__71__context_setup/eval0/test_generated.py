import re
import xml.etree.ElementTree as ET
import pytest
from youtube_dl.extractor.walla import WallaIE


class DummyWallaIE(WallaIE):
    """Subclass that overrides _download_xml to return a custom XML tree."""

    def __init__(self, xml_root):
        super().__init__()
        self._xml_root = xml_root

    def _download_xml(self, url, display_id):
        # Ignore url and display_id; return the pre-built XML root
        return self._xml_root


def build_xml(title, synopsis, preview_pic, duration, subtitles, qualities):
    """Helper to build an XML ElementTree root for testing."""
    root = ET.Element("video")
    items = ET.SubElement(root, "items")
    item = ET.SubElement(items, "item")
    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "synopsis").text = synopsis
    ET.SubElement(item, "preview_pic").text = preview_pic
    ET.SubElement(item, "duration").text = duration

    sub_el = ET.SubElement(item, "subtitles")
    for lang, src in subtitles:
        sub_item = ET.SubElement(sub_el, "subtitle")
        ET.SubElement(sub_item, "title").text = lang
        ET.SubElement(sub_item, "src").text = src

    qual_el = ET.SubElement(item, "qualities")
    for q_title, q_src in qualities:
        q_item = ET.SubElement(qual_el, "quality")
        ET.SubElement(q_item, "title").text = q_title
        ET.SubElement(q_item, "src").text = q_src

    return ET.ElementTree(root).getroot()


def test_normal_extraction(tmp_path):
    """Test normal extraction with all fields present."""
    xml_root = build_xml(
        title="Test Video",
        synopsis="A test description",
        preview_pic="http://example.com/thumb.jpg",
        duration="120",
        subtitles=[("עברית", "http://example.com/sub_heb.srt")],
        qualities=[("720p", "playpath_720"), ("480p", "playpath_480")],
    )
    extractor = DummyWallaIE(xml_root)

    url = "http://vod.walla.co.il/movie/123456/test-video"
    result = extractor._real_extract(url)

    assert result["id"] == "123456"
    assert result["display_id"] == "test-video"
    assert result["title"] == "Test Video"
    assert result["description"] == "A test description"
    assert result["thumbnail"] == "http://example.com/thumb.jpg"
    assert result["duration"] == 120

    # Check subtitles mapping
    assert "heb" in result["subtitles"]
    assert result["subtitles"]["heb"][0]["url"] == "http://example.com/sub_heb.srt"

    # Check formats
    formats = result["formats"]
    assert len(formats) == 2
    heights = {f["height"] for f in formats}
    assert heights == {720, 480}
    for f in formats:
        assert f["url"] == "rtmp://wafla.walla.co.il/vod"
        assert f["player_url"] == "http://isc.walla.co.il/w9/swf/video_swf/vod/WallaMediaPlayerAvod.swf"
        assert f["page_url"] == url
        assert f["ext"] == "flv"


def test_missing_subtitle_and_quality(tmp_path):
    """Test extraction when subtitles or qualities are missing."""
    xml_root = build_xml(
        title="No Subtitles",
        synopsis="No subtitles here",
        preview_pic="http://example.com/no_sub.jpg",
        duration="60",
        subtitles=[],  # No subtitles
        qualities=[("360p", "playpath_360")],  # Single quality
    )
    extractor = DummyWallaIE(xml_root)

    url = "http://vod.walla.co.il/movie/654321/no-subtitles"
    result = extractor._real_extract(url)

    assert result["id"] == "654321"
    assert result["display_id"] == "no-subtitles"
    assert result["title"] == "No Subtitles"
    assert result["description"] == "No subtitles here"
    assert result["thumbnail"] == "http://example.com/no_sub.jpg"
    assert result["duration"] == 60

    # No subtitles should result in empty dict
    assert result["subtitles"] == {}

    # One format with height 360
    formats = result["formats"]
    assert len(formats) == 1
    assert formats[0]["height"] == 360
    assert formats[0]["play_path"] == "playpath_360"


def test_invalid_url_raises():
    """Test that an invalid URL raises a ValueError."""
    xml_root = build_xml(
        title="Dummy",
        synopsis="Dummy",
        preview_pic="http://example.com/dummy.jpg",
        duration="30",
        subtitles=[],
        qualities=[],
    )
    extractor = DummyWallaIE(xml_root)

    invalid_url = "http://invalid.com/notmatching/123"
    with pytest.raises(ValueError):
        extractor._real_extract(invalid_url)
