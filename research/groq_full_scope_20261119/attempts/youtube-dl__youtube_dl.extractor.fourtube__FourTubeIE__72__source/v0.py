import re
import pytest
from youtube_dl.extractor.fourtube import FourTubeIE

# Test 1: Validate the regular expression used for matching URLs
def test_fourtube_valid_url_parsing():
    pattern = re.compile(FourTubeIE._VALID_URL)
    # A typical 4tube video URL
    url = "https://www.4tube.com/videos/123456/awesome-video"
    match = pattern.match(url)
    assert match is not None, "URL should match the pattern"
    assert match.group('kind') == 'www', "Subdomain should be captured correctly"
    assert match.group('id') == '123456', "Video ID should be captured correctly"
    assert match.group('display_id') == 'awesome-video', "Display ID should be captured correctly"

    # A mobile subdomain URL
    mobile_url = "http://m.4tube.com/embed/987654"
    match = pattern.match(mobile_url)
    assert match is not None, "Mobile URL should match the pattern"
    assert match.group('kind') == 'm', "Subdomain should be captured correctly for mobile"
    assert match.group('id') == '987654', "Video ID should be captured correctly for mobile"
    assert match.group('display_id') is None, "Display ID should be None when not present"

# Test 2: Ensure the URL template is formatted correctly
def test_fourtube_url_template_formatting():
    video_id = "555555"
    expected = "https://www.4tube.com/videos/555555/video"
    formatted = FourTubeIE._URL_TEMPLATE % video_id
    assert formatted == expected, "URL template should format the video ID correctly"

# Test 3: Verify that the test cases defined in the extractor contain required keys
def test_fourtube_test_cases_structure():
    required_keys = {"url", "md5", "info_dict"}
    for test in FourTubeIE._TESTS:
        # Each test dict must contain at least the required keys
        assert required_keys.issubset(test.keys()), f"Test case missing required keys: {test}"
        # The 'info_dict' should contain specific keys
        info = test["info_dict"]
        for key in ("id", "ext", "title", "uploader", "uploader_id", "upload_date",
                    "timestamp", "duration", "view_count", "like_count", "categories", "age_limit"):
            assert key in info, f"info_dict missing key '{key}' in test case: {test}"
