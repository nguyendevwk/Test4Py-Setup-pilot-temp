import re
import pytest
from youtube_dl.extractor.fourtube import PornerBrosIE
from youtube_dl.utils import ExtractorError

# Helper to create a fake webpage containing the minimal required meta tags
def fake_webpage(title, upload_date, thumbnail, media_id, qualities):
    meta_template = (
        f'<meta name="name" content="{title}">'
        f'<meta name="uploadDate" content="{upload_date}">'
        f'<meta name="thumbnailUrl" content="{thumbnail}">'
        f'<meta name="duration" content="PT20M">'
        f'<meta itemprop="interactionCount" content="UserPlays:1,234">'
        f'<meta itemprop="interactionCount" content="UserLikes:56">'
        f'<button data-id="{media_id}" data-quality="720p"></button>'
    )
    # Add additional quality buttons
    for q in qualities:
        meta_template += f'<button data-quality="{q}"></button>'
    return meta_template

@pytest.fixture
def ie(monkeypatch):
    """Return a PornerBrosIE instance with mocked download methods."""
    instance = PornerBrosIE()
    # Mock _download_webpage to return a fake page
    monkeypatch.setattr(
        instance,
        "_download_webpage",
        lambda url, video_id, *args, **kwargs: fake_webpage(
            title="Test Video",
            upload_date="20200101",
            thumbnail="https://example.com/thumb.jpg",
            media_id="12345",
            qualities=["480p", "1080p"],
        ),
    )
    # Mock _download_json to return dummy tokens
    monkeypatch.setattr(
        instance,
        "_download_json",
        lambda url, video_id, *args, **kwargs: {
            "720p": "https://example.com/720p.mp4",
            "480p": "https://example.com/480p.mp4",
            "1080p": "https://example.com/1080p.mp4",
        },
    )
    return instance

def test_extract_valid_url_and_fields(ie):
    """Test that a valid URL is parsed and returns expected fields."""
    url = "https://www.pornerbros.com/videos/test-video_123456"
    result = ie.extract(url)
    assert result["id"] == "123456"
    assert result["title"] == "Test Video"
    assert result["thumbnail"] == "https://example.com/thumb.jpg"
    assert result["uploader"] is None
    assert result["uploader_id"] is None
    assert result["timestamp"] == 1577836800  # 2020-01-01T00:00:00Z
    assert result["duration"] == 1200  # 20 minutes
    assert result["view_count"] == 1234
    assert result["like_count"] == 56
    # Formats should include all mocked qualities
    format_ids = {f["format_id"] for f in result["formats"]}
    assert format_ids == {"720p", "480p", "1080p"}

def test_mobile_url_uses_template(ie, monkeypatch):
    """Test that a mobile URL triggers the URL template substitution."""
    # Capture the URL passed to _download_webpage
    captured = {}
    def capture(url, video_id, *args, **kwargs):
        captured["url"] = url
        return fake_webpage(
            title="Mobile Test",
            upload_date="20200202",
            thumbnail="https://example.com/mobile.jpg",
            media_id="54321",
            qualities=["360p"],
        )
    monkeypatch.setattr(ie, "_download_webpage", capture)
    url = "https://m.pornerbros.com/videos/mobile-video_54321"
    ie.extract(url)
    # The URL should be replaced by the template
    assert captured["url"] == "https://www.pornerbros.com/videos/video_54321"

def test_invalid_url_raises_error(ie):
    """Test that an invalid URL raises ExtractorError."""
    with pytest.raises(ExtractorError):
        ie.extract("https://www.invalid.com/videos/invalid_000")
