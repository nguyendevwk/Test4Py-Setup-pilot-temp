import json
import re
import types
import pytest
from youtube_dl.extractor.zdf import ZDFBaseIE
from youtube_dl.utils import determine_ext, parse_codecs, qualities

class DummyIE(ZDFBaseIE):
    """A minimal subclass to expose protected methods for testing."""
    def __init__(self):
        super().__init__()
        self._download_json_calls = []

    def _download_json(self, url, video_id, note, headers=None):
        self._download_json_calls.append((url, video_id, note, headers))
        # Return a dummy JSON structure for ptmd tests
        return {
            "basename": "dummy_id",
            "priorityList": [
                {
                    "formitaeten": [
                        {
                            "qualities": [
                                {
                                    "audio": {
                                        "tracks": [
                                            {"uri": "https://example.com/track1.m3u8", "language": "deu"},
                                            {"uri": "https://example.com/track2.mp4", "language": "eng"},
                                        ]
                                    },
                                    "quality": "high",
                                    "type": "video",
                                    "mimeType": "application/x-mpegURL",
                                }
                            ]
                        }
                    ]
                }
            ],
            "attributes": {
                "duration": {"value": 120000}
            },
            "captions": [
                {"uri": "https://example.com/sub_de.vtt", "language": "deu"},
                {"uri": "https://example.com/sub_en.vtt", "language": "eng"},
            ],
        }

def test_extract_subtitles_basic():
    """Test that subtitles are extracted correctly from a simple JSON."""
    ie = DummyIE()
    src = {
        "captions": [
            {"uri": "https://example.com/sub_de.vtt", "language": "deu"},
            {"uri": "https://example.com/sub_en.vtt", "language": "eng"},
            {"uri": None, "language": "deu"},  # should be ignored
        ]
    }
    subtitles = ie._extract_subtitles(src)
    assert "deu" in subtitles
    assert "eng" in subtitles
    assert len(subtitles["deu"]) == 1
    assert subtitles["deu"][0]["url"] == "https://example.com/sub_de.vtt"
    assert subtitles["eng"][0]["url"] == "https://example.com/sub_en.vtt"

def test_extract_format_m3u8_and_f4m():
    """Test that _extract_format correctly handles m3u8 and f4m URLs."""
    ie = DummyIE()
    formats = []
    format_urls = set()
    # m3u8 case
    meta_m3u8 = {
        "url": "https://example.com/video.m3u8",
        "mimeType": "application/x-mpegURL",
        "quality": "auto",
        "type": "video",
        "mimeCodec": "avc1.64001F",
        "language": "deu",
    }
    ie._extract_format("vid123", formats, format_urls, meta_m3u8)
    # f4m case
    meta_f4m = {
        "url": "https://example.com/video.f4m",
        "mimeType": "application/f4m+xml",
        "quality": "high",
        "type": "video",
        "mimeCodec": "avc1.64001F",
        "language": "eng",
    }
    ie._extract_format("vid123", formats, format_urls, meta_f4m)
    # non-streaming case
    meta_mp4 = {
        "url": "https://example.com/video.mp4",
        "mimeType": "video/mp4",
        "quality": "low",
        "type": "video",
        "mimeCodec": "avc1.64001F",
        "language": "deu",
    }
    ie._extract_format("vid123", formats, format_urls, meta_mp4)

    # Verify that m3u8 and f4m formats were added via helper methods
    # They should be present in formats list
    m3u8_formats = [f for f in formats if f.get("format_id", "").startswith("hls")]
    f4m_formats = [f for f in formats if f.get("format_id", "").startswith("hds")]
    mp4_formats = [f for f in formats if f.get("format_id", "").startswith("http")]

    assert len(m3u8_formats) >= 1
    assert len(f4m_formats) >= 1
    assert len(mp4_formats) == 1
    mp4 = mp4_formats[0]
    assert mp4["url"] == "https://example.com/video.mp4"
    assert mp4["format_id"] == "http-video-low"
    assert mp4["quality"] == qualities(ie._QUALITIES)("low")

def test_extract_ptmd_integration():
    """Test that _extract_ptmd returns a fully populated result."""
    ie = DummyIE()
    result = ie._extract_ptmd(
        ptmd_url="https://api.zdf.de/ptmd/12345",
        video_id="vid123",
        api_token="dummy_token",
        referrer="https://www.zdf.de"
    )
    # Verify that _download_json was called with correct headers
    url, vid, note, headers = ie._download_json_calls[0]
    assert url == "https://api.zdf.de/ptmd/12345"
    assert vid == "vid123"
    assert headers["Api-Auth"] == "Bearer dummy_token"
    assert headers["Referer"] == "https://www.zdf.de"

    # Check result structure
    assert result["extractor_key"] == "ZDFIE"
    assert result["id"] == "dummy_id"
    assert result["duration"] == 120.0  # 120000 ms -> 120 s
    assert isinstance(result["formats"], list)
    assert len(result["formats"]) >= 1
    # Check that subtitles were extracted
    assert "deu" in result["subtitles"]
    assert "eng" in result["subtitles"]
    assert result["subtitles"]["deu"][0]["url"] == "https://example.com/sub_de.vtt"
