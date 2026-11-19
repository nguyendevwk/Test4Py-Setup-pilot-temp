import re
import pytest
from youtube_dl.extractor.fourtube import FuxIE

def test_valid_url_parsing():
    """The _VALID_URL regex should correctly capture id and display_id."""
    pattern = re.compile(FuxIE._VALID_URL)
    url = "https://www.fux.com/video/195359/awesome-fucking-kitchen-ends-cum-swallow"
    match = pattern.match(url)
    assert match is not None, "URL should match the regex"
    assert match.group("id") == "195359", "Captured id should be '195359'"
    assert match.group("display_id") == "awesome-fucking-kitchen-ends-cum-swallow", \
        "Captured display_id should match the slug"

def test_url_template_formatting():
    """The _URL_TEMPLATE should format correctly with a given id."""
    video_id = "123456"
    expected = f"https://www.fux.com/video/{video_id}/video"
    formatted = FuxIE._URL_TEMPLATE % video_id
    assert formatted == expected, "URL template formatting failed"

def test_test_cases_structure():
    """Each test case in _TESTS should contain required keys."""
    required_keys = {"url", "info_dict", "params"}
    for test in FuxIE._TESTS:
        # Only tests that are not only_matching should have info_dict and params
        if not test.get("only_matching"):
            assert "info_dict" in test, "Missing 'info_dict' in test case"
            assert "params" in test, "Missing 'params' in test case"
            # Ensure info_dict contains mandatory fields
            for key in ["id", "ext", "title", "uploader", "uploader_id",
                        "upload_date", "timestamp", "duration", "view_count",
                        "like_count", "categories", "age_limit"]:
                assert key in test["info_dict"], f"Missing '{key}' in info_dict"
        else:
            # only_matching tests should not have info_dict or params
            assert "info_dict" not in test, "only_matching test should not have 'info_dict'"
            assert "params" not in test, "only_matching test should not have 'params'"
