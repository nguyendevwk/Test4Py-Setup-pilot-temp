import re
import pytest
from youtube_dl.extractor.tvplay import TVPlayHomeIE

# Test 1: Validate the regular expression matches expected URLs and captures the ID correctly.
def test_valid_url_regex_matches_and_captures_id():
    ie = TVPlayHomeIE()
    # A URL that should match and contain ID 10047125
    url = "https://tvplay.tv3.lt/aferistai-n-7/aferistai-10047125/"
    match = re.match(ie._VALID_URL, url)
    assert match is not None, f"URL {url} did not match the regex"
    assert match.group('id') == "10047125", f"Captured ID {match.group('id')} != 10047125"

    # A URL that should not match (missing trailing slash and hyphen)
    bad_url = "https://tvplay.tv3.lt/aferistai-n-7/aferistai10047125"
    assert re.match(ie._VALID_URL, bad_url) is None, f"Bad URL {bad_url} incorrectly matched"

# Test 2: Ensure that the _match_id method extracts the correct ID from a valid URL.
def test_match_id_extraction():
    ie = TVPlayHomeIE()
    url = "https://play.tv3.lt/aferistai-10047125"
    # The regex should still match because of the _VALID_URL pattern
    video_id = ie._match_id(url)
    assert video_id == "10047125", f"_match_id returned {video_id} instead of 10047125"

# Test 3: Verify that URLs marked with 'only_matching': True in _TESTS are indeed only matching
# and do not provide any additional info_dict or params.
def test_only_matching_urls_in_tests():
    ie = TVPlayHomeIE()
    for test in ie._TESTS:
        if test.get('only_matching'):
            url = test['url']
            # The URL should match the regex
            assert re.match(ie._VALID_URL, url), f"URL {url} marked only_matching but does not match regex"
            # The test dict should not contain 'info_dict' or 'params'
            assert 'info_dict' not in test, f"only_matching test {url} contains info_dict"
            assert 'params' not in test, f"only_matching test {url} contains params"
