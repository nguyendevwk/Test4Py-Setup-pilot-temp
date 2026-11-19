import re
import json
import pytest
from youtube_dl.extractor.fourtube import FourTubeBaseIE
from youtube_dl.utils import parse_iso8601, parse_duration, str_to_int

class DummyFourTubeIE(FourTubeBaseIE):
    """A minimal stub of FourTubeBaseIE that returns controlled data."""
    _VALID_URL = r'https?://fourtube\.com/(?P<kind>m|v)/(?P<id>\d+)(?:/(?P<display_id>[^/]+))?'
    _URL_TEMPLATE = 'https://fourtube.com/v/%s'
    _TKN_HOST = 'api.fourtube.com'

    def __init__(self, webpage, token_json):
        super().__init__()
        self._webpage = webpage
        self._token_json = token_json

    def _download_webpage(self, url, video_id, note=None):
        return self._webpage

    def _download_json(self, url, video_id, data=None, headers=None):
        return self._token_json

    def _parse_json(self, s, video_id):
        return json.loads(s)

    def _sort_formats(self, formats):
        # keep order for deterministic tests
        pass


def test_extract_formats_normal():
    """Test that _extract_formats returns correct format dicts."""
    webpage = """
    <meta name="name" content="Test Video">
    <meta property="uploadDate" content="2023-01-01T12:00:00Z">
    <meta property="thumbnailUrl" content="https://thumb.url/img.jpg">
    <meta property="duration" content="PT1M30S">
    <meta itemprop="interactionCount" content="UserPlays:1,234">
    <meta itemprop="interactionCount" content="UserLikes:56">
    <button data-id="12345" data-quality="720p"></button>
    <button data-quality="480p"></button>
    """
    token_json = {
        "720p": "https://cdn.fourtube.com/720p.mp4",
        "480p": "https://cdn.fourtube.com/480p.mp4"
    }
    ie = DummyFourTubeIE(webpage, token_json)
    formats = ie._extract_formats(
        url="https://fourtube.com/v/12345",
        video_id="12345",
        media_id="12345",
        sources=["720p", "480p"]
    )
    assert formats == [
        {
            'url': 'https://cdn.fourtube.com/720p.mp4',
            'format_id': '720p',
            'resolution': '720p',
            'quality': 720
        },
        {
            'url': 'https://cdn.fourtube.com/480p.mp4',
            'format_id': '480p',
            'resolution': '480p',
            'quality': 480
        }
    ]


def test_real_extract_with_player_js():
    """Test extraction when media_id and sources are obtained from player JS."""
    webpage = """
    <meta name="name" content="JS Video">
    <meta property="uploadDate" content="2022-12-31T23:59:59Z">
    <meta property="thumbnailUrl" content="https://thumb.url/js.jpg">
    <meta property="duration" content="PT2M">
    <meta itemprop="interactionCount" content="UserPlays:10,000">
    <meta itemprop="interactionCount" content="UserLikes:200">
    <script id="playerembed" src="player.js"></script>
    """
    player_js = """
    $.ajax(url, opts); } } )([12345, [], 720, 480]);
    """
    token_json = {
        "720p": "https://cdn.fourtube.com/720p_js.mp4",
        "480p": "https://cdn.fourtube.com/480p_js.mp4"
    }

    class StubIE(DummyFourTubeIE):
        def _download_webpage(self, url, video_id, note=None):
            if url.endswith('player.js'):
                return player_js
            return webpage

    ie = StubIE(webpage, token_json)
    result = ie._real_extract("https://fourtube.com/m/99999")
    assert result['id'] == "99999"
    assert result['title'] == "JS Video"
    assert result['timestamp'] == parse_iso8601("2022-12-31T23:59:59Z")
    assert result['thumbnail'] == "https://thumb.url/js.jpg"
    assert result['view_count'] == 10000
    assert result['like_count'] == 200
    assert result['duration'] == parse_duration("PT2M")
    assert result['age_limit'] == 18
    # formats should be sorted by quality descending
    assert result['formats'][0]['quality'] == 720
    assert result['formats'][1]['quality'] == 480


def test_missing_title_raises():
    """Test that missing title meta raises an error."""
    webpage = """
    <meta property="uploadDate" content="2023-01-01T12:00:00Z">
    """
    token_json = {}
    ie = DummyFourTubeIE(webpage, token_json)
    with pytest.raises(ValueError):
        ie._real_extract("https://fourtube.com/v/12345")
