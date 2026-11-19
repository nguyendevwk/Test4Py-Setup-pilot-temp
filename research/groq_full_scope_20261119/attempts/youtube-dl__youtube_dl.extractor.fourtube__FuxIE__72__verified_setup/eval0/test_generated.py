import re
import pytest
from youtube_dl.extractor.fourtube import FuxIE

def test_valid_url_parsing_video_and_embed():
    """The _VALID_URL regex should correctly capture id and display_id for both video and embed URLs."""
    video_url = "https://www.fux.com/video/195359/awesome-fucking-kitchen-ends-cum-swallow"
    embed_url = "https://www.fux.com/embed/195359"

    video_match = re.match(FuxIE._VALID_URL, video_url)
    embed_match = re.match(FuxIE._VALID_URL, embed_url)

    assert video_match is not None, "Video URL did not match _VALID_URL"
    assert embed_match is not None, "Embed URL did not match _VALID_URL"

    # Check captured groups for video URL
    assert video_match.group("id") == "195359"
    assert video_match.group("display_id") == "awesome-fucking-kitchen-ends-cum-swallow"

    # Check captured groups for embed URL
    assert embed_match.group("id") == "195359"
    assert embed_match.group("display_id") is None

def test_url_template_formatting():
    """The _URL_TEMPLATE should format correctly with a given video id."""
    video_id = "123456"
    expected_url = f"https://www.fux.com/video/{video_id}/video"
    formatted_url = FuxIE._URL_TEMPLATE % video_id
    assert formatted_url == expected_url, "URL template formatting failed"

def test_invalid_url_does_not_match():
    """URLs that do not conform to the expected pattern should not match _VALID_URL."""
    invalid_urls = [
        "https://www.fux.com/invalid/195359",
        "https://fux.com/video/abc",
        "http://www.fux.com/video/195359/extra/path",
        "https://www.fux.com/video/",
    ]
    for url in invalid_urls:
        assert re.match(FuxIE._VALID_URL, url) is None, f"Unexpected match for URL: {url}"
