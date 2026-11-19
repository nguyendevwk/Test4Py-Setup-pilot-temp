import re
import pytest
from youtube_dl.extractor.fourtube import FourTubeIE, FourTubeBaseIE

# Helper subclass that overrides network calls to return controlled HTML
class TestFourTubeIE(FourTubeIE):
    def __init__(self, html):
        super().__init__()
        self._html = html

    def _download_webpage(self, url, video_id, note=None, errnote=None, headers=None, data=None, timeout=None, *, fatal=True):
        # Return the pre‑supplied HTML regardless of URL
        return self._html

    def _download_json(self, url, video_id, data=None, headers=None, note=None, timeout=None, *, fatal=True):
        # Return a fake token JSON mapping format to URL
        return {"1080": "https://example.com/1080.mp4", "720": "https://example.com/720.mp4"}

# Sample HTML containing all required meta tags and a button with media id
BASE_HTML = """
<html>
<head>
<meta name="name" content="Sample Video Title">
<meta name="uploadDate" content="2021-01-01T12:00:00Z">
<meta name="thumbnailUrl" content="https://example.com/thumb.jpg">
<meta name="duration" content="PT5M30S">
<meta itemprop="interactionCount" content="UserPlays:1,234">
<meta itemprop="interactionCount" content="UserLikes:56">
</head>
<body>
<a class="item-to-subscribe" href="/channel/awesome-channel" title="Go to Awesome Channel page">Awesome Channel</a>
<ul class="list">
<li><a href="#">Tag1</a></li>
<li><a href="#">Tag2</a></li>
</ul>
<button data-id="12345" data-quality="1080"></button>
<button data-quality="720"></button>
</body>
</html>
"""

# Test normal extraction with all fields present
def test_four_tube_ie_normal_extraction():
    ie = TestFourTubeIE(BASE_HTML)
    result = ie._real_extract("http://www.4tube.com/videos/123456/sample-video")
    assert result["id"] == "123456"
    assert result["title"] == "Sample Video Title"
    assert result["thumbnail"] == "https://example.com/thumb.jpg"
    assert result["uploader"] == "Awesome Channel"
    assert result["uploader_id"] == "awesome-channel"
    assert result["view_count"] == 1234
    assert result["like_count"] == 56
    assert result["duration"] == 330  # 5 minutes 30 seconds
    assert result["age_limit"] == 18
    # Formats should contain two entries with correct URLs
    formats = result["formats"]
    assert len(formats) == 2
    urls = {f["format_id"]: f["url"] for f in formats}
    assert urls["1080p"] == "https://example.com/1080.mp4"
    assert urls["720p"] == "https://example.com/720.mp4"

# Test extraction when optional fields are missing (e.g., uploader, categories)
def test_four_tube_ie_missing_optional():
    html = BASE_HTML.replace('Awesome Channel', '').replace('Tag1', '').replace('Tag2', '')
    ie = TestFourTubeIE(html)
    result = ie._real_extract("http://www.4tube.com/videos/654321/another-video")
    assert result["uploader"] is None
    assert result["uploader_id"] is None
    assert result["categories"] is None

# Test that missing required meta 'name' raises an error
def test_four_tube_ie_missing_required():
    html = BASE_HTML.replace('<meta name="name"', '<meta name="title"')
    ie = TestFourTubeIE(html)
    with pytest.raises(Exception) as excinfo:
        ie._real_extract("http://www.4tube.com/videos/111111/missing-title")
    assert "name" in str(excinfo.value)
