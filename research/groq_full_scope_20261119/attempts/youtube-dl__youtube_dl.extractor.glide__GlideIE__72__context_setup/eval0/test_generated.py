import pytest
from youtube_dl.extractor.glide import GlideIE

# Helper to create a GlideIE instance with a custom _download_webpage method
def make_extractor_with_webpage(html: str) -> GlideIE:
    extractor = GlideIE()
    # Monkey‑patch the _download_webpage method to return the provided HTML
    extractor._download_webpage = lambda url, video_id: html
    return extractor

def test_extract_full_fields(tmp_path):
    # HTML containing all required elements
    html = """
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
    extractor = make_extractor_with_webpage(html)
    result = extractor._real_extract('http://share.glide.me/UZF8zlmuQbe4mr+7dCiQ0w==')
    assert result['id'] == 'UZF8zlmuQbe4mr+7dCiQ0w=='
    assert result['title'] == "Damon's Glide message"
    assert result['url'] == 'https://cdn.example.com/video.mp4'
    assert result['thumbnail'] == 'https://cdn.example.com/thumb.jpg'

def test_extract_fallback_to_og(tmp_path):
    # HTML missing title, source, and img; rely on og tags
    html = """
    <html>
        <head>
            <meta property="og:title" content="OG Title">
            <meta property="og:video" content="https://cdn.example.com/og_video.mp4">
            <meta property="og:image" content="https://cdn.example.com/og_thumb.jpg">
        </head>
        <body></body>
    </html>
    """
    extractor = make_extractor_with_webpage(html)
    result = extractor._real_extract('http://share.glide.me/ABC123')
    assert result['id'] == 'ABC123'
    assert result['title'] == 'OG Title'
    assert result['url'] == 'https://cdn.example.com/og_video.mp4'
    assert result['thumbnail'] == 'https://cdn.example.com/og_thumb.jpg'

def test_invalid_url_raises():
    extractor = GlideIE()
    # The URL does not match the regex; _match_id should raise a ValueError
    with pytest.raises(ValueError):
        extractor._real_extract('http://invalid.url/not_a_glide_id')
