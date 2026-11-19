import re
import json
import pytest
from youtube_dl.extractor.udn import UDNEmbedIE
from youtube_dl.utils import determine_ext, int_or_none, js_to_json
from youtube_dl.compat import compat_urlparse

class DummyUDNIE(UDNEmbedIE):
    """A minimal subclass that overrides network calls for testing."""
    def __init__(self, page_content, url_map=None):
        super().__init__()
        self._page_content = page_content
        self._url_map = url_map or {}

    def _download_webpage(self, url, video_id, note=None):
        # Return the pre‑defined page content or a mapped URL content.
        return self._url_map.get(url, self._page_content)

def test_extract_with_options_and_formats():
    # Page containing a valid `options` JSON with video URLs.
    page = """
        <html>
        <script>
        var options = {"video":{"mp4":"//cdn.example.com/video_720p_500.mp4","hls":"//cdn.example.com/playlist.m3u8"},
                       "title":"Test Video",
                       "poster":"https://cdn.example.com/thumb.jpg"};
        </script>
        </html>
    """
    extractor = DummyUDNIE(page)
    result = extractor._real_extract('http://video.udn.com/embed/news/12345')
    assert result['id'] == '12345'
    assert result['title'] == 'Test Video'
    assert result['thumbnail'] == 'https://cdn.example.com/thumb.jpg'
    # Two formats: one mp4 and one m3u8
    assert any(f['url'].endswith('.mp4') for f in result['formats'])
    assert any(f['url'].endswith('.m3u8') for f in result['formats'])
    # Check that format IDs are prefixed with 'http-'
    assert all(f['format_id'].startswith('http-') for f in result['formats'])
    # Verify that height and tbr are parsed correctly for the mp4 format
    mp4_format = next(f for f in result['formats'] if f['url'].endswith('.mp4'))
    assert mp4_format['height'] == 720
    assert mp4_format['tbr'] == 500

def test_extract_youtube_redirect():
    # Page where options contain a YouTube URL
    page = """
        <html>
        <script>
        var options = {"video":{"youtube":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
                       "title":"YouTube Redirect",
                       "poster":"https://cdn.example.com/thumb2.jpg"};
        </script>
        </html>
    """
    extractor = DummyUDNIE(page)
    result = extractor._real_extract('https://video.udn.com/embed/news/67890')
    # Should return a URL result pointing to YouTube
    assert result['id'] == '67890'
    assert result['title'] == 'YouTube Redirect'
    assert result['thumbnail'] == 'https://cdn.example.com/thumb2.jpg'
    # The result should be a dict with a 'url' key pointing to YouTube
    assert result['url'] == 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    assert result['ie_key'] == 'Youtube'

def test_extract_without_options_parsing_fallback():
    # Page missing the `options` variable; fallback regexes are used.
    page = """
        <html>
        <script>
        var options_str = {"video":{"mp4":"//cdn.example.com/video_480p_300.mp4"},
                           "title":"Fallback Video",
                           "poster":"https://cdn.example.com/thumb3.jpg"};
        </script>
        </html>
    """
    # Provide the page content that contains the fallback JSON string.
    extractor = DummyUDNIE(page)
    result = extractor._real_extract('http://video.udn.com/embed/news/54321')
    assert result['id'] == '54321'
    assert result['title'] == 'Fallback Video'
    assert result['thumbnail'] == 'https://cdn.example.com/thumb3.jpg'
    # Only one format should be present
    assert len(result['formats']) == 1
    fmt = result['formats'][0]
    assert fmt['url'].endswith('.mp4')
    assert fmt['height'] == 480
    assert fmt['tbr'] == 300
