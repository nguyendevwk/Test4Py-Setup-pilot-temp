import pytest
from youtube_dl.extractor.zdf import ZDFBaseIE
from youtube_dl.utils import determine_ext, parse_codecs, qualities

class DummyZDFIE(ZDFBaseIE):
    def __init__(self):
        # InfoExtractor requires a _real_extract method; we provide a dummy
        self._real_extract = lambda x: None

    # Override protected methods that would otherwise perform network I/O
    def _download_json(self, url, video_id, note, headers=None):
        # Return a predictable structure based on the URL
        return {"basename": "dummy_id", "priorityList": [], "attributes": {"duration": {"value": 123456}}, "captions": []}

    def _sort_formats(self, formats):
        # Simple sort by quality for deterministic output
        formats.sort(key=lambda f: f.get('quality', 0))

def test_extract_subtitles_basic():
    ie = DummyZDFIE()
    src = {
        "captions": [
            {"uri": "http://example.com/sub_de.vtt", "language": "deu"},
            {"uri": "http://example.com/sub_en.vtt", "language": "eng"},
            {"uri": None, "language": "deu"},
            {"uri": "http://example.com/sub_de2.vtt"}  # default language
        ]
    }
    subtitles = ie._extract_subtitles(src)
    assert "deu" in subtitles
    assert "eng" in subtitles
    assert len(subtitles["deu"]) == 2
    assert subtitles["deu"][0]["url"] == "http://example.com/sub_de.vtt"
    assert subtitles["eng"][0]["url"] == "http://example.com/sub_en.vtt"

def test_extract_format_m3u8_and_f4m():
    ie = DummyZDFIE()
    formats = []
    format_urls = set()
    # M3U8 case
    meta_m3u8 = {"url": "http://example.com/stream.m3u8", "mimeType": "application/x-mpegURL",
                 "type": "video", "quality": "high", "mimeCodec": "avc1.64001F"}
    ie._extract_format("vid123", formats, format_urls, meta_m3u8)
    # F4M case
    meta_f4m = {"url": "http://example.com/stream.f4m", "mimeType": "application/f4m+xml",
                "type": "video", "quality": "low", "mimeCodec": "avc1.42E01E"}
    ie._extract_format("vid123", formats, format_urls, meta_f4m)
    # Regular case
    meta_regular = {"url": "http://example.com/video.mp4", "mimeType": "video/mp4",
                    "type": "video", "quality": "med", "mimeCodec": "avc1.4D401E"}
    ie._extract_format("vid123", formats, format_urls, meta_regular)

    # Check that format_urls contains all three URLs
    assert len(format_urls) == 3
    # Check that formats list contains entries for each format
    assert any(f.get("url") == "http://example.com/stream.m3u8" for f in formats)
    assert any(f.get("url") == "http://example.com/stream.f4m" for f in formats)
    assert any(f.get("url") == "http://example.com/video.mp4" for f in formats)
    # Verify that the regular format has correct format_id and quality
    reg_fmt = next(f for f in formats if f["url"] == "http://example.com/video.mp4")
    assert reg_fmt["format_id"] == "http-video-med"
    assert reg_fmt["quality"] == qualities(ie._QUALITIES)("med")

def test_extract_ptmd_integration():
    ie = DummyZDFIE()
    # Prepare a fake ptmd URL and override _call_api to return a custom structure
    def fake_call_api(url, video_id, item, api_token=None, referrer=None):
        return {
            "basename": "test_video",
            "priorityList": [
                {
                    "formitaeten": [
                        {
                            "type": "audio",
                            "mimeType": "audio/mp4",
                            "qualities": [
                                {
                                    "quality": "low",
                                    "audio": {
                                        "tracks": [
                                            {"uri": "http://example.com/audio_low.mp3", "language": "deu"},
                                            {"uri": "http://example.com/audio_low2.mp3", "language": "eng"}
                                        ]
                                    }
                                },
                                {
                                    "quality": "high",
                                    "audio": {
                                        "tracks": [
                                            {"uri": "http://example.com/audio_high.mp3", "language": "deu"}
                                        ]
                                    }
                                }
                            ]
                        }
                    ]
                }
            ],
            "attributes": {"duration": {"value": 60000}},
            "captions": [
                {"uri": "http://example.com/sub_de.vtt", "language": "deu"}
            ]
        }
    ie._call_api = fake_call_api
    result = ie._extract_ptmd("http://example.com/ptmd", "vid123", None, None)
    assert result["id"] == "test_video"
    assert result["duration"] == 60.0  # 60000 ms -> 60 s
    assert result["extractor_key"] == ie.ie_key()
    # Check formats
    formats = result["formats"]
    assert len(formats) == 3
    qualities_list = [f["quality"] for f in formats]
    assert set(qualities_list) == {qualities(ie._QUALITIES)("low"), qualities(ie._QUALITIES)("high")}
    # Check subtitles
    subtitles = result["subtitles"]
    assert "deu" in subtitles
    assert subtitles["deu"][0]["url"] == "http://example.com/sub_de.vtt"
