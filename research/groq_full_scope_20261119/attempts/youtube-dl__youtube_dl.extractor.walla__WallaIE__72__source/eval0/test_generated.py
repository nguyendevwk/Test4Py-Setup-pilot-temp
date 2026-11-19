import re
import xml.etree.ElementTree as ET
import pytest
from youtube_dl.extractor.walla import WallaIE


def _make_xml():
    return ET.fromstring(
        """
        <video>
            <items>
                <item>
                    <title>Test Title</title>
                    <synopsis>Test Description</synopsis>
                    <preview_pic>http://example.com/thumbnail.jpg</preview_pic>
                    <duration>120</duration>
                    <subtitles>
                        <subtitle>
                            <title>עברית</title>
                            <src>http://example.com/subs.srt</src>
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
        """)


def _patch_download_xml(ie, xml_root):
    def fake_download_xml(url, display_id):
        return xml_root
    ie._download_xml = fake_download_xml


def test_walla_ie_normal_extraction(tmp_path):
    url = "http://vod.walla.co.il/movie/123456/test-video"
    ie = WallaIE()
    _patch_download_xml(ie, _make_xml())
    result = ie._real_extract(url)

    assert result["id"] == "123456"
    assert result["display_id"] == "test-video"
    assert result["title"] == "Test Title"
    assert result["description"] == "Test Description"
    assert result["thumbnail"] == "http://example.com/thumbnail.jpg"
    assert result["duration"] == 120

    # Check subtitles mapping
    assert "heb" in result["subtitles"]
    assert result["subtitles"]["heb"][0]["url"] == "http://example.com/subs.srt"

    # Check formats
    formats = result["formats"]
    assert len(formats) == 2
    for fmt in formats:
        assert fmt["url"] == "rtmp://wafla.walla.co.il/vod"
        assert fmt["player_url"] == "http://isc.walla.co.il/w9/swf/video_swf/vod/WallaMediaPlayerAvod.swf"
        assert fmt["page_url"] == url
        assert fmt["ext"] == "flv"
        assert fmt["format_id"] in ("720p", "480p")
        if fmt["format_id"] == "720p":
            assert fmt["height"] == 720
        else:
            assert fmt["height"] == 480


def test_walla_ie_no_subtitles(tmp_path):
    xml_root = ET.fromstring(
        """
        <video>
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
        </video>
        """)
    url = "http://vod.walla.co.il/movie/654321/no-sub"
    ie = WallaIE()
    _patch_download_xml(ie, xml_root)
    result = ie._real_extract(url)

    assert result["subtitles"] == {}
    assert len(result["formats"]) == 1
    fmt = result["formats"][0]
    assert fmt["format_id"] == "360p"
    assert fmt["height"] == 360


def test_walla_ie_invalid_url_raises():
    ie = WallaIE()
    with pytest.raises(AttributeError):
        ie._real_extract("http://invalid.url/notmatching")
