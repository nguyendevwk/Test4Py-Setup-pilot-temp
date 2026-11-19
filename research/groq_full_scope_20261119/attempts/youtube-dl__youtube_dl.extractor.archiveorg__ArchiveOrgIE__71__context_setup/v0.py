import re
import pytest
from youtube_dl.extractor.archiveorg import ArchiveOrgIE

# Test 1: Validate the regular expression used for matching URLs
def test_valid_url_regex_matches_expected_patterns():
    regex = re.compile(ArchiveOrgIE._VALID_URL)
    # Expected to match both 'details' and 'embed' paths
    assert regex.match('http://archive.org/details/XD300-23_68HighlightsAResearchCntAugHumanIntellect')
    assert regex.match('https://archive.org/embed/XD300-23_68HighlightsAResearchCntAugHumanIntellect')
    # Should not match URLs with different path or domain
    assert not regex.match('http://archive.org/invalid/XD300-23')
    assert not regex.match('https://example.com/details/XD300-23')

# Test 2: Ensure that the test cases defined in the extractor contain required keys
def test_extractor_tests_structure():
    for test in ArchiveOrgIE._TESTS:
        # Every test must have a 'url' key
        assert 'url' in test, "Test case missing 'url' key"
        # If the test expects a full extraction, it must contain 'info_dict'
        if not test.get('only_matching'):
            assert 'info_dict' in test, "Test case missing 'info_dict' key"
            # The info_dict should at least contain an 'id' field
            assert 'id' in test['info_dict'], "info_dict missing 'id' field"

# Test 3: Verify that the extractor reports suitability correctly
def test_extractor_suitability():
    extractor = ArchiveOrgIE()
    # URLs that should be considered suitable
    suitable_urls = [
        'http://archive.org/details/XD300-23_68HighlightsAResearchCntAugHumanIntellect',
        'https://archive.org/embed/XD300-23_68HighlightsAResearchCntAugHumanIntellect',
    ]
    for url in suitable_urls:
        assert extractor.suitable(url), f"Extractor should be suitable for {url}"
    # URLs that should not be considered suitable
    unsuitable_urls = [
        'http://archive.org/invalid/XD300-23',
        'https://example.com/details/XD300-23',
    ]
    for url in unsuitable_urls:
        assert not extractor.suitable(url), f"Extractor should not be suitable for {url}"
