import re
import json
import pytest
from youtube_dl.extractor.udn import UDNEmbedIE
from youtube_dl.utils import determine_ext, int_or_none, js_to_json
from youtube_dl.compat import compat_urlparse

class DummyUDNIE(UDNEmbedIE):
    """UDNEmbedIE with overridden network methods for testing."""
    def __init__(self, webpage):
        super().__init__()
        self._webpage = webpage

    def _download_webpage(self, url, video_id, note=None, errnote=None, **kw):
        # Return the pre‑defined webpage regardless of URL
        return self._webpage

    def _extract_m3u8_formats(self, url, video_id, ext='mp4', m3u8_id='hls'):
        # Simplified stub: return a single format dict
        return [{'url': url, 'format_id': m3u8_id, 'ext': ext}]

    def _extract_f4m_formats(self, url, video_id, f4m_id='hds'):
        # Simplified stub: return a single format dict
        return [{'url': url, 'format_id': f4m_id, 'ext': 'f4m'}]


def test_extract_with_options_and_formats():
    """Test normal extraction when options JSON is present."""
    # Construct a page containing a JS options object with video URLs
    page = """
    <html><head><script>
    var options = {"video":{"mp4":"//cdn.example.com/video_720p.mp4","hls":"//cdn.example.com/stream.m3u8"},
                   "title":"Test Video",
                   "poster":"https://cdn.example.com/thumb.jpg"};
    </script></head></html>
    """
    extractor = DummyUDNIE(page)
    result = extractor._real_extract('http://video.udn.com/embed/news/12345')

    assert result['id'] == '12345'
    assert result['title'] == 'Test Video'
    assert result['thumbnail'] == 'https://cdn.example.com/thumb.jpg'
    # Two formats: mp4 and m3u8
    assert len(result['formats']) == 2
    formats = {f['format_id']: f for f in result['formats']}
    assert formats['http-mp4']['url'] == 'https://cdn.example.com/video_720p.mp4'
    assert formats['hls']['url'] == 'https://cdn.example.com/stream.m3u8'
    assert formats['hls']['ext'] == 'mp4'  # stub returns ext 'mp4'


def test_extract_youtube_redirect():
    """Test extraction when a YouTube URL is provided in options."""
    page = """
    <html><head><script>
    var options = {"video":{"youtube":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
                   "title":"YouTube Redirect",
                   "poster":"https://cdn.example.com/thumb2.jpg"};
    </script></head></html>
    """
    extractor = DummyUDNIE(page)
    result = extractor._real_extract('https://video.udn.com/embed/news/67890')

    # Should return a URL result pointing to YouTube
    assert result['id'] == '67890'
    assert result['title'] == 'YouTube Redirect'
    assert result['thumbnail'] == 'https://cdn.example.com/thumb2.jpg'
    # The result should be a dict with 'url' and 'ie_key'
    assert result['url'] == 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    assert result['ie_key'] == 'Youtube'


def test_extract_with_fallback_options():
    """Test extraction when options JSON is empty and fallback parsing is used."""
    # Page with empty options and separate video JSON
    page = """
    <html><head><script>
    var options = {};
    var video = {"mp4":"//cdn.example.com/video_480p.mp4"};
    var title = 'Fallback Video';
    var poster = 'https://cdn.example.com/thumb3.jpg';
    </script></head></html>
    """
    extractor = DummyUDNIE(page)
    result = extractor._real_extract('http://video.udn.com/play/news/54321')

    assert result['id'] == '54321'
    assert result['title'] == 'Fallback Video'
    assert result['thumbnail'] == 'https://cdn.example.com/thumb3.jpg'
    assert len(result['formats']) == 1
    fmt = result['formats'][0]
    assert fmt['url'] == 'https://cdn.example.com/video_480p.mp4'
    assert fmt['format_id'] == 'http-mp4'
    # Height and tbr should be None because regex does not match
    assert fmt.get('height') is None
    assert fmt.get('tbr') is None
