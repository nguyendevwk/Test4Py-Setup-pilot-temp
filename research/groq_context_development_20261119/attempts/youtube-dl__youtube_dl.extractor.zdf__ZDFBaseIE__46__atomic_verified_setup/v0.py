import json
import re
import pytest
from youtube_dl.extractor.zdf import ZDFBaseIE
from youtube_dl.utils import determine_ext, parse_codecs, qualities
from youtube_dl.compat import compat_str

class DummyZDFIE(ZDFBaseIE):
    """A minimal subclass to expose protected methods for testing."""
    def __init__(self):
        super().__init__()
        # Dummy downloader attributes
        self._downloader = None

    # Override _download_json to avoid network calls
    def _download_json(self, url, video_id, note, headers=None):
        return {"dummy": "data"}

    # Override _parse_json to avoid network calls
    def _parse_json(self, json_str, video_id):
        return json.loads(json_str)

    # Override _search_regex to avoid network calls
    def _search_regex(self, pattern, string, name, default=None, fatal=True, group=None):
        return default

def test_extract_subtitles_basic():
    """Verify that subtitles are extracted correctly from a simple JSON structure."""
    ie = DummyZDFIE()
    src = {
        "captions": [
            {"uri": "http://example.com/sub1.srt", "language": "eng"},
            {"uri": "http://example.com/sub2.srt", "language": "deu"},
            {"uri": None, "language": "fra"},
            {"uri": "http://example.com/sub3.srt"}  # default language
        ]
    }
    subs = ie._extract_subtitles(src)
    assert isinstance(subs, dict)
    assert subs["eng"] == [{"url": "http://example.com/sub1.srt"}]
    assert subs["deu"] == [{"url": "http://example.com/sub2.srt"}]
    assert subs["fra"] == []  # no valid URL
    assert subs["deu"] == [{"url": "http://example.com/sub2.srt"}]
    assert subs["deu"] == [{"url": "http://example.com/sub2.srt"}]
    # default language should be 'deu' if not specified
    assert subs["deu"] == [{"url": "http://example.com/sub3.srt"}]

def test_extract_format_m3u8_and_duplicate():
    """Test that _extract_format handles m3u8 URLs and ignores duplicates."""
    ie = DummyZDFIE()
    formats = []
    format_urls = set()
    meta = {
        "url": "http://example.com/stream.m3u8",
        "mimeType": "application/x-mpegURL",
        "type": "video",
        "quality": "high",
        "mimeCodec": "avc1.64001F",
        "language": "eng"
    }
    # First extraction should add m3u8 formats
    ie._extract_format("vid123", formats, format_urls, meta)
    assert any(f.get("format_id") == "hls" for f in formats)
    # Duplicate URL should not add again
    prev_len = len(formats)
    ie._extract_format("vid123", formats, format_urls, meta)
    assert len(formats) == prev_len

def test_extract_ptmd_structure_and_sorting():
    """Ensure _extract_ptmd returns expected structure and sorts formats."""
    ie = DummyZDFIE()
    # Mock _call_api to return a controlled response
    def mock_call_api(url, video_id, item, api_token=None, referrer=None):
        return {
            "basename": "testvideo",
            "priorityList": [
                {
                    "formitaeten": [
                        {
                            "type": "video",
                            "mimeType": "video/mp4",
                            "qualities": [
                                {
                                    "quality": "low",
                                    "audio": {"tracks": [
                                        {"uri": "http://example.com/low.mp4", "language": "deu"},
                                        {"uri": "http://example.com/low2.mp4", "language": "eng"}
                                    ]}
                                },
                                {
                                    "quality": "high",
                                    "audio": {"tracks": [
                                        {"uri": "http://example.com/high.mp4", "language": "deu"}
                                    ]}
                                }
                            ]
                        }
                    ]
                }
            ],
            "attributes": {
                "duration": {"value": 120000}  # milliseconds
            },
            "captions": [
                {"uri": "http://example.com/sub.srt", "language": "eng"}
            ]
        }
    ie._call_api = mock_call_api

    result = ie._extract_ptmd("http://example.com/api", "vid123", None, None)

    assert result["extractor_key"] == "ZDFIE"
    assert result["id"] == "testvideo"
    assert result["duration"] == 120.0  # seconds
    assert "subtitles" in result
    assert "eng" in result["subtitles"]
    assert len(result["formats"]) == 3
    # Formats should be sorted by quality (high first)
    qualities_list = [f["quality"] for f in result["formats"]]
    assert qualities_list == sorted(qualities_list, reverse=True)
