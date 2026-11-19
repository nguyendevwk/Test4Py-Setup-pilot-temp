import json
import re
import pytest
from youtube_dl.extractor.itv import ITVIE
from youtube_dl.utils import determine_ext, parse_duration, clean_html, get_element_by_class

class FakeITVIE(ITVIE):
    def __init__(self, webpage, playlist_json):
        super().__init__(downloader=None)
        self._webpage = webpage
        self._playlist_json = playlist_json

    def _download_webpage(self, url, video_id, note=None, errnote=None, timeout=None, *, data=None, headers=None, query_string=None, errback=None, fatal=True):
        return self._webpage

    def _download_json(self, url, video_id, data=None, headers=None, note=None, timeout=None, errnote=None, errback=None, fatal=True):
        return self._playlist_json

def test_itvie_normal_extraction(tmp_path):
    # Sample webpage containing the required attributes and JSON-LD
    webpage = '''
    <html>
    <head><meta property="og:title" content="Liar - Series 2 - Episode 6"/></head>
    <body>
    <div id="video" data-video-playlist="https://example.com/playlist" data-video-id="vid123" data-video-hmac="abc123"></div>
    <div class="episode-info__synopsis">This is a <b>description</b>.</div>
    <script type="application/ld+json">
    {"@context":"http://schema.org","@type":"TVEpisode","name":"Liar - Series 2 - Episode 6"}
    </script>
    </body>
    </html>
    '''
    # Sample playlist JSON with media files and subtitles
    playlist_json = {
        "Playlist": {
            "Video": {
                "Base": "https://cdn.example.com/",
                "MediaFiles": [
                    {"Href": "/video1.mp4"},
                    {"Href": "/video2.m3u8"}
                ],
                "Subtitles": [
                    {"Href": "https://cdn.example.com/subs_en.vtt"}
                ],
                "Duration": "PT1H30M"
            }
        }
    }
    ie = FakeITVIE(webpage, playlist_json)
    result = ie._real_extract("https://www.itv.com/hub/liar/2a4547a0012")
    assert result["id"] == "2a4547a0012"
    assert result["title"] == "Liar - Series 2 - Episode 6"
    assert result["description"] == "This is a description."
    assert result["duration"] == 5400  # 1h30m in seconds
    # Formats should contain both mp4 and m3u8 entries
    formats = result["formats"]
    assert any(f.get("url") == "https://cdn.example.com/video1.mp4" for f in formats)
    assert any(f.get("url") == "https://cdn.example.com/video2.m3u8" for f in formats)
    # Subtitles should contain the vtt file
    subtitles = result["subtitles"]
    assert "en" in subtitles
    assert any(sub["url"] == "https://cdn.example.com/subs_en.vtt" for sub in subtitles["en"])

def test_itvie_missing_media_and_subtitles(tmp_path):
    # Webpage with attributes but no media files or subtitles
    webpage = '''
    <html>
    <head><meta property="og:title" content="No Media Episode"/></head>
    <body>
    <div id="video" data-video-playlist="https://example.com/playlist" data-video-id="vid456" data-video-hmac="def456"></div>
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
    ie = FakeITVIE(webpage, playlist_json)
    result = ie._real_extract("https://www.itv.com/hub/no-media/vid456")
    assert result["id"] == "vid456"
    assert result["title"] == "No Media Episode"
    assert result["duration"] == 0
    # No formats or subtitles should be present
    assert result["formats"] == []
    assert result["subtitles"] == {}

def test_itvie_invalid_json_ld_fallback(tmp_path):
    # Webpage with no JSON-LD but with BreadcrumbList containing TVEpisode
    webpage = '''
    <html>
    <head><meta property="og:title" content="Fallback Episode"/></head>
    <body>
    <div id="video" data-video-playlist="https://example.com/playlist" data-video-id="vid789" data-video-hmac="ghi789"></div>
    <script type="application/ld+json">
    {"@context":"http://schema.org","@type":"BreadcrumbList","itemListElement":[{"item":{"@type":"TVEpisode","name":"Fallback Episode"}}]}
    </script>
    </body>
    </html>
    '''
    playlist_json = {
        "Playlist": {
            "Video": {
                "Base": None,
                "MediaFiles": [{"Href": "/fallback.mp4"}],
                "Subtitles": [],
                "Duration": "PT5M"
            }
        }
    }
    ie = FakeITVIE(webpage, playlist_json)
    result = ie._real_extract("https://www.itv.com/hub/fallback/vid789")
    assert result["id"] == "vid789"
    assert result["title"] == "Fallback Episode"
    assert result["duration"] == 300
    formats = result["formats"]
    assert any(f.get("url") == "https://example.com/fallback.mp4" for f in formats)
