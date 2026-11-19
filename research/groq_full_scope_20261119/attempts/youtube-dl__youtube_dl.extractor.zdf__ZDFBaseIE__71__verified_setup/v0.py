import json
import re
import pytest
from youtube_dl.extractor.zdf import ZDFBaseIE
from youtube_dl.utils import determine_ext, parse_codecs, qualities, NO_DEFAULT


class DummyZDFIE(ZDFBaseIE):
    """A minimal subclass that allows us to call protected methods."""
    def __init__(self):
        super().__init__()
        self._download_json_calls = []

    def _download_json(self, url, video_id, note, headers=None):
        self._download_json_calls.append((url, video_id, note, headers))
        # Return a dummy JSON structure that mimics the real API response
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
                                            {
                                                "uri": "http://example.com/audio.mp4",
                                                "language": "deu"
                                            }
                                        ]
                                    },
                                    "quality": "high"
                                }
                            ],
                            "type": "audio",
                            "mimeType": "video/mp4"
                        }
                    ]
                }
            ],
            "attributes": {
                "duration": {"value": 120000}  # milliseconds
            },
            "captions": [
                {"uri": "http://example.com/sub_de.vtt", "language": "deu"},
                {"uri": "http://example.com/sub_en.vtt", "language": "eng"}
            ]
        }


def test_extract_subtitles_basic():
    """Test that subtitles are extracted correctly from a JSON structure."""
    ie = DummyZDFIE()
    json_data = {
        "captions": [
            {"uri": "http://example.com/sub_de.vtt", "language": "deu"},
            {"uri": "http://example.com/sub_en.vtt", "language": "eng"},
            {"uri": None, "language": "deu"},  # should be ignored
        ]
    }
    subtitles = ie._extract_subtitles(json_data)
    assert "deu" in subtitles
    assert "eng" in subtitles
    assert len(subtitles["deu"]) == 1
    assert subtitles["deu"][0]["url"] == "http://example.com/sub_de.vtt"
    assert subtitles["eng"][0]["url"] == "http://example.com/sub_en.vtt"


def test_extract_format_m3u8_and_duplicate():
    """Test that _extract_format handles m3u8 URLs and ignores duplicates."""
    ie = DummyZDFIE()
    formats = []
    format_urls = set()
    meta = {
        "url": "http://example.com/stream.m3u8",
        "mimeType": "application/x-mpegURL",
        "type": "video",
        "quality": "hd",
        "mimeCodec": "avc1.64001f",
        "language": "deu"
    }
    # First extraction should add formats
    ie._extract_format("vid123", formats, format_urls, meta)
    assert len(formats) > 0
    # Second extraction with same URL should not add new formats
    prev_len = len(formats)
    ie._extract_format("vid123", formats, format_urls, meta)
    assert len(formats) == prev_len


def test_extract_ptmd_with_mocked_api_and_duration():
    """Test that _extract_ptmd correctly processes mocked API data and calculates duration."""
    ie = DummyZDFIE()
    # Use the dummy _download_json implementation
    result = ie._extract_ptmd(
        ptmd_url="http://example.com/api/ptmd",
        video_id="vid123",
        api_token="dummy_token",
        referrer="http://example.com"
    )
    # Check that the extractor key matches the subclass key
    assert result["extractor_key"] == DummyZDFIE.ie_key()
    # The id should come from the mocked basename
    assert result["id"] == "dummy_id"
    # Duration should be converted from milliseconds to seconds
    assert result["duration"] == 120.0
    # Formats should contain at least one entry
    assert isinstance(result["formats"], list)
    assert len(result["formats"]) >= 1
    # Subtitles should be extracted correctly
    subtitles = result["subtitles"]
    assert "deu" in subtitles
    assert "eng" in subtitles
    assert subtitles["deu"][0]["url"] == "http://example.com/sub_de.vtt"
    assert subtitles["eng"][0]["url"] == "http://example.com/sub_en.vtt"
