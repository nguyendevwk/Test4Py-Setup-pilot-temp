import pytest
from youtube_dl.extractor.zdf import ZDFBaseIE
from youtube_dl.utils import determine_ext, parse_codecs, qualities
from youtube_dl.compat import compat_str

class DummyZDFIE(ZDFBaseIE):
    """A minimal subclass to expose protected methods for testing."""
    def __init__(self):
        super().__init__()
        self._download_json_called = False

    def _download_json(self, url, video_id, note, headers=None):
        self._download_json_called = True
        return {"dummy": "data"}

    def _call_api(self, url, video_id, item, api_token=None, referrer=None):
        # Return a controlled JSON structure for testing
        return {
            "basename": "test_video",
            "priorityList": [
                {
                    "formitaeten": [
                        {
                            "qualities": [
                                {
                                    "audio": {
                                        "tracks": [
                                            {"uri": "http://example.com/track1.mp4", "language": "deu"},
                                            {"uri": "http://example.com/track2.m3u8", "language": "eng"},
                                        ]
                                    },
                                    "quality": "high",
                                }
                            ],
                            "type": "video",
                            "mimeType": "video/mp4",
                        },
                        {
                            "qualities": [
                                {
                                    "audio": {
                                        "tracks": [
                                            {"uri": "http://example.com/track3.f4m", "language": "deu"},
                                        ]
                                    },
                                    "quality": "low",
                                }
                            ],
                            "type": "video",
                            "mimeType": "application/f4m+xml",
                        },
                    ]
                }
            ],
            "attributes": {
                "duration": {"value": 120000}  # milliseconds
            },
            "captions": [
                {"uri": "http://example.com/sub_de.vtt", "language": "deu"},
                {"uri": "http://example.com/sub_en.vtt", "language": "eng"},
            ],
        }

def test_extract_subtitles():
    ie = DummyZDFIE()
    src = {
        "captions": [
            {"uri": "http://example.com/sub_de.vtt", "language": "deu"},
            {"uri": "http://example.com/sub_en.vtt", "language": "eng"},
            {"uri": None, "language": "fra"},
        ]
    }
    subtitles = ie._extract_subtitles(src)
    assert "deu" in subtitles
    assert "eng" in subtitles
    assert len(subtitles["deu"]) == 1
    assert subtitles["deu"][0]["url"] == "http://example.com/sub_de.vtt"
    assert len(subtitles["eng"]) == 1
    assert subtitles["eng"][0]["url"] == "http://example.com/sub_en.vtt"

def test_extract_format_and_sorting(tmp_path):
    ie = DummyZDFIE()
    video_id = "vid123"
    formats = []
    format_urls = set()
    meta_mp4 = {
        "url": "http://example.com/video.mp4",
        "type": "video",
        "mimeType": "video/mp4",
        "quality": "high",
        "language": "deu",
        "mimeCodec": "avc1.64001F",
    }
    meta_m3u8 = {
        "url": "http://example.com/stream.m3u8",
        "type": "video",
        "mimeType": "application/x-mpegURL",
        "quality": "auto",
        "language": "eng",
        "mimeCodec": None,
    }
    meta_f4m = {
        "url": "http://example.com/stream.f4m",
        "type": "video",
        "mimeType": "application/f4m+xml",
        "quality": "low",
        "language": "deu",
        "mimeCodec": None,
    }

    # MP4
    ie._extract_format(video_id, formats, format_urls, meta_mp4)
    assert any(f["url"] == meta_mp4["url"] for f in formats)
    assert any(f["format_id"] == "http-video-high" for f in formats)

    # M3U8
    ie._extract_format(video_id, formats, format_urls, meta_m3u8)
    assert any(f["url"] == meta_m3u8["url"] for f in formats)
    assert any(f["format_id"].startswith("hls") for f in formats)

    # F4M
    ie._extract_format(video_id, formats, format_urls, meta_f4m)
    assert any(f["url"] == meta_f4m["url"] for f in formats)
    assert any(f["format_id"].startswith("hds") for f in formats)

    # Duplicate URL should not be added again
    prev_len = len(formats)
    ie._extract_format(video_id, formats, format_urls, meta_mp4)
    assert len(formats) == prev_len

def test_extract_ptmd_and_duration(tmp_path):
    ie = DummyZDFIE()
    ptmd_url = "http://example.com/api/ptmd"
    video_id = "vid123"
    api_token = "token"
    referrer = "http://example.com"

    result = ie._extract_ptmd(ptmd_url, video_id, api_token, referrer)

    # Check extractor key and id
    assert result["extractor_key"] == "ZDF"
    assert result["id"] == "test_video"

    # Duration should be converted from milliseconds to seconds
    assert result["duration"] == 120.0

    # Formats should contain entries for each track
    urls = {f["url"] for f in result["formats"]}
    assert "http://example.com/track1.mp4" in urls
    assert "http://example.com/track2.m3u8" in urls
    assert "http://example.com/track3.f4m" in urls

    # Subtitles extracted correctly
    subtitles = result["subtitles"]
    assert "deu" in subtitles
    assert "eng" in subtitles
    assert len(subtitles["deu"]) == 1
    assert subtitles["deu"][0]["url"] == "http://example.com/sub_de.vtt"
