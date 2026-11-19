import re
import pytest
from youtube_dl.extractor.archiveorg import ArchiveOrgIE

# Test 1: Verify that the extractor correctly extracts the video ID from a valid URL
def test_extract_video_id():
    extractor = ArchiveOrgIE()
    url = "https://archive.org/details/XD300-23_68HighlightsAResearchCntAugHumanIntellect"
    # _match_id uses the _VALID_URL regex to capture the ID
    video_id = extractor._match_id(url)
    assert video_id == "XD300-23_68HighlightsAResearchCntAugHumanIntellect"

# Test 2: Verify that the extractor's _VALID_URL regex matches URLs that should be handled
def test_valid_url_matching():
    extractor = ArchiveOrgIE()
    valid_urls = [
        "http://archive.org/details/Cops1922",
        "https://archive.org/embed/XD300-23_68HighlightsAResearchCntAugHumanIntellect",
        "http://archive.org/details/MSNBCW_20131125_040000_To_Catch_a_Predator/",
    ]
    for url in valid_urls:
        assert extractor.suitable(url) is True, f"URL should be suitable: {url}"
    # Ensure that a non-archive.org URL is not matched
    assert extractor.suitable("https://example.com/video") is False

# Test 3: Verify that an invalid URL raises a ValueError when attempting to match the ID
def test_invalid_url_raises():
    extractor = ArchiveOrgIE()
    invalid_url = "https://archive.org/invalid/12345"
    with pytest.raises(ValueError):
        extractor._match_id(invalid_url)
