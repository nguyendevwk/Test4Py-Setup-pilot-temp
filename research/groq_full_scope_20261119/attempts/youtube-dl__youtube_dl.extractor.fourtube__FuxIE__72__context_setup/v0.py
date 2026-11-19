import re
import pytest
from youtube_dl.extractor.fourtube import FuxIE

# Helper to create a minimal webpage containing all required meta tags
def minimal_webpage():
    return """
    <html>
    <head>
        <meta name="name" content="Test Video Title">
        <meta property="uploadDate" content="2023-01-01T12:00:00Z">
        <meta property="thumbnailUrl" content="https://example.com/thumb.jpg">
        <meta property="duration" content="PT5M">
        <meta itemprop="interactionCount" content="UserPlays:1,234">
        <meta itemprop="interactionCount" content="UserLikes:56">
    </head>
    <body>
        <a class="item-to-subscribe" href="/channel/testuser" title="Go to Test User page">Test User</a>
        <ul class="list"><li><a>Category1</a></li><li><a>Category2</a></li></ul>
        <button data-id="12345" data-quality="720p"></button>
    </body>
    </html>
    """

def test_fuxie_normal_extraction(monkeypatch):
    """Test normal extraction with a URL containing display_id."""
    ie = FuxIE()
    # Patch download methods to return the minimal webpage and dummy token JSON
    monkeypatch.setattr(ie, "_download_webpage", lambda url, video_id, *_, **__: minimal_webpage())
    monkeypatch.setattr(ie, "_download_json", lambda url, video_id, *_, **__: {"720p": {"token": "https://example.com/video.mp4"}})
    result = ie._real_extract("https://www.fux.com/video/123456/test-video")
    assert result["id"] == "123456"
    assert result["title"] == "Test Video Title"
    assert result["uploader"] == "Test User"
    assert result["uploader_id"] == "testuser"
    assert result["thumbnail"] == "https://example.com/thumb.jpg"
    assert result["view_count"] == 1234
    assert result["like_count"] == 56
    assert result["duration"] == 300
    assert result["age_limit"] == 18
    assert isinstance(result["formats"], list)
    assert result["formats"][0]["url"] == "https://example.com/video.mp4"

def test_fuxie_missing_display_id(monkeypatch):
    """Test that a URL without display_id uses the URL template."""
    ie = FuxIE()
    monkeypatch.setattr(ie, "_download_webpage", lambda url, video_id, *_, **__: minimal_webpage())
    monkeypatch.setattr(ie, "_download_json", lambda url, video_id, *_, **__: {"720p": {"token": "https://example.com/video.mp4"}})
    result = ie._real_extract("https://www.fux.com/video/123456")
    # The URL template should be used, but extraction logic is the same
    assert result["id"] == "123456"
    assert result["title"] == "Test Video Title"

def test_fuxie_invalid_url_raises(monkeypatch):
    """Test that an invalid URL raises an AttributeError due to regex mismatch."""
    ie = FuxIE()
    with pytest.raises(AttributeError):
        ie._real_extract("https://invalid.com/not-a-fux-url")
