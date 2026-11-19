import re
import pytest
from youtube_dl.extractor.fourtube import FourTubeBaseIE


class DummyFourTubeIE(FourTubeBaseIE):
    # Simplified patterns for testing
    _VALID_URL = r'https?://example\.com/(?P<id>\w+)(?:/(?P<display_id>[\w-]+))?'
    _URL_TEMPLATE = 'https://example.com/%s'
    _TKN_HOST = 'token.example.com'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store calls for verification
        self._download_json_calls = []
        self._download_webpage_calls = []

    def _download_json(self, url, video_id, data=None, headers=None):
        self._download_json_calls.append((url, video_id, data, headers))
        # Return a predictable token dict
        return {'1080': 'https://cdn.example.com/1080p.mp4',
                '720': 'https://cdn.example.com/720p.mp4',
                '480': 'https://cdn.example.com/480p.mp4'}

    def _download_webpage(self, url, video_id, note=None, errnote=None, headers=None, data=None, timeout=10, err=None):
        self._download_webpage_calls.append((url, video_id, note, errnote, headers, data, timeout, err))
        # Return a minimal HTML containing required meta tags
        return f"""
        <html>
            <head>
                <meta name="name" content="Test Video">
                <meta property="uploadDate" content="2023-01-01T12:00:00Z">
                <meta property="thumbnailUrl" content="https://example.com/thumb.jpg">
                <meta property="duration" content="PT1M30S">
                <meta itemprop="interactionCount" content="UserPlays:1,234">
                <meta itemprop="interactionCount" content="UserLikes:56">
            </head>
            <body>
                <a class="item-to-subscribe" href="/channel/abc123" title="Go to abc123 page">abc123</a>
                <a class="item-to-subscribe" href="/channel/abc123" title="Go to Channel Name page">Channel Name</a>
                <ul class="list">
                    <li><a href="#">Tag1</a></li>
                    <li><a href="#">Tag2</a></li>
                </ul>
                <button data-id="999" data-quality="1080"></button>
                <button data-quality="720"></button>
                <button data-quality="480"></button>
            </body>
        </html>
        """


def test_extract_formats_returns_expected_list(tmp_path):
    """Test that _extract_formats returns a list of format dicts with correct fields."""
    ie = DummyFourTubeIE()
    url = 'https://example.com/abc'
    video_id = 'abc'
    media_id = '999'
    sources = ['1080', '720', '480']
    formats = ie._extract_formats(url, video_id, media_id, sources)

    # Verify that the returned list has the same length as sources
    assert len(formats) == len(sources)

    # Verify each format dict contains expected keys and values
    for fmt, quality in zip(formats, sources):
        assert fmt['format_id'] == f'{quality}p'
        assert fmt['resolution'] == f'{quality}p'
        assert fmt['quality'] == int(quality)
        assert fmt['url'] == f'https://cdn.example.com/{quality}p.mp4'


def test_real_extract_parses_expected_fields(tmp_path):
    """Test that _real_extract parses title, timestamp, thumbnail, uploader, etc."""
    ie = DummyFourTubeIE()
    # URL that matches _VALID_URL and includes display_id
    url = 'https://example.com/abc/abc-display'
    result = ie._real_extract(url)

    # Basic fields
    assert result['id'] == 'abc'
    assert result['title'] == 'Test Video'
    assert result['thumbnail'] == 'https://example.com/thumb.jpg'
    assert result['uploader'] == 'Channel Name'
    assert result['uploader_id'] == 'abc123'
    assert result['categories'] == ['Tag1', 'Tag2']
    assert result['view_count'] == 1234
    assert result['like_count'] == 56
    assert result['duration'] == 90  # 1 minute 30 seconds
    assert result['age_limit'] == 18

    # Formats should be present and non-empty
    assert isinstance(result['formats'], list)
    assert len(result['formats']) == 3
    # Check that the first format is 1080p
    assert result['formats'][0]['format_id'] == '1080p'


def test_real_extract_raises_on_invalid_url():
    """Test that _real_extract raises ExtractorError when URL does not match pattern."""
    ie = DummyFourTubeIE()
    invalid_url = 'https://invalid.com/notmatching'
    with pytest.raises(Exception) as excinfo:
        ie._real_extract(invalid_url)
    # The exception should indicate a URL mismatch
    assert 'does not match' in str(excinfo.value) or 'Invalid URL' in str(excinfo.value)
