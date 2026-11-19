import pytest
from youtube_dl.extractor.glide import GlideIE


@pytest.fixture
def extractor():
    """Return a fresh GlideIE instance."""
    return GlideIE()


def test_normal_extraction(extractor, monkeypatch):
    """Test normal extraction with all fields present."""
    sample_webpage = """
        <html>
            <head><title>Damon's Glide message</title></head>
            <body>
                <video>
                    <source src="https://cdn.example.com/video.mp4" type="video/mp4">
                </video>
                <img id="video-thumbnail" src="https://cdn.example.com/thumb.jpg">
            </body>
        </html>
    """
    # Patch the download method to return our sample webpage
    monkeypatch.setattr(extractor, "_download_webpage", lambda url, video_id: sample_webpage)

    result = extractor._real_extract("http://share.glide.me/UZF8zlmuQbe4mr+7dCiQ0w==")

    assert result["id"] == "UZF8zlmuQbe4mr+7dCiQ0w=="
    assert result["title"] == "Damon's Glide message"
    assert result["url"] == "https://cdn.example.com/video.mp4"
    assert result["thumbnail"] == "https://cdn.example.com/thumb.jpg"


def test_missing_title_fallback(extractor, monkeypatch):
    """If <title> is missing, fallback to og:title."""
    sample_webpage = """
        <html>
            <head></head>
            <body>
                <meta property="og:title" content="Fallback Title">
                <video>
                    <source src="https://cdn.example.com/video.mp4" type="video/mp4">
                </video>
                <img id="video-thumbnail" src="https://cdn.example.com/thumb.jpg">
            </body>
        </html>
    """
    monkeypatch.setattr(extractor, "_download_webpage", lambda url, video_id: sample_webpage)

    result = extractor._real_extract("http://share.glide.me/UZF8zlmuQbe4mr+7dCiQ0w==")

    assert result["title"] == "Fallback Title"


def test_missing_video_url_fallback(extractor, monkeypatch):
    """If <source> is missing, fallback to og:video:url."""
    sample_webpage = """
        <html>
            <head><title>Damon's Glide message</title></head>
            <body>
                <meta property="og:video:url" content="https://cdn.example.com/fallback.mp4">
                <img id="video-thumbnail" src="https://cdn.example.com/thumb.jpg">
            </body>
        </html>
    """
    monkeypatch.setattr(extractor, "_download_webpage", lambda url, video_id: sample_webpage)

    result = extractor._real_extract("http://share.glide.me/UZF8zlmuQbe4mr+7dCiQ0w==")

    assert result["url"] == "https://cdn.example.com/fallback.mp4"
