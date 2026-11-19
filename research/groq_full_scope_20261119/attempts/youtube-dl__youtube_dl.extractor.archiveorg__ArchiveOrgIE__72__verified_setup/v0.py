import re
import pytest
from youtube_dl.extractor.archiveorg import ArchiveOrgIE

# Test 1: Validate that the regular expression matches known archive.org URLs
def test_valid_url_matches():
    valid_urls = [
        "http://archive.org/details/XD300-23_68HighlightsAResearchCntAugHumanIntellect",
        "https://archive.org/details/Cops1922",
        "http://archive.org/embed/XD300-23_68HighlightsAResearchCntAugHumanIntellect",
        "https://archive.org/details/MSNBCW_20131125_040000_To_Catch_a_Predator/",
    ]
    pattern = re.compile(ArchiveOrgIE._VALID_URL)
    for url in valid_urls:
        assert pattern.match(url), f"URL should match pattern: {url}"

# Test 2: Ensure that test cases marked with 'only_matching' do not contain an 'info_dict'
def test_only_matching_tests():
    for test in ArchiveOrgIE._TESTS:
        if test.get("only_matching"):
            assert "info_dict" not in test, (
                f"Test case with URL {test['url']} should not contain 'info_dict'"
            )

# Test 3: Verify that each test case with an 'info_dict' contains all required keys
def test_info_dict_keys():
    required_keys = {
        "id", "ext", "title", "description", "timestamp", "upload_date"
    }
    for test in ArchiveOrgIE._TESTS:
        info = test.get("info_dict")
        if info:
            missing = required_keys - info.keys()
            assert not missing, f"Missing keys in info_dict for URL {test['url']}: {missing}"
