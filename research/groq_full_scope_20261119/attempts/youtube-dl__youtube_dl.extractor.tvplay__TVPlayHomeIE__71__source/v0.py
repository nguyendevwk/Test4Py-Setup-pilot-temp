import re
import pytest
from youtube_dl.extractor.tvplay import TVPlayHomeIE

# Test 1: Validate that the regular expression correctly extracts the video id
def test_valid_url_id_extraction():
    url = "https://tvplay.tv3.lt/aferistai-n-7/aferistai-10047125/"
    match = re.match(TVPlayHomeIE._VALID_URL, url)
    assert match is not None, "URL should match the extractor pattern"
    assert match.group("id") == "10047125", "Extracted id should match the numeric suffix"

# Test 2: Ensure that the extractor's _TESTS list contains at least one full test case
def test_tests_list_contains_full_test():
    full_test = next((t for t in TVPlayHomeIE._TESTS if "info_dict" in t), None)
    assert full_test is not None, "There should be at least one full test case in _TESTS"
    info = full_test["info_dict"]
    required_keys = {"id", "ext", "title", "description", "series",
                     "season", "season_number", "duration",
                     "timestamp", "upload_date", "age_limit"}
    assert required_keys.issubset(info.keys()), "info_dict should contain all required keys"

# Test 3: Verify that the extractor correctly identifies URLs that should only be matched
def test_only_matching_urls():
    only_matching_urls = [
        t["url"] for t in TVPlayHomeIE._TESTS if t.get("only_matching")
    ]
    for url in only_matching_urls:
        assert re.match(TVPlayHomeIE._VALID_URL, url), f"URL {url} should match the pattern"
        # The extractor should not provide an info_dict for these URLs
        test_entry = next(t for t in TVPlayHomeIE._TESTS if t["url"] == url)
        assert "info_dict" not in test_entry, f"URL {url} should not have an info_dict"
