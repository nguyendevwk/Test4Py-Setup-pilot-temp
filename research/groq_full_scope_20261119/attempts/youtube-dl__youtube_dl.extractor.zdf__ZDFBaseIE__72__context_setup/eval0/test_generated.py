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
            {"uri": None, "language": "deu"},
        ]
    }
    subtitles = ie._extract_subtitles(src)
    assert "deu" in subtitles
    assert "eng" in subtitles
    assert len(subtitles["deu"]) == 1
    assert subtitles["deu"][0]["url"] == "http://example.com/sub_de.vtt"
    assert subtitles["eng"][0]["url"] == "http://example.com/sub_en.vtt"

def test_extract_format_and_sort():
    ie = DummyZDFIE()
    formats = []
    track_uris = set()
    meta = {
        "url": "http://example.com/video.mp4",
        "type": "video",
        "mimeType": "video/mp4",
        "quality": "high",
        "language": "deu",
        "mimeCodec": "avc1.64001F",
    }
    ie._extract_format("vid123", formats, track_uris, meta)
    # Should have added one format
    assert len(formats) == 1
    f = formats[0]
    assert f["url"] == meta["url"]
    assert f["format_id"] == "http-video-high"
    assert f["format_note"] == "high"
    assert f["quality"] == qualities(ie._QUALITIES)("high")
    # Duplicate URL should not be added again
    ie._extract_format("vid123", formats, track_uris, meta)
    assert len(formats) == 1

def test_extract_ptmd_integration():
    ie = DummyZDFIE()
    ptmd_url = "http://example.com/api/ptmd"
    result = ie._extract_ptmd(ptmd_url, "vid123", api_token=None, referrer=None)
    # Check that the extractor key matches
    assert result["extractor_key"] == "ZDF"
    # ID should come from basename
    assert result["id"] == "test_video"
    # Duration should be converted from ms to seconds
    assert result["duration"] == 120.0
    # Formats should include both mp4 and f4m entries
    format_urls = {f["url"] for f in result["formats"]}
    assert "http://example.com/track1.mp4" in format_urls
    assert "http://example.com/track3.f4m" in format_urls
    # Subtitles should be extracted correctly
    subtitles = result["subtitles"]
    assert "deu" in subtitles
    assert "eng" in subtitles
    assert subtitles["deu"][0]["url"] == "http://example.com/sub_de.vtt"
    assert subtitles["eng"][0]["url"] == "http://example.com/sub_en.vtt"
