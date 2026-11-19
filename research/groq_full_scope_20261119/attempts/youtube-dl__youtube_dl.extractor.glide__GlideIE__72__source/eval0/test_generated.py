import pytest
from youtube_dl.extractor.glide import GlideIE

# Helper to create an extractor instance with a custom _download_webpage
def make_extractor(webpage_content):
    ie = GlideIE()
    ie._download_webpage = lambda url, video_id: webpage_content
    return ie

def test_normal_extraction():
    # Sample webpage containing all required elements
    webpage = """
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
    ie = make_extractor(webpage)
    result = ie._real_extract('http://share.glide.me/UZF8zlmuQbe4mr+7dCiQ0w==')
    assert result['id'] == 'UZF8zlmuQbe4mr+7dCiQ0w=='
    assert result['title'] == "Damon's Glide message"
    assert result['url'] == "https://cdn.example.com/video.mp4"
    assert result['thumbnail'] == "https://cdn.example.com/thumb.jpg"

def test_missing_title_fallback():
    # Webpage without <title> but with og:title
    webpage = """
        <html>
            <head>
                <meta property="og:title" content="Fallback Title">
            </head>
            <body>
                <video>
                    <source src="https://cdn.example.com/video.mp4" type="video/mp4">
                </video>
                <img id="video-thumbnail" src="https://cdn.example.com/thumb.jpg">
            </body>
        </html>
    """
    ie = make_extractor(webpage)
    result = ie._real_extract('http://share.glide.me/UZF8zlmuQbe4mr+7dCiQ0w==')
    assert result['title'] == "Fallback Title"

def test_missing_video_url_fallback():
    # Webpage without <source> but with og:video:url
    webpage = """
        <html>
            <head>
                <meta property="og:video:url" content="https://cdn.example.com/video.mp4">
            </head>
            <body>
                <img id="video-thumbnail" src="https://cdn.example.com/thumb.jpg">
            </body>
        </html>
    """
    ie = make_extractor(webpage)
    result = ie._real_extract('http://share.glide.me/UZF8zlmuQbe4mr+7dCiQ0w==')
    assert result['url'] == "https://cdn.example.com/video.mp4"
