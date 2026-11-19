import json
import re
import pytest
from youtube_dl.extractor.zdf import ZDFBaseIE
from youtube_dl.utils import determine_ext, parse_codecs, qualities

class DummyIE(ZDFBaseIE):
    def __init__(self):
        super().__init__()
        self._download_json_calls = []

    def _download_json(self, url, video_id, note, headers=None):
        self._download_json_calls.append((url, video_id, note, headers))
        # Return a minimal fake response
        return {"basename": "fake_id", "priorityList": [], "attributes": {"duration": {"value": 123456}}, "captions": []}

    def _parse_json(self, json_str, video_id):
        return json.loads(json_str)

    def _search_regex(self, pattern, string, name, default=None, fatal=True, group=None):
        m = re.search(pattern, string)
        if m:
            return m.group(group or 1)
        if fatal:
            raise ValueError(f"Regex {name} not found")
        return default

    def _extract_m3u8_formats(self, url, video_id, ext, **kwargs):
        return [{"url": url, "format_id": "hls", "ext": ext}]

    def _extract_f4m_formats(self, url, video_id, **kwargs):
        return [{"url": url, "format_id": "hds"}]

    def _sort_formats(self, formats):
        formats.sort(key=lambda f: f.get("quality", 0))

@pytest.fixture
def ie():
    return DummyIE()

def test_extract_subtitles_basic(ie):
    src = {
        "captions": [
            {"uri": "http://example.com/sub1.srt", "language": "eng"},
            {"uri": "http://example.com/sub2.srt", "language": "deu"},
            {"uri": None, "language": "fra"},
            {"uri": "http://example.com/sub3.srt"},
        ]
    }
    subs = ie._extract_subtitles(src)
    assert "eng" in subs
    assert "deu" in subs
    assert "fra" not in subs
    assert len(subs["eng"]) == 1
    assert subs["eng"][0]["url"] == "http://example.com/sub1.srt"
    assert subs["deu"][0]["url"] == "http://example.com/sub2.srt"
    assert subs["deu"][1]["url"] == "http://example.com/sub3.srt"

def test_extract_format_m3u8_and_f4m(ie):
    formats = []
    urls = set()
    meta_m3u8 = {"url": "http://example.com/stream.m3u8", "mimeType": "application/x-mpegURL", "quality": "high"}
    meta_f4m = {"url": "http://example.com/stream.f4m", "mimeType": "application/f4m+xml", "quality": "low"}
    meta_other = {"url": "http://example.com/video.mp4", "mimeType": "video/mp4", "quality": "medium", "type": "video", "mimeCodec": "avc1.42E01E", "language": "deu"}
    ie._extract_format("vid", formats, urls, meta_m3u8)
    ie._extract_format("vid", formats, urls, meta_f4m)
    ie._extract_format("vid", formats, urls, meta_other)
    # m3u8 format
    assert any(f["format_id"] == "hls" for f in formats)
    # f4m format
    assert any(f["format_id"] == "hds" for f in formats)
    # other format
    assert any(f["format_id"] == "http-video-medium" for f in formats)
    # Ensure no duplicate URLs
    assert len(urls) == 3
    # Check that quality is mapped correctly
    qual_map = qualities(ie._QUALITIES)
    for f in formats:
        if f["format_id"] == "http-video-medium":
            assert f["quality"] == qual_map("medium")

def test_extract_ptmd_parses_duration_and_subtitles(ie):
    # Prepare a fake ptmd JSON with duration and captions
    ptmd_json = {
        "basename": "test123",
        "priorityList": [],
        "attributes": {"duration": {"value": 987654}},
        "captions": [
            {"uri": "http://example.com/sub.srt", "language": "eng"}
        ]
    }
    # Monkeypatch _call_api to return our fake JSON
    def fake_call_api(url, video_id, item, api_token=None, referrer=None):
        return ptmd_json
    ie._call_api = fake_call_api
    result = ie._extract_ptmd("http://api.example.com/ptmd", "vid", None, None)
    assert result["id"] == "test123"
    assert result["duration"] == pytest.approx(987.654)
    assert "eng" in result["subtitles"]
    assert result["subtitles"]["eng"][0]["url"] == "http://example.com/sub.srt"
    assert result["extractor_key"] == "ZDFIE"
