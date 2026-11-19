import json
import re
import pytest
from youtube_dl.extractor.itv import ITVIE
from youtube_dl.utils import determine_ext, parse_duration, clean_html, get_element_by_class

class DummyITVIE(ITVIE):
    """Subclass ITVIE to override network calls for deterministic testing."""
    def __init__(self, webpage, playlist_json):
        self._webpage = webpage
        self._playlist_json = playlist_json

    def _download_webpage(self, url, video_id, note=None, errnote=None, timeout=None, *, data=None, headers=None, query_string=None, fatal=True):
        return self._webpage

    def _download_json(self, url, video_id, note=None, timeout=None, data=None, headers=None, query_string=None, fatal=True):
        return self._playlist_json

def test_itvie_normal_extraction(tmp_path):
    # Sample webpage containing required attributes and JSON-LD
    webpage = """
    <html>
    <head>
        <meta property="og:title" content="Test Episode Title"/>
    </head>
    <body>
        <div id="video" data-video-playlist="https://api.itv.com/playlist" data-video-id="12345" data-video-hmac="abcd1234"></div>
        <div class="episode-info__synopsis">This is a <b>test</b> synopsis.</div>
        <script type="application/ld+json">
        {
            "@context": "http://schema.org",
            "@type": "TVEpisode",
            "name": "Test Episode Title",
            "description": "Test description",
            "episodeNumber": 1,
            "seasonNumber": 1,
            "series": "Test Series"
        }
        </script>
    </body>
    </html>
    """
    # Sample playlist JSON returned by _download_json
    playlist_json = {
        "Playlist": {
            "Video": {
                "Base": "https://cdn.itv.com/",
                "MediaFiles": [
                    {"Href": "/video1.mp4"},
                    {"Href": "/video2.m3u8"}
                ],
                "Subtitles": [
                    {"Href": "https://cdn.itv.com/subs_en.vtt"}
                ],
                "Duration": "PT1H30M"
            }
        }
    }
    extractor = DummyITVIE(webpage, playlist_json)
    result = extractor._real_extract("https://www.itv.com/hub/test/12345")
    # Basic info checks
    assert result["id"] == "12345"
    assert result["title"] == "Test Episode Title"
    assert result["description"] == "This is a test synopsis."
    # Formats
    formats = result["formats"]
    assert any(f.get("url") == "https://cdn.itv.com/video1.mp4" for f in formats)
    assert any(f.get("url") == "https://cdn.itv.com/video2.m3u8" for f in formats)
    # Subtitles
    subtitles = result["subtitles"]
    assert "en" in subtitles
    assert subtitles["en"][0]["url"] == "https://cdn.itv.com/subs_en.vtt"
    # Duration parsed correctly
    assert result["duration"] == 5400  # 1 hour 30 minutes

def test_itvie_no_media_files(tmp_path):
    # Webpage with attributes but no MediaFiles
    webpage = """
    <html>
    <body>
        <div id="video" data-video-playlist="https://api.itv.com/playlist" data-video-id="12345" data-video-hmac="abcd1234"></div>
    </body>
    </html>
    """
    playlist_json = {
        "Playlist": {
            "Video": {
                "Base": "https://cdn.itv.com/",
                "MediaFiles": [],
                "Subtitles": [],
                "Duration": "PT0M"
            }
        }
    }
    extractor = DummyITVIE(webpage, playlist_json)
    result = extractor._real_extract("https://www.itv.com/hub/test/12345")
    # Formats list should be empty
    assert result["formats"] == []
    # Subtitles should be empty
    assert result["subtitles"] == {}
    # Duration zero
    assert result["duration"] == 0

def test_itvie_invalid_href_and_subtitles(tmp_path):
    # Webpage with invalid hrefs and non-dict subtitles
    webpage = """
    <html>
    <body>
        <div id="video" data-video-playlist="https://api.itv.com/playlist" data-video-id="12345" data-video-hmac="abcd1234"></div>
    </body>
    </html>
    """
    playlist_json = {
        "Playlist": {
            "Video": {
                "Base": None,
                "MediaFiles": [
                    {"Href": None},
                    {"Href": "invalid://path"}
                ],
                "Subtitles": [
                    {"Href": None},
                    "not a dict",
                    {"Href": "https://cdn.itv.com/subs_en.vtt"}
                ],
                "Duration": "PT5M"
            }
        }
    }
    extractor = DummyITVIE(webpage, playlist_json)
    result = extractor._real_extract("https://www.itv.com/hub/test/12345")
    # Only the valid media file should be included
    formats = result["formats"]
    assert len(formats) == 1
    assert formats[0]["url"] == "invalid://path"
    # Only the valid subtitle should be included
    subtitles = result["subtitles"]
    assert "en" in subtitles
    assert subtitles["en"][0]["url"] == "https://cdn.itv.com/subs_en.vtt"
    # Duration parsed correctly
    assert result["duration"] == 300
