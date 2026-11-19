import json
import re
import types
import pytest
from youtube_dl.extractor.zdf import ZDFBaseIE
from youtube_dl.utils import determine_ext, parse_codecs, qualities, NO_DEFAULT

class DummyIE(ZDFBaseIE):
    """Subclass to expose protected methods and mock network calls."""
    def __init__(self):
        super().__init__()
        self._download_json_called = False
        self._download_json_return = None

    def _download_json(self, url, video_id, note, headers=None):
        self._download_json_called = True
        return self._download_json_return

def test_extract_subtitles_basic():
    """Verify that subtitles are extracted correctly from a simple JSON."""
    ie = DummyIE()
    src = {
        "captions": [
            {"uri": "http://example.com/sub_de.vtt", "language": "deu"},
            {"uri": "http://example.com/sub_en.vtt", "language": "eng"},
            {"uri": None, "language": "fre"},
            {"uri": "http://example.com/sub_de2.vtt", "language": "deu"},
        ]
    }
    subs = ie._extract_subtitles(src)
    assert isinstance(subs, dict)
    assert subs == {
        "deu": [
            {"url": "http://example.com/sub_de.vtt"},
            {"url": "http://example.com/sub_de2.vtt"},
        ],
        "eng": [
            {"url": "http://example.com/sub_en.vtt"},
        ],
    }

def test_extract_format_m3u8_and_f4m():
    """Verify that _extract_format handles m3u8 and f4m URLs correctly."""
    ie = DummyIE()
    formats = []
    format_urls = set()
    # m3u8 case
    meta_m3u8 = {
        "url": "http://example.com/stream.m3u8",
        "mimeType": "application/x-mpegURL",
        "type": "video",
        "quality": "high",
        "language": "deu",
    }
    ie._extract_format("vid123", formats, format_urls, meta_m3u8)
    # f4m case
    meta_f4m = {
        "url": "http://example.com/stream.f4m",
        "mimeType": "application/f4m+xml",
        "type": "video",
        "quality": "low",
        "language": "eng",
    }
    ie._extract_format("vid123", formats, format_urls, meta_f4m)
    # normal case
    meta_http = {
        "url": "http://example.com/video.mp4",
        "mimeType": "video/mp4",
        "mimeCodec": "avc1.64001F",
        "type": "video",
        "quality": "med",
        "language": "deu",
    }
    ie._extract_format("vid123", formats, format_urls, meta_http)
    # ensure no duplicates
    assert len(format_urls) == 3
    # check that normal format has expected fields
    http_format = next(f for f in formats if f.get("url") == "http://example.com/video.mp4")
    assert http_format["format_id"] == "http-video-med"
    assert http_format["format_note"] == "med"
    assert http_format["quality"] == qualities(ie._QUALITIES)("med")
    assert http_format["language"] == "deu"
    assert http_format["preference"] == -10
    # ensure m3u8 and f4m formats are added via helper methods
    assert any(f.get("url") == "http://example.com/stream.m3u8" for f in formats)
    assert any(f.get("url") == "http://example.com/stream.f4m" for f in formats)

def test_extract_ptmd_and_sorting(tmp_path):
    """Verify that _extract_ptmd processes metadata correctly and sorts formats."""
    ie = DummyIE()
    # Prepare fake API response
    ptmd_response = {
        "basename": "testvideo",
        "attributes": {"duration": {"value": 123456}},
        "priorityList": [
            {
                "formitaeten": [
                    {
                        "qualities": [
                            {
                                "audio": {"tracks": [
                                    {"uri": "http://example.com/audio_low.mp4", "language": "deu"},
                                    {"uri": "http://example.com/audio_high.mp4", "language": "eng"},
                                ]},
                                "quality": "low",
                            },
                            {
                                "audio": {"tracks": [
                                    {"uri": "http://example.com/audio_med.mp4", "language": "deu"},
                                ]},
                                "quality": "med",
                            },
                        ],
                        "type": "audio",
                        "mimeType": "audio/mp4",
                        "mimeCodec": "mp4a.40.2",
                    }
                ]
            }
        ],
        "captions": [
            {"uri": "http://example.com/sub_de.vtt", "language": "deu"},
        ]
    }
    ie._download_json_return = ptmd_response
    result = ie._extract_ptmd("http://example.com/api/ptmd", "vid123", None, None)
    # Check extractor key and id
    assert result["extractor_key"] == "ZDFIE"
    assert result["id"] == "testvideo"
    # Duration should be converted from ms to seconds
    assert result["duration"] == pytest.approx(123.456, rel=1e-6)
    # Subtitles extraction
    assert result["subtitles"] == {"deu": [{"url": "http://example.com/sub_de.vtt"}]}
    # Formats should be sorted by quality (high, med, low)
    qualities_order = [qualities(ie._QUALITIES)(q) for q in ["high", "med", "low"]]
    sorted_qualities = [f["quality"] for f in result["formats"]]
    assert sorted_qualities == sorted_qualities[::-1]  # descending
    # Ensure all expected URLs present
    urls = {f["url"] for f in result["formats"]}
    assert urls == {
        "http://example.com/audio_low.mp4",
        "http://example.com/audio_med.mp4",
        "http://example.com/audio_high.mp4",
    }
