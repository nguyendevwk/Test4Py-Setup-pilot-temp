import re
import pytest
from youtube_dl.extractor.fourtube import FuxIE


def test_valid_url_parsing():
    """Ensure the _VALID_URL regex correctly captures id and display_id."""
    pattern = re.compile(FuxIE._VALID_URL)
    url = "https://www.fux.com/video/195359/awesome-fucking-kitchen-ends-cum-swallow"
    match = pattern.match(url)
    assert match is not None, "URL should match the pattern"
    assert match.group("id") == "195359", "Video ID should be captured correctly"
    assert match.group("display_id") == "awesome-fucking-kitchen-ends-cum-swallow", \
        "Display ID should be captured correctly"

    # Test a URL without display_id
    url_no_disp = "https://m.fux.com/video/123456"
    match_no_disp = pattern.match(url_no_disp)
    assert match_no_disp is not None, "URL without display_id should match"
    assert match_no_disp.group("id") == "123456", "Video ID should be captured correctly"
    assert match_no_disp.group("display_id") is None, "Display ID should be None when absent"

    # Test an embed URL
    embed_url = "https://www.fux.com/embed/987654"
    embed_match = pattern.match(embed_url)
    assert embed_match is not None, "Embed URL should match"
    assert embed_match.group("id") == "987654", "Embed video ID should be captured correctly"
    assert embed_match.group("display_id") is None, "Display ID should be None for embed URLs"


def test_url_template_and_token_host():
    """Verify that the URL template and token host are as expected."""
    video_id = "12345"
    expected_url = f"https://www.fux.com/video/{video_id}/video"
    assert FuxIE._URL_TEMPLATE % video_id == expected_url, "URL template formatting failed"
    assert FuxIE._TKN_HOST == "token.fux.com", "Token host should be 'token.fux.com'"


def test_test_entries_structure():
    """Check that each test entry in _TESTS has the required keys and types."""
    for entry in FuxIE._TESTS:
        # Every test must have a 'url' key
        assert "url" in entry, "Test entry missing 'url' key"
        # If 'info_dict' is present, it should be a dict
        if "info_dict" in entry:
            assert isinstance(entry["info_dict"], dict), "'info_dict' must be a dict"
            # Required keys in info_dict
            required_keys = {"id", "ext", "title", "uploader", "uploader_id",
                             "upload_date", "timestamp", "duration",
                             "view_count", "like_count", "categories", "age_limit"}
            missing = required_keys - entry["info_dict"].keys()
            assert not missing, f"Missing keys in info_dict: {missing}"
        # 'only_matching' and 'params' are optional but if present should be bool/dict
        if "only_matching" in entry:
            assert isinstance(entry["only_matching"], bool), "'only_matching' must be bool"
        if "params" in entry:
            assert isinstance(entry["params"], dict), "'params' must be a dict"
