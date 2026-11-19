import json
import re
import pytest
from youtube_dl.extractor.konserthusetplay import KonserthusetPlayIE


class DummyKonserthusetPlayIE(KoncerthusetPlayIE):
    """A KonserthusetPlayIE that returns predefined webpage and JSON data."""

    def __init__(self, webpage, rest_json):
        super().__init__()
        self._webpage = webpage
        self._rest_json = rest_json

    def _download_webpage(self, url, video_id, note=None, errnote=None, *, data=None, headers=None, timeout=None, fatal=True):
        return self._webpage

    def _download_json(self, url, video_id, note=None, headers=None, data=None, timeout=None, transform_source=None, errnote=None, *, fatal=True):
        if transform_source:
            return transform_source(json.dumps(self._rest_json))
        return self._rest_json


def test_full_extraction(tmp_path):
    """Test normal extraction with all fields present."""
    # Prepare fake webpage containing the 'e' parameter
    webpage = (
        '<html>'
        '<script src="https://csp.picsearch.com/rest?e=XYZ123&containerId=mediaplayer&i=object"></script>'
        '</html>'
    )
    # Prepare fake JSON response
    rest_json = {
        "media": {
            "title": "Test Title",
            "image": "https://example.com/thumb.jpg",
            "duration": 123456,
            "mediaInfo": {"description": "Test description"},
        },
        "playerconfig": {
            "title": "Config Title",
            "playlist": [
                {
                    "url": "https://example.com/stream.m3u8",
                    "fallbackUrl": "https://example.com/fallback.mp4",
                    "captionsAvailableLanguages": {"en": "https://example.com/captions_en.vtt"},
                    "bitrates": [
                        {"url": "https://example.com/720p.mp4", "bitrate": 2000, "width": 1280, "height": 720},
                        {"url": "https://example.com/480p.mp4", "bitrate": 1000, "width": 854, "height": 480},
                    ],
                }
            ],
            "rtmp": {"netConnectionUrl": "rtmp://example.com/"},
            "plugins": {"bwcheck": {"netConnectionUrl": "rtmp://example.com/"}},
        },
    }

    ie = DummyKonserthusetPlayIE(webpage, rest_json)
    result = ie._real_extract("http://konserthusetplay.se/?m=TESTID")

    assert result["id"] == "TESTID"
    assert result["title"] == "Config Title"
    assert result["description"] == "Test description"
    assert result["thumbnail"] == "https://example.com/thumb.jpg"
    assert result["duration"] == 123.456  # duration in seconds
    assert isinstance(result["formats"], list)
    # At least one format should be present
    assert any(f.get("url") == "https://example.com/stream.m3u8" for f in result["formats"])
    # Subtitles should contain the English entry
    assert "en" in result["subtitles"]
    assert result["subtitles"]["en"][0]["url"] == "https://example.com/captions_en.vtt"


def test_fallback_only(tmp_path):
    """Test scenario where no RTMP formats are available but a fallback URL exists."""
    webpage = (
        '<html>'
        '<script src="https://csp.picsearch.com/rest?e=ABCDEF&containerId=mediaplayer&i=object"></script>'
        '</html>'
    )
    rest_json = {
        "media": {"title": "Fallback Test"},
        "playerconfig": {
            "playlist": [
                {
                    "fallbackUrl": "https://example.com/fallback.mp4",
                    "captionsAvailableLanguages": {},
                }
            ],
            "rtmp": {},
            "plugins": {},
        },
    }

    ie = DummyKonserthusetPlayIE(webpage, rest_json)
    result = ie._real_extract("http://rspoplay.se/?m=FALLBACKID")

    assert result["id"] == "FALLBACKID"
    assert result["title"] == "Fallback Test"
    assert len(result["formats"]) == 1
    assert result["formats"][0]["url"] == "https://example.com/fallback.mp4"
    assert result["subtitles"] == {}


def test_no_formats_or_fallback(tmp_path):
    """Test scenario where neither RTMP nor fallback URLs are provided."""
    webpage = (
        '<html>'
        '<script src="https://csp.picsearch.com/rest?e=NOPL&containerId=mediaplayer&i=object"></script>'
        '</html>'
    )
    rest_json = {
        "media": {"title": "No Formats"},
        "playerconfig": {
            "playlist": [
                {
                    "captionsAvailableLanguages": {},
                }
            ],
            "rtmp": {},
            "plugins": {},
        },
    }

    ie = DummyKonserthusetPlayIE(webpage, rest_json)
    result = ie._real_extract("http://konserthusetplay.se/?m=NOFORMATS")

    assert result["id"] == "NOFORMATS"
    assert result["title"] == "No Formats"
    assert result["formats"] == []
    assert result["subtitles"] == {}
