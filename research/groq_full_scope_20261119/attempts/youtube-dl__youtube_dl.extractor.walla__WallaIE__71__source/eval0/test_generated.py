import re
import xml.etree.ElementTree as ET
import pytest
from youtube_dl.extractor.walla import WallaIE


def _make_xml():
    return """<?xml version="1.0"?>
<video>
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
        <quality>
          <title>low</title>
          <src>playpath_low</src>
        </quality>
      </qualities>
    </item>
  </items>
</video>"""


def test_walla_ie_normal_extraction(tmp_path):
    """Test normal extraction with subtitles and multiple formats."""
    xml_data = _make_xml()
    tree = ET.ElementTree(ET.fromstring(xml_data))

    def fake_download_xml(url, display_id):
        assert url.startswith("http://video2.walla.co.il/")
        return tree

    ie = WallaIE()
    ie._download_xml = fake_download_xml

    url = "http://vod.walla.co.il/movie/123456/test-title"
    result = ie._real_extract(url)

    assert result["id"] == "123456"
    assert result["display_id"] == "test-title"
    assert result["title"] == "Test Title"
    assert result["description"] == "Test Description"
    assert result["thumbnail"] == "http://example.com/thumb.jpg"
    assert result["duration"] == 120

    # Subtitles
    subtitles = result["subtitles"]
    assert "heb" in subtitles
    assert subtitles["heb"][0]["url"] == "http://example.com/subs.heb.srt"
    assert "English" in subtitles
    assert subtitles["English"][0]["url"] == "http://example.com/subs.eng.srt"

    # Formats
    formats = result["formats"]
    assert len(formats) == 3
    for f in formats:
        assert f["url"] == "rtmp://wafla.walla.co.il/vod"
        assert f["player_url"] == "http://isc.walla.co.il/w9/swf/video_swf/vod/WallaMediaPlayerAvod.swf"
        assert f["page_url"] == url
        assert f["ext"] == "flv"
    # Check height parsing
    heights = {f["format_id"]: f.get("height") for f in formats}
    assert heights["720p"] == 720
    assert heights["480p"] == 480
    assert heights["low"] is None


def test_walla_ie_missing_subtitles(tmp_path):
    """Test extraction when no subtitles are present."""
    xml_data = """<?xml version="1.0"?>
<video>
  <items>
    <item>
      <title>NoSubs</title>
      <synopsis>No description</synopsis>
      <preview_pic>http://example.com/no.jpg</preview_pic>
      <duration>60</duration>
      <subtitles/>
      <qualities>
        <quality>
          <title>360p</title>
          <src>playpath_360</src>
        </quality>
      </qualities>
    </item>
  </items>
</video>"""
    tree = ET.ElementTree(ET.fromstring(xml_data))

    def fake_download_xml(url, display_id):
        return tree

    ie = WallaIE()
    ie._download_xml = fake_download_xml

    url = "http://vod.walla.co.il/movie/654321/no-subs"
    result = ie._real_extract(url)

    assert result["subtitles"] == {}
    assert len(result["formats"]) == 1
    fmt = result["formats"][0]
    assert fmt["format_id"] == "360p"
    assert fmt["height"] == 360


def test_walla_ie_invalid_url_raises():
    """Test that an invalid URL raises an AttributeError due to missing match."""
    ie = WallaIE()
    with pytest.raises(AttributeError):
        ie._real_extract("http://invalid.url/notmatching")
