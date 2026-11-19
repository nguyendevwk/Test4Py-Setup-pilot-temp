import json
import re
import types
import pytest
from youtube_dl.extractor.zdf import ZDFBaseIE
from youtube_dl.utils import determine_ext, parse_codecs, qualities

class DummyZDFIE(ZDFBaseIE):
    """A minimal subclass that overrides network and format extraction methods
    to allow deterministic testing without external dependencies."""
    def __init__(self):
        super().__init__()
        self._download_json_calls = []

    def _download_json(self, url, video_id, note, headers=None):
        # Record the call and return a dummy JSON based on the URL
        self._download_json_calls.append((url, video_id, note, headers))
        # Return a simple JSON structure that mimics the expected API response
        return {"basename": "dummy_id", "attributes": {"duration": {"value": 123456}}, "captions": []}

    def _extract_m3u8_formats(self, url, video_id, ext, **kw):
        # Return a single dummy format for HLS
        return [{
            "url": url,
            "format_id": "hls",
            "format_note": "hls",
            "quality": qualities(self._QUALITIES)("auto"),
            "preference": -10,
        }]

    def _extract_f4m_formats(self, url, video_id, **kw):
        # Return a single dummy format for F4M
        return [{
            "url": url,
            "format_id": "f4m",
            "format_note": "f4m",
            "quality": qualities(self._QUALITIES)("auto"),
            "preference": -10,
        }]

    def _sort_formats(self, formats):
        # No-op for testing
        pass

    def _parse_json(self, json_str, video_id):
        return json.loads(json_str)

    def _search_regex(self, pattern, string, name, default=None, group=None):
        m = re.search(pattern, string)
        if not m:
            return default
        return m.group(group) if group else m.group(0)

def test_extract_subtitles_basic():
    """Test that subtitles are extracted correctly from a simple JSON structure."""
    ie = DummyZDFIE()
    src = {
        "captions": [
            {"uri": "http://example.com/sub_de.vtt", "language": "deu"},
            {"uri": "http://example.com/sub_en.vtt", "language": "eng"},
            {"uri": None, "language": "deu"},
            {"uri": "http://example.com/sub_de2.vtt"}  # default language
        ]
    }
    subs = ie._extract_subtitles(src)
    assert "deu" in subs
    assert "eng" in subs
    assert len(subs["deu"]) == 2
    assert len(subs["eng"]) == 1
    assert subs["deu"][0]["url"] == "http://example.com/sub_de.vtt"
    assert subs["deu"][1]["url"] == "http://example.com/sub_de2.vtt"

def test_extract_format_various_mime_and_ext():
    """Test that _extract_format handles different MIME types and extensions."""
    ie = DummyZDFIE()
    formats = []
    seen = set()

    # HLS via MIME type
    ie._extract_format("vid1", formats, seen, {
        "url": "http://example.com/stream.m3u8",
        "mimeType": "application/x-mpegURL",
        "quality": "high",
        "type": "video",
        "language": "deu",
    })
    assert any(f["format_id"] == "hls" for f in formats)
    assert len(formats) == 1

    # HLS via extension
    formats.clear()
    seen.clear()
    ie._extract_format("vid2", formats, seen, {
        "url": "http://example.com/stream2.m3u8",
        "mimeType": "video/mp4",
        "quality": "low",
        "type": "video",
        "language": "eng",
    })
    assert any(f["format_id"] == "hls" for f in formats)
    assert len(formats) == 1

    # F4M via MIME type
    formats.clear()
    seen.clear()
    ie._extract_format("vid3", formats, seen, {
        "url": "http://example.com/stream.f4m",
        "mimeType": "application/f4m+xml",
        "quality": "med",
        "type": "video",
        "language": "deu",
    })
    assert any(f["format_id"] == "f4m" for f in formats)
    assert len(formats) == 1

    # F4M via extension
    formats.clear()
    seen.clear()
    ie._extract_format("vid4", formats, seen, {
        "url": "http://example.com/stream2.f4m",
        "mimeType": "video/mp4",
        "quality": "med",
        "type": "video",
        "language": "eng",
    })
    assert any(f["format_id"] == "f4m" for f in formats)
    assert len(formats) == 1

    # Regular MP4
    formats.clear()
    seen.clear()
    ie._extract_format("vid5", formats, seen, {
        "url": "http://example.com/video.mp4",
        "mimeType": "video/mp4",
        "quality": "veryhigh",
        "type": "video",
        "language": "deu",
    })
    assert any(f["format_id"] == "http-video-veryhigh" for f in formats)
    assert len(formats) == 1
    assert formats[0]["quality"] == qualities(ie._QUALITIES)("veryhigh")

def test_extract_ptmd_integration():
    """Test that _extract_ptmd correctly processes a mocked API response."""
    ie = DummyZDFIE()
    # Prepare a fake ptmd URL and video ID
    ptmd_url = "http://api.zdf.de/ptmd/12345"
    video_id = "12345"
    api_token = "dummy_token"
    referrer = "http://example.com"

    # Call _extract_ptmd and verify returned structure
    result = ie._extract_ptmd(ptmd_url, video_id, api_token, referrer)

    # Verify that the dummy _download_json was called with correct headers
    called_url, called_id, note, headers = ie._download_json_calls[-1]
    assert called_url == ptmd_url
    assert called_id == video_id
    assert headers["Api-Auth"] == f"Bearer {api_token}"
    assert headers["Referer"] == referrer

    # Verify the result structure
    assert result["extractor_key"] == "ZDFIE"
    assert result["id"] == "dummy_id"
    assert result["duration"] == 123.456  # 123456 ms converted to seconds
    assert isinstance(result["formats"], list)
    assert isinstance(result["subtitles"], dict)
    # Since dummy API returns no captions, subtitles should be empty
    assert result["subtitles"] == {}
