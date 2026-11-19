import pytest
from youtube_dl.extractor.glide import GlideIE


def test_normal_extraction(monkeypatch):
    """Test normal extraction with all fields present."""
    # Prepare a fake webpage containing title, video source and thumbnail
    fake_webpage = (
        '<html><head><title>Damon\'s Glide message</title></head>'
        '<body>'
        '<video><source src="https://cdn.example.com/video.mp4" type="video/mp4"></video>'
        '<img id="video-thumbnail" src="https://cdn.example.com/thumb.jpg">'
        '</body></html>'
    )

    # Monkeypatch the download and search helpers
    monkeypatch.setattr(GlideIE, "_download_webpage", lambda self, url, video_id: fake_webpage)
    monkeypatch.setattr(GlideIE, "_match_id", lambda self, url: "UZF8zlmuQbe4mr+7dCiQ0w==")
    monkeypatch.setattr(GlideIE, "_proto_relative_url", lambda self, url: url)

    ie = GlideIE()
    result = ie._real_extract("http://share.glide.me/UZF8zlmuQbe4mr+7dCiQ0w==")

    assert result["id"] == "UZF8zlmuQbe4mr+7dCiQ0w=="
    assert result["title"] == "Damon's Glide message"
    assert result["url"] == "https://cdn.example.com/video.mp4"
    assert result["thumbnail"] == "https://cdn.example.com/thumb.jpg"


def test_missing_title_fallback(monkeypatch):
    """Test that the title falls back to og title when <title> is missing."""
    fake_webpage = (
        '<html><head>'
        '<meta property="og:title" content="OG Title">'
        '</head>'
        '<body>'
        '<video><source src="https://cdn.example.com/video.mp4"></video>'
        '<img id="video-thumbnail" src="https://cdn.example.com/thumb.jpg">'
        '</body></html>'
    )

    monkeypatch.setattr(GlideIE, "_download_webpage", lambda self, url, video_id: fake_webpage)
    monkeypatch.setattr(GlideIE, "_match_id", lambda self, url: "id123")
    monkeypatch.setattr(GlideIE, "_proto_relative_url", lambda self, url: url)

    ie = GlideIE()
    result = ie._real_extract("http://share.glide.me/id123")

    assert result["title"] == "OG Title"


def test_missing_video_url_fallback(monkeypatch):
    """Test that the video URL falls back to og video URL when <source> is missing."""
    fake_webpage = (
        '<html><head>'
        '<meta property="og:video" content="https://cdn.example.com/og_video.mp4">'
        '</head>'
        '<body>'
        '<img id="video-thumbnail" src="https://cdn.example.com/thumb.jpg">'
        '</body></html>'
    )

    monkeypatch.setattr(GlideIE, "_download_webpage", lambda self, url, video_id: fake_webpage)
    monkeypatch.setattr(GlideIE, "_match_id", lambda self, url: "id456")
    monkeypatch.setattr(GlideIE, "_proto_relative_url", lambda self, url: url)

    ie = GlideIE()
    result = ie._real_extract("http://share.glide.me/id456")

    assert result["url"] == "https://cdn.example.com/og_video.mp4"
