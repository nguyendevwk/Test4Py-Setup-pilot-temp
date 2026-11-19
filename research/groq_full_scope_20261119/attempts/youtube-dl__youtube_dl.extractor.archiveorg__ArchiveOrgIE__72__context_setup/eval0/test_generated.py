import re
import pytest
from youtube_dl.extractor.archiveorg import ArchiveOrgIE


def test_valid_url_matches():
    """The _VALID_URL regex should match known archive.org URLs."""
    pattern = re.compile(ArchiveOrgIE._VALID_URL)
    # Valid URLs
    assert pattern.match(
        "http://archive.org/details/XD300-23_68HighlightsAResearchCntAugHumanIntellect"
    )
    assert pattern.match(
        "https://archive.org/embed/XD300-23_68HighlightsAResearchCntAugHumanIntellect"
    )
    # Invalid URLs
    assert not pattern.match("http://example.com/details/abc")
    assert not pattern.match("https://archive.org/invalid/XD300-23")


def test_tests_structure():
    """Each entry in _TESTS should contain the required keys for a valid test."""
    required_keys = {"url", "md5", "info_dict"}
    for test in ArchiveOrgIE._TESTS:
        # Only tests that are not only_matching should contain info_dict
        if test.get("only_matching"):
            continue
        assert "url" in test, "Test entry missing 'url'"
        assert "md5" in test, "Test entry missing 'md5'"
        assert "info_dict" in test, "Test entry missing 'info_dict'"
        info = test["info_dict"]
        # Basic required fields in info_dict
        assert "id" in info, "info_dict missing 'id'"
        assert "ext" in info, "info_dict missing 'ext'"
        assert "title" in info, "info_dict missing 'title'"


def test_real_extract_invalid_url_raises():
    """_real_extract should raise a ValueError when the URL does not match the pattern."""
    ie = ArchiveOrgIE()
    with pytest.raises(ValueError):
        ie._real_extract("https://example.com/invalid/url")
