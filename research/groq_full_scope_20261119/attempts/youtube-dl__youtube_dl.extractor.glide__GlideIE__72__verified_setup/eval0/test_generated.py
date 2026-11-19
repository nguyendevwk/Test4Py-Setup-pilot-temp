import pytest
from youtube_dl.extractor.glide import GlideIE
from youtube_dl.utils import ExtractorError

# Sample webpage containing all required elements
WEBPAGE_FULL = """
<html>
<head><title>Damon's Glide message</title></head>
<body>
<source src="https://cdn.glide.me/video.mp4" type="video/mp4">
<img id="video-thumbnail" src="https://cdn.glide.me/thumb.jpg">
</body>
</html>
"""

# Sample webpage missing title and thumbnail, but with video source
WEBPAGE_NO_TITLE_THUMB = """
<html>
<body>
<source src="https://cdn.glide.me/video.mp4" type="video/mp4">
</body>
</html>
"""

# Sample webpage missing video source
WEBPAGE_NO_VIDEO = """
<html>
<head><title>No Video</title></head>
<body>
<img id="video-thumbnail" src="https://cdn.glide.me/thumb.jpg">
</body>
</html>
"""

def _mock_download_webpage(url, video_id):
    """Return a predefined webpage based on the video_id."""
    if video_id == "full":
        return WEBPAGE_FULL
    if video_id == "no_title_thumb":
        return WEBPAGE_NO_TITLE_THUMB
    if video_id == "no_video":
        return WEBPAGE_NO_VIDEO
    raise ExtractorError("Unknown video_id")

@pytest.fixture
def extractor():
    ie = GlideIE()
    # Monkey‑patch the download method to avoid network access
    ie._download_webpage = _mock_download_webpage
    return ie

def test_full_extraction(extractor):
    """Test normal extraction with all elements present."""
    result = extractor._real_extract("http://share.glide.me/full")
    assert result["id"] == "full"
    assert result["title"] == "Damon's Glide message"
    assert result["url"] == "https://cdn.glide.me/video.mp4"
    assert result["thumbnail"] == "https://cdn.glide.me/thumb.jpg"

def test_missing_title_and_thumbnail(extractor):
    """Test extraction when title and thumbnail are missing."""
    result = extractor._real_extract("http://share.glide.me/no_title_thumb")
    assert result["id"] == "no_title_thumb"
    # Title should fallback to None because no <title> or og:title
    assert result["title"] is None
    assert result["url"] == "https://cdn.glide.me/video.mp4"
    # Thumbnail should be None
    assert result["thumbnail"] is None

def test_missing_video_url_raises(extractor):
    """Test that extraction fails when no video URL is found."""
    with pytest.raises(ExtractorError):
        extractor._real_extract("http://share.glide.me/no_video")
