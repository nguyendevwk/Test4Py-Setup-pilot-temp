import re
import pytest
from youtube_dl.extractor.tvplay import TVPlayHomeIE
from youtube_dl.utils import ExtractorError

# Test 1: Verify that the extractor correctly extracts the video ID from a valid URL.
def test_match_id_extraction(tmp_path):
    ie = TVPlayHomeIE()
    url = "https://tvplay.tv3.lt/aferistai-n-7/aferistai-10047125/"
    # The ID should be the numeric part after the last hyphen.
    expected_id = "10047125"
    extracted_id = ie._match_id(url)
    assert extracted_id == expected_id, f"Expected ID {expected_id}, got {extracted_id}"

# Test 2: Verify that an invalid URL raises an ExtractorError when attempting to match.
def test_invalid_url_raises_error(tmp_path):
    ie = TVPlayHomeIE()
    invalid_url = "https://example.com/not-a-tvplay-url"
    with pytest.raises(ExtractorError):
        ie._match_id(invalid_url)

# Test 3: Verify that the _VALID_URL regex matches all URLs listed in the _TESTS.
def test_valid_url_pattern_matches_all_test_cases(tmp_path):
    pattern = re.compile(TVPlayHomeIE._VALID_URL)
    for test in TVPlayHomeIE._TESTS:
        url = test["url"]
        assert pattern.match(url), f"URL {url} did not match the _VALID_URL pattern"
