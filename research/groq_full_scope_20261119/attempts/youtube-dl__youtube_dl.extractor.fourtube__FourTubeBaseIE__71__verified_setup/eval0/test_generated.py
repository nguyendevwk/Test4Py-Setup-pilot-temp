import re
import pytest
from youtube_dl.extractor.fourtube import FourTubeBaseIE


class DummyFourTubeIE(FourTubeBaseIE):
    """Subclass that overrides network calls for deterministic testing."""

    def __init__(self, token_response):
        super().__init__()
        self._token_response = token_response

    def _download_json(self, url, video_id, data=None, headers=None):
        # Return the pre‑configured token mapping regardless of URL.
        return self._token_response


def test_extract_formats_normal():
    # Arrange: token mapping for three formats
    token_response = {
        '1080': 'https://example.com/1080p',
        '720': 'https://example.com/720p',
        '480': 'https://example.com/480p',
    }
    ie = DummyFourTubeIE(token_response)
    url = 'https://example.com/video'
    video_id = 'abc123'
    media_id = 'media456'
    sources = ['1080', '720', '480']

    # Act
    formats = ie._extract_formats(url, video_id, media_id, sources)

    # Assert: formats sorted by quality descending
    expected = [
        {'url': 'https://example.com/1080p', 'format_id': '1080p',
         'resolution': '1080p', 'quality': 1080},
        {'url': 'https://example.com/720p', 'format_id': '720p',
         'resolution': '720p', 'quality': 720},
        {'url': 'https://example.com/480p', 'format_id': '480p',
         'resolution': '480p', 'quality': 480},
    ]
    assert formats == expected


def test_extract_formats_single_source():
    # Arrange: single format
    token_response = {'360': 'https://example.com/360p'}
    ie = DummyFourTubeIE(token_response)
    url = 'https://example.com/video'
    video_id = 'id1'
    media_id = 'mid1'
    sources = ['360']

    # Act
    formats = ie._extract_formats(url, video_id, media_id, sources)

    # Assert: single format entry
    assert formats == [{
        'url': 'https://example.com/360p',
        'format_id': '360p',
        'resolution': '360p',
        'quality': 360,
    }]


def test_extract_formats_empty_sources():
    # Arrange: no sources provided
    token_response = {}
    ie = DummyFourTubeIE(token_response)
    url = 'https://example.com/video'
    video_id = 'id2'
    media_id = 'mid2'
    sources = []

    # Act
    formats = ie._extract_formats(url, video_id, media_id, sources)

    # Assert: empty list returned
    assert formats == []
