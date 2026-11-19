import re
import json
import pytest
from youtube_dl.extractor.udn import UDNEmbedIE
from youtube_dl.utils import determine_ext

class DummyUDNIE(UDNEmbedIE):
    """Subclass that overrides network calls for deterministic testing."""
    def __init__(self, page_content):
        super().__init__()
        self._page_content = page_content

    def _download_webpage(self, url, video_id, note=None):
        # Return the predefined page content regardless of URL
        return self._page_content

def test_extract_with_options_json(tmp_path):
    # Page containing a valid `options` JavaScript object
    page = """
    <html><body>
    <script>
    var options = {
        "video": {
            "mp4": "/api/video/300040/720p.mp4",
            "hls": "/api/video/300040/playlist.m3u8"
        },
        "title": "Sample Video",
        "poster": "https://example.com/thumbnail.jpg"
    };
    </script>
    </body></html>
    """
    extractor = DummyUDNIE(page)
    result = extractor.extract('http://video.udn.com/embed/news/300040')
    assert result['id'] == '300040'
    assert result['title'] == 'Sample Video'
    assert result['thumbnail'] == 'https://example.com/thumbnail.jpg'
    # Two formats expected: mp4 and hls
    assert len(result['formats']) == 2
    # Verify format IDs and URLs
    mp4_fmt = next(f for f in result['formats'] if f['format_id'] == 'http-mp4')
    hls_fmt = next(f for f in result['formats'] if f['format_id'] == 'http-hls')
    assert mp4_fmt['url'].endswith('/api/video/300040/720p.mp4')
    assert hls_fmt['url'].endswith('/api/video/300040/playlist.m3u8')
    # Check that HLS format has been expanded into multiple entries
    assert any(f['format_id'].startswith('hls') for f in result['formats'])

def test_extract_youtube_redirect(tmp_path):
    # Page where options contain a YouTube URL
    page = """
    <html><body>
    <script>
    var options = {
        "video": {
            "youtube": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        },
        "title": "YouTube Redirect",
        "poster": null
    };
    </script>
    </body></html>
    """
    extractor = DummyUDNIE(page)
    result = extractor.extract('https://video.udn.com/embed/news/123456')
    # Should return a URL result pointing to YouTube
    assert result['id'] == '123456'
    assert result['formats'] == []
    assert result['title'] == 'YouTube Redirect'
    assert result['thumbnail'] is None
    # The extractor should have returned a URL result, not a dict
    # In youtube-dl, url_result returns a dict with 'url' and 'ie_key'
    assert isinstance(result, dict)
    assert result.get('url') == 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    assert result.get('ie_key') == 'Youtube'

def test_extract_without_options_json(tmp_path):
    # Page lacking the `options` variable, forcing fallback parsing
    page = """
    <html><body>
    <script>
    var options_str = {
        "video": {
            "mp4": "/api/video/654321/480p.mp4"
        },
        "title": "Fallback Video",
        "poster": "https://example.com/fallback.jpg"
    };
    </script>
    </body></html>
    """
    extractor = DummyUDNIE(page)
    result = extractor.extract('http://video.udn.com/embed/news/654321')
    assert result['id'] == '654321'
    assert result['title'] == 'Fallback Video'
    assert result['thumbnail'] == 'https://example.com/fallback.jpg'
    assert len(result['formats']) == 1
    fmt = result['formats'][0]
    assert fmt['url'].endswith('/api/video/654321/480p.mp4')
    assert fmt['format_id'] == 'http-mp4'
    # Height and tbr should be None because regex didn't match
    assert fmt.get('height') is None
    assert fmt.get('tbr') is None
