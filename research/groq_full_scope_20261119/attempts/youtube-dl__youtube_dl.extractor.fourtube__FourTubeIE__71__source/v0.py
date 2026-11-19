import re
import pytest
from youtube_dl.extractor.fourtube import FourTubeIE

def test_valid_url_matching():
    """FourTubeIE should match known URL patterns and capture the video id."""
    pattern = re.compile(FourTubeIE._VALID_URL)
    # A typical 4tube URL
    url = "http://www.4tube.com/videos/123456/awesome-video"
    match = pattern.match(url)
    assert match is not None, f"URL {url} should match the pattern"
    assert match.group("id") == "123456", "Captured id should be '123456'"
    # An embed URL
    embed_url = "http://m.4tube.com/embed/987654"
    embed_match = pattern.match(embed_url)
    assert embed_match is not None, f"Embed URL {embed_url} should match the pattern"
    assert embed_match.group("id") == "987654", "Captured id should be '987654'"

def test_invalid_url_rejection():
    """FourTubeIE should not match URLs that do not conform to the pattern."""
    pattern = re.compile(FourTubeIE._VALID_URL)
    # A URL from a different domain
    bad_url = "http://example.com/videos/123456"
    assert pattern.match(bad_url) is None, "Non-4tube URL should not match"
    # A malformed 4tube URL
    malformed_url = "http://www.4tube.com/invalid/123456"
    assert pattern.match(malformed_url) is None, "Malformed 4tube URL should not match"

def test_url_template_and_test_entries():
    """The URL template should format correctly and test entries contain required keys."""
    # Test URL template formatting
    video_id = "555555"
    expected_url = f"https://www.4tube.com/videos/{video_id}/video"
    assert FourTubeIE._URL_TEMPLATE % video_id == expected_url

    # Validate that each test entry in _TESTS has the expected keys
    required_keys = {"url", "md5", "info_dict"}
    for test in FourTubeIE._TESTS:
        if "only_matching" in test:
            # Skip entries that only test matching
            continue
        assert required_keys.issubset(test.keys()), f"Test entry missing required keys: {test}"
        # Ensure the md5 is a 32-character hex string
        assert re.fullmatch(r"[a-f0-9]{32}", test["md5"]), f"Invalid md5 in test: {test['md5']}"
        # Ensure the info_dict contains the expected fields
        info = test["info_dict"]
        for field in ["id", "ext", "title", "uploader", "uploader_id", "upload_date",
                      "timestamp", "duration", "view_count", "like_count", "categories", "age_limit"]:
            assert field in info, f"Missing field '{field}' in info_dict of test: {test}"
