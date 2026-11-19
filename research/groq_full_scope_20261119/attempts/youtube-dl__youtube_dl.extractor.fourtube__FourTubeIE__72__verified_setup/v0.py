import re
import pytest
from youtube_dl.extractor.fourtube import FourTubeIE

def test_valid_url_match():
    """FourTubeIE should correctly extract id and display_id from a valid URL."""
    url = "http://www.4tube.com/videos/209733/hot-babe-holly-michaels-gets-her-ass-stuffed-by-black"
    match = re.match(FourTubeIE._VALID_URL, url)
    assert match is not None, "URL did not match the regex"
    assert match.group("id") == "209733", "Extracted id is incorrect"
    assert match.group("display_id") == "hot-babe-holly-michaels-gets-her-ass-stuffed-by-black", \
        "Extracted display_id is incorrect"

def test_url_template_formatting():
    """The URL_TEMPLATE should produce a correct video page URL when formatted with an id."""
    video_id = "123456"
    expected = f"https://www.4tube.com/videos/{video_id}/video"
    formatted = FourTubeIE._URL_TEMPLATE % video_id
    assert formatted == expected, "URL_TEMPLATE formatting failed"

def test_test_cases_structure():
    """Each test case in _TESTS should contain the required keys for a valid test."""
    required_keys = {"url", "md5", "info_dict"}
    for test in FourTubeIE._TESTS:
        assert "url" in test, "Test case missing 'url'"
        if "only_matching" in test:
            # only_matching tests should not have md5 or info_dict
            assert "md5" not in test and "info_dict" not in test, \
                "only_matching test case should not contain 'md5' or 'info_dict'"
        else:
            assert "md5" in test, "Test case missing 'md5'"
            assert "info_dict" in test, "Test case missing 'info_dict'"
            assert isinstance(test["info_dict"], dict), "'info_dict' should be a dict"
            # Ensure required keys exist in info_dict
            for key in ["id", "ext", "title", "uploader", "uploader_id", "upload_date",
                        "timestamp", "duration", "view_count", "like_count", "categories", "age_limit"]:
                assert key in test["info_dict"], f"info_dict missing key '{key}'"
