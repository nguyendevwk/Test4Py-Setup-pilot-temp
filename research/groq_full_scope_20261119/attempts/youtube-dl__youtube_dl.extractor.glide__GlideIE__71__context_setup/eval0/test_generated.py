import re
import pytest
from youtube_dl.extractor.glide import GlideIE

def test_valid_url_pattern_matches_expected_id():
    """The _VALID_URL regex should capture the video id from a typical Glide URL."""
    url = "https://share.glide.me/UZF8zlmuQbe4mr+7dCiQ0w=="
    match = re.match(GlideIE._VALID_URL, url)
    assert match is not None, "URL should match the _VALID_URL pattern"
    assert match.group("id") == "UZF8zlmuQbe4mr+7dCiQ0w==", "Captured id should match the expected value"

def test_test_dict_contains_required_keys_and_types():
    """The _TEST dictionary should contain the required keys with correct types."""
    test = GlideIE._TEST
    assert isinstance(test, dict), "_TEST should be a dictionary"
    for key in ("url", "md5", "info_dict"):
        assert key in test, f"_TEST missing required key: {key}"
    assert isinstance(test["url"], str), "URL in _TEST should be a string"
    assert isinstance(test["md5"], str), "MD5 in _TEST should be a string"
    assert isinstance(test["info_dict"], dict), "info_dict in _TEST should be a dictionary"

def test_info_dict_contains_expected_fields_and_patterns():
    """The info_dict in _TEST should contain the expected fields with correct patterns."""
    info = GlideIE._TEST["info_dict"]
    expected_keys = {"id", "ext", "title", "thumbnail"}
    assert expected_keys == set(info.keys()), "info_dict should contain exactly the expected keys"
    assert info["id"] == "UZF8zlmuQbe4mr+7dCiQ0w==", "info_dict id should match the test id"
    assert info["ext"] == "mp4", "info_dict ext should be 'mp4'"
    assert isinstance(info["title"], str), "info_dict title should be a string"
    assert isinstance(info["thumbnail"], str), "info_dict thumbnail should be a string"
    # The thumbnail should match the provided regex pattern
    thumbnail_pattern = re.compile(info["thumbnail"])
    assert thumbnail_pattern.match("https://example.cloudfront.net/image.jpg"), "thumbnail pattern should match a valid URL"
