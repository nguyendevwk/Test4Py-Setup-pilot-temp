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
        self._download_json_calls = []

    def _download_json(self, url, video_id, note, headers=None):
        self._download_json_calls.append((url, video_id, note, headers))
        # Return a simple JSON structure for testing
        return {"basename": "test_video", "attributes": {"duration": {"value": 123456}}, "captions": []}

    def _extract_m3u8_formats(self, url, video_id, ext, **kwargs):
        return [{"url": url, "format_id": "hls", "ext": ext}]

    def _extract_f4m_formats(self, url, video_id, **kwargs):
        return [{"url": url, "format_id": "hds"}]

    def _sort_formats(self, formats):
        formats.sort(key=lambda f: f.get("quality", 0))

    def _parse_json(self, json_str, video_id):
        return json.loads(json_str)

    def _search_regex(self, pattern, string, name, default=None, group=None):
        m = re.search(pattern, string)
        if not m:
            return default
        return m.group(group) if group else m.group(0)

def test_extract_subtitles_basic():
    """Test that subtitles are extracted correctly from a simple JSON."""
    ie = DummyZDFIE()
    src = {
        "captions": [
            {"uri": "http://example.com/sub_de.vtt", "language": "deu"},
            {"uri": "http://example.com/sub_en.vtt", "language": "eng"},
            {"uri": None, "language": "deu"},
        ]
    }
    subtitles = ie._extract_subtitles(src)
    assert "deu" in subtitles
    assert "eng" in subtitles
    assert len(subtitles["deu"]) == 1
    assert subtitles["deu"][0]["url"] == "http://example.com/sub_de.vtt"
    assert subtitles["eng"][0]["url"] == "http://example.com/sub_en.vtt"

def test_extract_format_m3u8_and_f4m():
    """Test that _extract_format handles m3u8 and f4m URLs correctly."""
    ie = DummyZDFIE()
    formats = []
    format_urls = set()
    # m3u8 case
    ie._extract_format(
        "vid123", formats, format_urls,
        {"url": "http://example.com/stream.m3u8", "mimeType": "application/x-mpegURL",
         "type": "video", "quality": "high", "language": "deu"})
    assert any(f["format_id"] == "hls" for f in formats)
    # f4m case
    ie._extract_format(
        "vid123", formats, format_urls,
        {"url": "http://example.com/stream.f4m", "mimeType": "application/f4m+xml",
         "type": "video", "quality": "low", "language": "deu"})
    assert any(f["format_id"] == "hds" for f in formats)
    # regular case
    ie._extract_format(
        "vid123", formats, format_urls,
        {"url": "http://example.com/video.mp4", "mimeType": "video/mp4",
         "type": "video", "quality": "med", "language": "deu"})
    assert any(f["format_id"] == "http-video-med" for f in formats)
    # duplicate URL should not add again
    prev_len = len(formats)
    ie._extract_format(
        "vid123", formats, format_urls,
        {"url": "http://example.com/video.mp4", "mimeType": "video/mp4",
         "type": "video", "quality": "med", "language": "deu"})
    assert len(formats) == prev_len

def test_extract_ptmd_and_player(tmp_path):
    """Test that _extract_ptmd returns expected structure and _extract_player parses JSON."""
    ie = DummyZDFIE()
    # Prepare a fake ptmd JSON with one format
    ptmd_json = {
        "basename": "video123",
        "attributes": {"duration": {"value": 60000}},
        "priorityList": [
            {
                "formitaeten": [
                    {
                        "qualities": [
                            {
                                "audio": {"tracks": [
                                    {"uri": "http://example.com/audio.mp4", "language": "deu"}
                                ]},
                                "quality": "high"
                            }
                        ],
                        "type": "video",
                        "mimeType": "video/mp4"
                    }
                ]
            }
        ],
        "captions": [
            {"uri": "http://example.com/sub_de.vtt", "language": "deu"}
        ]
    }
    # Mock _call_api to return our ptmd_json
    def mock_call_api(url, video_id, item, api_token=None, referrer=None):
        return ptmd_json
    ie._call_api = mock_call_api

    result = ie._extract_ptmd("http://example.com/ptmd", "video123", None, None)
    assert result["id"] == "video123"
    assert result["duration"] == 60.0  # 60000 ms -> 60 s
    assert result["extractor_key"] == "ZDFIE"
    assert len(result["formats"]) == 1
    fmt = result["formats"][0]
    assert fmt["url"] == "http://example.com/audio.mp4"
    assert fmt["format_id"] == "http-video-high"
    assert fmt["quality"] == qualities(ie._QUALITIES)("high")
    assert result["subtitles"]["deu"][0]["url"] == "http://example.com/sub_de.vtt"

    # Test _extract_player with a simple webpage containing JSON
    webpage = '<script>var data = data-zdfplayer-jsb=\'{"key":"value"}\';</script>'
    player_data = ie._extract_player(webpage, "video123")
    assert player_data == {"key": "value"}
