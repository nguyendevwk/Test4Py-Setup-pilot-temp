import re
import pytest
from youtube_dl.extractor.udn import UDNEmbedIE
from youtube_dl.utils import determine_ext, int_or_none
from youtube_dl.compat import compat_urlparse

# Helper to create a minimal InfoExtractor instance with overridden methods
class DummyIE(UDNEmbedIE):
    def __init__(self, page_content, id_value='12345'):
        super().__init__()
        self._page_content = page_content
        self._id_value = id_value

    def _download_webpage(self, url, video_id, note=None):
        # Return the predefined page content regardless of URL
        return self._page_content

    def _match_id(self, url):
        return self._id_value


def test_parsing_options_success():
    # Page contains a valid options JSON with video URLs and title
    page = """
        <html>
        <script>
        var options = {"video":{"mp4":"//cdn.example.com/video_720p_500.mp4"},
                       "title":"Test Video",
                       "poster":"https://cdn.example.com/thumb.jpg"};
        </script>
        </html>
    """
    ie = DummyIE(page)
    result = ie._real_extract('http://video.udn.com/embed/news/12345')
    assert result['id'] == '12345'
    assert result['title'] == 'Test Video'
    assert result['thumbnail'] == 'https://cdn.example.com/thumb.jpg'
    # Only one format should be present
    assert len(result['formats']) == 1
    fmt = result['formats'][0]
    assert fmt['url'] == 'https://cdn.example.com/video_720p_500.mp4'
    assert fmt['format_id'] == 'http-mp4'
    assert fmt['height'] == 720
    assert fmt['tbr'] == 500
    assert fmt['ext'] == 'mp4'


def test_youtube_redirect():
    # Page contains a youtube redirect in options
    page = """
        <html>
        <script>
        var options = {"video":{"youtube":"https://www.youtube.com/watch?v=abc123"},
                       "title":"YouTube Video",
                       "poster":"https://cdn.example.com/thumb.jpg"};
        </script>
        </html>
    """
    ie = DummyIE(page)
    result = ie._real_extract('http://video.udn.com/embed/news/67890')
    # Should return a url_result dict
    assert result['url'] == 'https://www.youtube.com/watch?v=abc123'
    assert result['ie_key'] == 'Youtube'


def test_no_video_urls():
    # Page contains options without video key, fallback parsing used
    page = """
        <html>
        <script>
        var options = {"title":"Fallback Video",
                       "poster":"https://cdn.example.com/thumb.jpg"};
        </script>
        <script>
        var video = {"mp4":"//cdn.example.com/fallback_480p_300.mp4"};
        </script>
        </html>
    """
    ie = DummyIE(page)
    result = ie._real_extract('http://video.udn.com/embed/news/54321')
    assert result['id'] == '54321'
    assert result['title'] == 'Fallback Video'
    assert result['thumbnail'] == 'https://cdn.example.com/thumb.jpg'
    assert len(result['formats']) == 1
    fmt = result['formats'][0]
    assert fmt['url'] == 'https://cdn.example.com/fallback_480p_300.mp4'
    assert fmt['format_id'] == 'http-mp4'
    assert fmt['height'] == 480
    assert fmt['tbr'] == 300
    assert fmt['ext'] == 'mp4'
