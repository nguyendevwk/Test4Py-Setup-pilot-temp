import re
import json
import pytest
from youtube_dl.extractor.fourtube import FourTubeBaseIE
from youtube_dl.utils import parse_iso8601, parse_duration, str_to_int

class DummyFourTubeIE(FourTubeBaseIE):
    """A minimal subclass that overrides network calls to return controlled data."""
    _VALID_URL = r'https?://fourtube\.com/(?P<kind>m|v)/(?P<id>\d+)(?:/(?P<display_id>[^/]+))?'
    _URL_TEMPLATE = 'https://fourtube.com/v/%s'
    _TKN_HOST = 'example.com'

    def __init__(self, webpage, token_json):
        super().__init__()
        self._webpage = webpage
        self._token_json = token_json

    def _download_webpage(self, url, video_id, note=None):
        return self._webpage

    def _download_json(self, url, video_id, data=None, headers=None):
        return self._token_json

    def _search_regex(self, *args, **kwargs):
        return super()._search_regex(*args, **kwargs)

    def _html_search_meta(self, name, webpage, default=None):
        return super()._html_search_meta(name, webpage, default=default)

    def _html_search_regex(self, *args, **kwargs):
        return super()._html_search_regex(*args, **kwargs)

    def _search_regex(self, *args, **kwargs):
        return super()._search_regex(*args, **kwargs)

    def _parse_json(self, s, video_id):
        return json.loads(s)

@pytest.fixture
def sample_webpage():
    return """
    <html>
    <head>
        <meta name="name" content="Sample Video">
        <meta name="uploadDate" content="2021-01-01T12:00:00Z">
        <meta name="thumbnailUrl" content="https://example.com/thumb.jpg">
        <meta name="duration" content="PT2M30S">
        <meta itemprop="interactionCount" content="UserPlays:1,234">
        <meta itemprop="interactionCount" content="UserLikes:56">
    </head>
    <body>
        <a class="item-to-subscribe" href="/channel/abc123" title="Go to abc123 page">ABC</a>
        <a class="item-to-subscribe" href="/channel/abc123" title="Go to ABC page">ABC</a>
        <ul class="list">
            <li><a href="#">Tag1</a></li>
            <li><a href="#">Tag2</a></li>
        </ul>
        <button data-id="987" data-quality="720p"></button>
        <button data-quality="1080p"></button>
    </body>
    </html>
    """

@pytest.fixture
def token_json():
    return {
        "720p": "https://cdn.example.com/720p.mp4",
        "1080p": "https://cdn.example.com/1080p.mp4"
    }

def test_extract_formats_returns_correct_formats():
    ie = DummyFourTubeIE(webpage="", token_json=token_json())
    formats = ie._extract_formats(
        url="https://fourtube.com/v/123",
        video_id="123",
        media_id="987",
        sources=["720p", "1080p"]
    )
    expected = [
        {'url': 'https://cdn.example.com/720p.mp4', 'format_id': '720p', 'resolution': '720p', 'quality': 720},
        {'url': 'https://cdn.example.com/1080p.mp4', 'format_id': '1080p', 'resolution': '1080p', 'quality': 1080}
    ]
    assert formats == expected

def test_real_extract_parses_all_fields(sample_webpage, token_json):
    ie = DummyFourTubeIE(webpage=sample_webpage, token_json=token_json)
    result = ie.extract_info("https://fourtube.com/v/123", download=False)
    assert result['id'] == '123'
    assert result['title'] == 'Sample Video'
    assert result['thumbnail'] == 'https://example.com/thumb.jpg'
    assert result['uploader'] == 'ABC'
    assert result['uploader_id'] == 'abc123'
    assert result['categories'] == ['Tag1', 'Tag2']
    assert result['timestamp'] == parse_iso8601('2021-01-01T12:00:00Z')
    assert result['like_count'] == 56
    assert result['view_count'] == 1234
    assert result['duration'] == parse_duration('PT2M30S')
    assert result['age_limit'] == 18
    # formats should match token_json
    expected_formats = [
        {'url': 'https://cdn.example.com/720p.mp4', 'format_id': '720p', 'resolution': '720p', 'quality': 720},
        {'url': 'https://cdn.example.com/1080p.mp4', 'format_id': '1080p', 'resolution': '1080p', 'quality': 1080}
    ]
    assert result['formats'] == expected_formats

def test_real_extract_handles_missing_optional_fields(tmp_path, sample_webpage, token_json):
    # Remove optional meta tags to test defaults
    modified = re.sub(r'<meta name="duration" content="PT2M30S">', '', sample_webpage)
    modified = re.sub(r'<meta itemprop="interactionCount" content="UserLikes:56">', '', modified)
    ie = DummyFourTubeIE(webpage=modified, token_json=token_json)
    result = ie.extract_info("https://fourtube.com/v/123", download=False)
    assert result['duration'] is None
    assert result['like_count'] is None
    assert result['view_count'] == 1234
