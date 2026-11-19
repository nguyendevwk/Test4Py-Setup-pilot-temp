import json
import re
import pytest
from youtube_dl.extractor.itv import ITVIE
from youtube_dl.utils import determine_ext, parse_duration, clean_html, get_element_by_class

class DummyITVIE(ITVIE):
    def __init__(self, webpage, playlist_json):
        super().__init__(downloader=None)
        self._webpage = webpage
        self._playlist_json = playlist_json

    def _download_webpage(self, url, video_id, note=None, err=None, timeout=None, *, data=None, headers=None):
        return self._webpage

    def _download_json(self, url, video_id, data=None, headers=None, note=None, timeout=None, err=None):
        return self._playlist_json

def test_itvie_normal_extraction(tmp_path):
    # Prepare a minimal webpage with required attributes
    webpage = '''
    <html>
      <head><meta property="og:title" content="Test Episode"/></head>
      <body>
        <div id="video" data-video-playlist="https://example.com/playlist"
             data-video-id="vid123" data-video-hmac="abc123"></div>
        <div class="episode-info__synopsis">This is a <b>test</b> synopsis.</div>
    </body>
    </html>
    '''
    # Prepare a playlist JSON with one media file and one subtitle
    playlist_json = {
        "Playlist": {
            "Video": {
                "Base": "https://cdn.example.com/",
                "MediaFiles": [
                    {"Href": "/video1.mp4"},
                    {"Href": "/video2.m3u8"}
                ],
                "Subtitles": [
                    {"Href": "https://cdn.example.com/subs.vtt"}
                ],
                "Duration": "PT1H30M"
            }
        }
    }
    extractor = DummyITVIE(webpage, playlist_json)
    result = extractor._real_extract("https://www.itv.com/hub/test/vid123")

    # Basic info checks
    assert result["id"] == "vid123"
    assert result["title"] == "Test Episode"
    assert result["description"] == "This is a test synopsis."
    assert result["duration"] == 5400  # 1h30m in seconds

    # Formats
    formats = result["formats"]
    assert any(f.get("url") == "https://cdn.example.com/video1.mp4" for f in formats)
    # m3u8 format should be extracted via _extract_m3u8_formats
    assert any(f.get("format_id") == "hls" for f in formats)

    # Subtitles
    subtitles = result["subtitles"]
    assert "en" in subtitles
    assert subtitles["en"][0]["url"] == "https://cdn.example.com/subs.vtt"
    assert subtitles["en"][0]["ext"] == "vtt"

def test_itvie_no_media_files(tmp_path):
    # Webpage with required attributes but playlist has no MediaFiles
    webpage = '''
    <html>
      <head><meta property="og:title" content="No Media"/></head>
      <body>
        <div id="video" data-video-playlist="https://example.com/playlist"
             data-video-id="vid456" data-video-hmac="def456"></div>
    </body>
    </html>
    '''
    playlist_json = {
        "Playlist": {
            "Video": {
                "Base": None,
                "MediaFiles": [],
                "Subtitles": [],
                "Duration": "PT0M"
            }
        }
    }
    extractor = DummyITVIE(webpage, playlist_json)
    result = extractor._real_extract("https://www.itv.com/hub/test/vid456")

    # Formats list should be empty
    assert result["formats"] == []

    # Subtitles should be empty
    assert result["subtitles"] == {}

    # Duration zero
    assert result["duration"] == 0

def test_itvie_missing_playlist_attribute():
    # Webpage missing both data-video-playlist and data-video-id
    webpage = '''
    <html>
      <head><meta property="og:title" content="Missing"/></head>
      <body>
        <div id="video" data-video-hmac="xyz789"></div>
    </body>
    </html>
    '''
    playlist_json = {}
    extractor = DummyITVIE(webpage, playlist_json)
    with pytest.raises(KeyError):
        extractor._real_extract("https://www.itv.com/hub/test/vid789")
