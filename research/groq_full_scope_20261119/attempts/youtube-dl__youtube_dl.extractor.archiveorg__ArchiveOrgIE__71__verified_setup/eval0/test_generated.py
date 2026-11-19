import re
import pytest
from youtube_dl.extractor.archiveorg import ArchiveOrgIE

def test_valid_url_matches_expected_patterns():
    """The _VALID_URL regex should match both details and embed URLs."""
    valid_urls = [
        "http://archive.org/details/XD300-23_68HighlightsAResearchCntAugHumanIntellect",
        "https://archive.org/embed/XD300-23_68HighlightsAResearchCntAugHumanIntellect",
        "https://www.archive.org/details/Cops1922",
        "http://www.archive.org/embed/Cops1922",
    ]
    invalid_urls = [
        "http://archive.org/invalid/XD300-23",
        "https://archive.org/details/",
        "https://archive.org/embed/",
        "https://example.com/details/XD300-23",
    ]
    pattern = re.compile(ArchiveOrgIE._VALID_URL)
    for url in valid_urls:
        assert pattern.match(url), f"URL should match: {url}"
    for url in invalid_urls:
        assert not pattern.match(url), f"URL should not match: {url}"

def test_tests_structure_and_content():
    """Each entry in _TESTS should contain the required keys."""
    for test in ArchiveOrgIE._TESTS:
        assert "url" in test, "Test entry missing 'url'"
        if test.get("only_matching"):
            # only_matching tests should not contain info_dict or md5
            assert "info_dict" not in test, "only_matching test should not have info_dict"
            assert "md5" not in test, "only_matching test should not have md5"
        else:
            # normal tests must contain info_dict and md5
            assert "info_dict" in test, "Test entry missing 'info_dict'"
            assert "md5" in test, "Test entry missing 'md5'"
            # Ensure info_dict contains required fields
            required_fields = {"id", "ext", "title"}
            missing = required_fields - test["info_dict"].keys()
            assert not missing, f"info_dict missing fields: {missing}"

def test_extract_id_from_url():
    """The _match_id method should correctly extract the video id."""
    ie = ArchiveOrgIE()
    test_cases = {
        "http://archive.org/details/XD300-23_68HighlightsAResearchCntAugHumanIntellect": "XD300-23_68HighlightsAResearchCntAugHumanIntellect",
        "https://archive.org/embed/Cops1922": "Cops1922",
        "https://www.archive.org/details/SomeVideo123": "SomeVideo123",
    }
    for url, expected_id in test_cases.items():
        extracted_id = ie._match_id(url)
        assert extracted_id == expected_id, f"Expected {expected_id} but got {extracted_id}"
