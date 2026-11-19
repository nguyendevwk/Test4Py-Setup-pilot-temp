import json
import re
import pytest
from youtube_dl.extractor.itv import ITVIE
from youtube_dl.utils import determine_ext, parse_duration, clean_html

# Helper subclass that injects controlled responses
class DummyITVIE(ITVIE):
    def __init__(self, webpage, playlist_json):
        super().__init__(downloader=None)
        self._webpage = webpage
        self._playlist_json = playlist_json

    def _download_webpage(self, url, video_id):
        return self._webpage

    def _download_json(self, url, video_id, data=None, headers=None):
        return self._playlist_json

# Sample webpage and playlist data for normal extraction
sample_webpage = """
<html>
<head><meta property="og:title" content="Liar - Series 2 - Episode 6"/></head>
<body>
<div class="episode-info__synopsis">This is a <b>description</b>.</div>
<div id="video" data-video-playlist="https://api.itv.com/playlist"
     data-video-id="vid123" data-video-hmac="abcd1234"></div>
<script type="application/ld+json">
{
  "@context":"http://schema.org",
  "@type":"TVEpisode",
  "name":"Liar - Series 2 - Episode 6",
  "description":"md5:d0f91536569dec79ea184f0a44cca089",
  "episodeNumber":6,
  "seasonNumber":2,
  "series":"Liar"
}
</script>
</body>
</html>
"""

sample_playlist = {
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

def test_itvie_normal_extraction():
    ie = DummyITVIE(sample_webpage, sample_playlist)
    result = ie._real_extract("https://www.itv.com/hub/liar/2a4547a0012")
    assert result["id"] == "2a4547a0012"
    assert result["title"] == "Liar - Series 2 - Episode 6"
    assert result["description"] == "This is a description."
    assert result["duration"] == parse_duration("PT1H30M")
    # formats should include both mp4 and m3u8
    formats = result["formats"]
    assert any(f["url"] == "https://cdn.itv.com/video1.mp4" for f in formats)
    assert any(f["url"].startswith("https://cdn.itv.com/video2.m3u8") for f in formats)
    # subtitles
    subs = result["subtitles"]
    assert "en" in subs
    assert subs["en"][0]["url"] == "https://cdn.itv.com/subs_en.vtt"

def test_itvie_no_media_files():
    # Playlist with no MediaFiles
    playlist_no_media = {
        "Playlist": {
            "Video": {
                "Base": "https://cdn.itv.com/",
                "MediaFiles": [],
                "Subtitles": [],
                "Duration": "PT0M"
            }
        }
    }
    ie = DummyITVIE(sample_webpage, playlist_no_media)
    result = ie._real_extract("https://www.itv.com/hub/liar/2a4547a0012")
    assert result["formats"] == []  # no formats
    assert result["subtitles"] == {}  # no subtitles
    assert result["duration"] == 0

def test_itvie_invalid_json_raises():
    # Simulate invalid JSON by returning a string instead of dict
    class BadJSONDummyITVIE(DummyITVIE):
        def _download_json(self, url, video_id, data=None, headers=None):
            return "not a dict"
    ie = BadJSONDummyITVIE(sample_webpage, "not a dict")
    with pytest.raises(TypeError):
        ie._real_extract("https://www.itv.com/hub/liar/2a4547a0012")
