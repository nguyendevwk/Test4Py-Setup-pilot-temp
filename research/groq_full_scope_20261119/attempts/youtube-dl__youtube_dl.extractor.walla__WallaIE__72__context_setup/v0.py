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
                <duration>120</duration>
                <subtitles>
                    <subtitle>
                        <title>עברית</title>
                        <src>http://example.com/subs.hebrew.srt</src>
                    </subtitle>
                    <subtitle>
                        <title>English</title>
                        <src>http://example.com/subs.english.srt</src>
                    </subtitle>
                </subtitles>
                <qualities>
                    <quality>
                        <title>720p</title>
                        <src>playpath_720p</src>
                    </quality>
                    <quality>
                        <title>480p</title>
                        <src>playpath_480p</src>
                    </quality>
                </qualities>
            </item>
        </items>
    </video>
    """
    return ET.fromstring(xml_str)


def test_real_extract_parses_all_fields(tmp_path, sample_xml):
    """Test that _real_extract correctly parses all expected fields."""
    # Monkeypatch _download_xml to return our sample XML
    def fake_download_xml(self, url, display_id):
        assert url.startswith("http://video2.walla.co.il/?w=null/null/")
        assert display_id == "sample-video"
        return sample_xml

    WallaIE._download_xml = fake_download_xml

    extractor = WallaIE()
    result = extractor._real_extract(
        "http://vod.walla.co.il/movie/123456/sample-video"
    )

    assert result["id"] == "123456"
    assert result["display_id"] == "sample-video"
    assert result["title"] == "Sample Title"
    assert result["description"] == "Sample Description"
    assert result["thumbnail"] == "http://example.com/thumbnail.jpg"
    assert result["duration"] == 120

    # Check formats
    formats = result["formats"]
    assert len(formats) == 2
    for fmt in formats:
        assert fmt["url"] == "rtmp://wafla.walla.co.il/vod"
        assert fmt["player_url"] == "http://isc.walla.co.il/w9/swf/video_swf/vod/WallaMediaPlayerAvod.swf"
        assert fmt["page_url"] == "http://vod.walla.co.il/movie/123456/sample-video"
        assert fmt["ext"] == "flv"
        assert fmt["format_id"] in ("720p", "480p")
        assert fmt["height"] in (720, 480)

    # Check subtitles mapping
    subtitles = result["subtitles"]
    assert "heb" in subtitles
    assert subtitles["heb"][0]["url"] == "http://example.com/subs.hebrew.srt"
    assert "English" in subtitles
    assert subtitles["English"][0]["url"] == "http://example.com/subs.english.srt"


def test_real_extract_handles_missing_subtitles(tmp_path, sample_xml):
    """Test that _real_extract works when no subtitles are present."""
    # Remove subtitles element
    for sub in sample_xml.findall(".//subtitles"):
        sub.clear()

    def fake_download_xml(self, url, display_id):
        return sample_xml

    WallaIE._download_xml = fake_download_xml

    extractor = WallaIE()
    result = extractor._real_extract(
        "http://vod.walla.co.il/movie/654321/no-subtitles"
    )

    assert result["subtitles"] == {}


def test_real_extract_invalid_url_raises():
    """Test that passing an invalid URL raises an AttributeError due to missing match."""
    extractor = WallaIE()
    with pytest.raises(AttributeError):
        extractor._real_extract("http://invalid.url/notmatchingpattern")
