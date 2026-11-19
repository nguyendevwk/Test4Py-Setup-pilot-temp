import re
import pytest
from youtube_dl.extractor.fourtube import PornerBrosIE

# Test 1: Validate that the _VALID_URL regex matches expected URLs and captures groups correctly
def test_valid_url_parsing():
    pattern = re.compile(PornerBrosIE._VALID_URL)
    # URL with www subdomain
    url1 = "https://www.pornerbros.com/videos/skinny-brunette-takes-big-cock-down-her-anal-hole_181369"
    m1 = pattern.match(url1)
    assert m1 is not None, "URL should match the regex"
    assert m1.group('kind') == 'www', "Subdomain should be captured as 'www'"
    assert m1.group('display_id') == 'skinny-brunette-takes-big-cock-down-her-anal-hole', "Display ID should be captured"
    assert m1.group('id') == '181369', "Video ID should be captured"

    # URL with embed path
    url2 = "https://www.pornerbros.com/embed/181369"
    m2 = pattern.match(url2)
    assert m2 is not None, "Embed URL should match the regex"
    assert m2.group('kind') is None, "No subdomain should be captured"
    assert m2.group('display_id') is None, "No display_id should be captured for embed"
    assert m2.group('id') == '181369', "Video ID should be captured"

    # URL with mobile subdomain
    url3 = "https://m.pornerbros.com/videos/skinny-brunette-takes-big-cock-down-her-anal-hole_181369"
    m3 = pattern.match(url3)
    assert m3 is not None, "Mobile URL should match the regex"
    assert m3.group('kind') == 'm', "Subdomain should be captured as 'm'"

# Test 2: Ensure that the URL template correctly formats a video ID into a full URL
def test_url_template_formatting():
    video_id = "123456"
    expected_url = "https://www.pornerbros.com/videos/video_123456"
    formatted_url = PornerBrosIE._URL_TEMPLATE % video_id
    assert formatted_url == expected_url, "URL template should format the video ID correctly"

# Test 3: Verify that the token host constant is defined as expected
def test_token_host_constant():
    assert PornerBrosIE._TKN_HOST == "token.pornerbros.com", "Token host should be 'token.pornerbros.com'"
