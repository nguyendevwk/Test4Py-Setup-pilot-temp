import re
import pytest
from youtube_dl.extractor.trutv import TruTVIE
from youtube_dl.utils import int_or_none, parse_iso8601

class DummyTruTVIE(TruTVIE):
    """Subclass that overrides network calls with deterministic data."""
    def __init__(self, json_response):
        super().__init__(downloader=None)
        self._json_response = json_response

    def _download_json(self, url, display_id, note=None, errnote=None, data=None, headers=None, query_string=None, timeout=None, add_dto=None, **kw):
        # Return the pre‑provided JSON regardless of URL
        return self._json_response


def test_episode_url_parsing(tmp_path):
    # Simulated JSON for an episode
    json_resp = {
        "episode": {
            "mediaId": "123abc",
            "title": "  Episode Title  ",
            "description": "Desc",
            "images": [
                {"srcUrl": "http://img1.jpg", "width": "640", "height": "360"},
                {"srcUrl": None, "width": "0", "height": "0"},
                {"srcUrl": "http://img2.jpg", "width": None, "height": None}
            ],
            "publicationDate": "2023-01-01T12:00:00Z",
            "showTitle": "Show",
            "seasonNum": "2",
            "episodeNum": "5"
        }
    }
    ie = DummyTruTVIE(json_resp)
    url = "https://www.trutv.com/shows/show-123/episode/42"
    info = ie.extract(url)

    assert info["id"] == "123abc"
    assert info["display_id"] == "42"
    assert info["title"] == "Episode Title"
    assert info["description"] == "Desc"
    assert info["series"] == "Show"
    assert info["season_number"] == 2
    assert info["episode_number"] == 5
    assert info["timestamp"] == parse_iso8601("2023-01-01T12:00:00Z")
    # Thumbnails should skip entries without srcUrl and convert sizes
    assert len(info["thumbnails"]) == 2
    assert info["thumbnails"][0]["url"] == "http://img1.jpg"
    assert info["thumbnails"][0]["width"] == 640
    assert info["thumbnails"][0]["height"] == 360
    assert info["thumbnails"][1]["url"] == "http://img2.jpg"
    assert info["thumbnails"][1]["width"] is None
    assert info["thumbnails"][1]["height"] is None


def test_clip_url_parsing(tmp_path):
    # Simulated JSON for a clip
    json_resp = {
        "info": {
            "mediaId": "clip123",
            "title": "Clip Title",
            "description": None,
            "images": [],
            "publicationDate": None,
            "showTitle": None,
            "seasonNum": None,
            "episodeNum": None
        }
    }
    ie = DummyTruTVIE(json_resp)
    url = "https://www.trutv.com/shows/show-123/videos/clip-slug"
    info = ie.extract(url)

    assert info["id"] == "clip123"
    assert info["display_id"] == "clip-slug"
    assert info["title"] == "Clip Title"
    assert info["description"] is None
    assert info["series"] is None
    assert info["season_number"] is None
    assert info["episode_number"] is None
    assert info["timestamp"] is None
    assert info["thumbnails"] == []


def test_invalid_url_raises():
    ie = DummyTruTVIE({})
    with pytest.raises(re.error):
        # URL does not match the pattern; re.match will return None
        ie.extract("https://www.trutv.com/invalid/url")
