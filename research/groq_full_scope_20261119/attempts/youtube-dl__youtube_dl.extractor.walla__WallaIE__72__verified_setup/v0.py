import re
import xml.etree.ElementTree as ET

import pytest

from youtube_dl.extractor.walla import WallaIE


@pytest.fixture
def sample_xml():
    """Return an ElementTree Element representing a minimal Walla video XML."""
    xml_str = """
    <video>
        <items>
            <item>
                <title>Sample Title</title>
                <synopsis>Sample Description</synopsis>
                <preview_pic>http://example.com/thumbnail.jpg</preview_pic>
                <duration>1234</duration>
                <subtitles>
                    <subtitle>
                        <title>עברית</title>
                        <src>http://example.com/sub_heb.srt</src>
                    </subtitle>
                    <subtitle>
                        <title>English</title>
                        <src>http://example.com/sub_eng.srt</src>
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
    </video>
    """
    return ET.fromstring(xml_str)


def test_walla_ie_parses_expected_fields(tmp_path, sample_xml):
    """Test that WallaIE extracts all expected fields correctly."""
    # Monkeypatch _download_xml to return our sample XML
    def fake_download_xml(self, url, display_id):
        return sample_xml

    WallaIE._download_xml = fake_download_xml

    url = "http://vod.walla.co.il/movie/123456/sample-title"
    extractor = WallaIE()
    result = extractor._real_extract(url)

    assert result["id"] == "123456"
    assert result["display_id"] == "sample-title"
    assert result["title"] == "Sample Title"
    assert result["description"] == "Sample Description"
    assert result["thumbnail"] == "http://example.com/thumbnail.jpg"
    assert result["duration"] == 1234

    # Check formats
    formats = result["formats"]
    assert len(formats) == 2
    for fmt in formats:
        assert fmt["url"] == "rtmp://wafla.walla.co.il/vod"
        assert fmt["player_url"] == "http://isc.walla.co.il/w9/swf/video_swf/vod/WallaMediaPlayerAvod.swf"
        assert fmt["page_url"] == url
        assert fmt["ext"] == "flv"
        assert fmt["format_id"] in ("720p", "480p")
        assert "height" in fmt
        assert fmt["height"] in (720, 480)

    # Check subtitles mapping
    subtitles = result["subtitles"]
    assert "heb" in subtitles
    assert "English" in subtitles
    assert subtitles["heb"][0]["url"] == "http://example.com/sub_heb.srt"
    assert subtitles["English"][0]["url"] == "http://example.com/sub_eng.srt"


def test_walla_ie_handles_missing_subtitle_language(tmp_path, sample_xml):
    """Test that subtitles with an unmapped language are kept as-is."""
    # Remove Hebrew subtitle to force unmapped language
    for sub in sample_xml.findall(".//subtitle"):
        if sub.find("title").text == "עברית":
            sample_xml.remove(sub)

    def fake_download_xml(self, url, display_id):
        return sample_xml

    WallaIE._download_xml = fake_download_xml

    url = "http://vod.walla.co.il/movie/654321/another-title"
    extractor = WallaIE()
    result = extractor._real_extract(url)

    subtitles = result["subtitles"]
    # Only English subtitle remains, key should be 'English'
    assert "English" in subtitles
    assert "heb" not in subtitles
    assert subtitles["English"][0]["url"] == "http://example.com/sub_eng.srt"


def test_walla_ie_invalid_url_raises():
    """Test that an invalid URL causes an AttributeError due to missing regex groups."""
    extractor = WallaIE()
    with pytest.raises(AttributeError):
        extractor._real_extract("http://invalid.url/notmatchingpattern")
