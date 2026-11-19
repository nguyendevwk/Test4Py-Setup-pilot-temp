import re
import pytest
from youtube_dl.extractor.fourtube import PornerBrosIE

# Test that the regular expression matches the expected URL patterns
def test_valid_url_matching():
    pattern = re.compile(PornerBrosIE._VALID_URL)
    # Full URL with www subdomain
    url1 = "https://www.pornerbros.com/videos/skinny-brunette-takes-big-cock-down-her-anal-hole_181369"
    # Full URL with embed path
    url2 = "https://www.pornerbros.com/embed/181369"
    # Mobile subdomain
    url3 = "https://m.pornerbros.com/videos/skinny-brunette-takes-big-cock-down-her-anal-hole_181369"
    # Non-matching URL
    url4 = "https://www.pornerbros.com/other/12345"

    assert pattern.match(url1) is not None, "Pattern should match www video URL"
    assert pattern.match(url2) is not None, "Pattern should match embed URL"
    assert pattern.match(url3) is not None, "Pattern should match mobile video URL"
    assert pattern.match(url4) is None, "Pattern should not match unrelated URL"

# Test that the URL template correctly formats a video ID
def test_url_template():
    video_id = "181369"
    expected_url = "https://www.pornerbros.com/videos/video_181369"
    formatted_url = PornerBrosIE._URL_TEMPLATE % video_id
    assert formatted_url == expected_url, "URL template should format video ID correctly"

# Test that the token host constant is as expected
def test_tkn_host():
    expected_host = "token.pornerbros.com"
    assert PornerBrosIE._TKN_HOST == expected_host, "Token host should be token.pornerbros.com"
