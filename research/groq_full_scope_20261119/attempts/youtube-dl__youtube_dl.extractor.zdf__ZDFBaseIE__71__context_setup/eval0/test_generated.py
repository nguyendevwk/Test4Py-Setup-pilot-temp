import json
import re
import pytest
from youtube_dl.extractor.zdf import ZDFBaseIE
from youtube_dl.utils import determine_ext, parse_codecs, qualities

class DummyZDFIE(ZDFBaseIE):
    """A minimal subclass that allows us to test protected methods."""
    def __init__(self):
        super().__init__()
        # dummy downloader to satisfy base class init
        self._downloader = None

    def _download_json(self, url, video_id, note, headers=None):
        """Override to return a predefined JSON for testing."""
        return self._mock_json

@pytest.fixture
def dummy_ie():
    return DummyZDFIE()

def test_extract_subtitles_basic(dummy_ie):
    """Test that subtitles are extracted correctly from a simple payload."""
    src = {
        "captions": [
            {"uri": "http://example.com/sub1.srt", "language": "eng"},
            {"uri": "http://example.com/sub2.srt", "language": "deu"},
            {"uri": None, "language": "fre"},
            {"uri": "http://example.com/sub3.srt"},
        ]
    }
    subtitles = dummy_ie._extract_subtitles(src)
    assert "eng" in subtitles
    assert "deu" in subtitles
    assert "fre" not in subtitles  # uri was None
    assert len(subtitles["eng"]) == 1
    assert subtitles["eng"][0]["url"] == "http://example.com/sub1.srt"
    assert subtitles["deu"][0]["url"] == "http://example.com/sub2.srt"
    assert subtitles["deu"][0]["url"] == "http://example.com/sub2.srt"
    # default language for missing language field
    assert subtitles["deu"][0]["url"] == "http://example.com/sub2.srt"

def test_extract_format_m3u8_and_duplicate(dummy_ie):
    """Test that m3u8 URLs are processed and duplicates are ignored."""
    video_id = "vid123"
    formats = []
    format_urls = set()
    meta = {
        "url": "http://example.com/stream.m3u8",
        "mimeType": "application/x-mpegURL",
        "type": "video",
        "quality": "high",
        "language": "deu",
    }
    # First extraction should add m3u8 formats
    dummy_ie._extract_format(video_id, formats, format_urls, meta)
    assert any(f.get("url") == "http://example.com/stream.m3u8" for f in formats)
    # Second extraction with same URL should not add duplicates
    dummy_ie._extract_format(video_id, formats, format_urls, meta)
    assert len(formats) == 1  # no duplicate added

def test_extract_ptmd_with_mocked_api(dummy_ie):
    """Test _extract_ptmd processes mocked API response correctly."""
    # Mock API JSON
    dummy_ie._mock_json = {
        "basename": "content456",
        "priorityList": [
            {
                "formitaeten": [
                    {
                        "qualities": [
                            {
                                "audio": {
                                    "tracks": [
                                        {"uri": "http://example.com/audio.mp4", "language": "deu"},
                                        {"uri": "http://example.com/audio2.mp4", "language": "eng"},
                                    ]
                                },
                                "quality": "high",
                                "type": "video",
                                "mimeType": "video/mp4",
                            }
                        ]
                    }
                ]
            }
        ],
        "attributes": {
            "duration": {"value": 123456}  # milliseconds
        },
        "captions": [
            {"uri": "http://example.com/sub.srt", "language": "eng"}
        ]
    }

    result = dummy_ie._extract_ptmd(
        ptmd_url="http://api.example.com/ptmd/content456",
        video_id="vid123",
        api_token="dummy_token",
        referrer="http://referrer.example.com"
    )

    # Check extractor key and id
    assert result["extractor_key"] == dummy_ie.ie_key()
    assert result["id"] == "content456"

    # Duration should be converted to seconds
    assert result["duration"] == pytest.approx(123.456)

    # Formats should contain two entries with correct URLs
    urls = {f["url"] for f in result["formats"]}
    assert "http://example.com/audio.mp4" in urls
    assert "http://example.com/audio2.mp4" in urls

    # Subtitles should be extracted correctly
    assert "eng" in result["subtitles"]
    assert result["subtitles"]["eng"][0]["url"] == "http://example.com/sub.srt"
