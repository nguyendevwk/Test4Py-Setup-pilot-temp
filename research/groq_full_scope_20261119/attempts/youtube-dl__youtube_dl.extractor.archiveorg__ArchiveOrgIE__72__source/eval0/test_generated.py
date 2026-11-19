import re
import pytest
from youtube_dl.extractor.archiveorg import ArchiveOrgIE

# Test that the regular expression correctly extracts the video ID from a valid URL
def test_valid_url_extraction():
    url = "https://archive.org/details/XD300-23_68HighlightsAResearchCntAugHumanIntellect"
    ie = ArchiveOrgIE()
    video_id = ie._match_id(url)
    assert video_id == "XD300-23_68HighlightsAResearchCntAugHumanIntellect"

# Test that the extractor reports suitable for a known valid URL
def test_suitable_url():
    url = "http://archive.org/embed/XD300-23_68HighlightsAResearchCntAugHumanIntellect"
    ie = ArchiveOrgIE()
    assert ie.suitable(url) is True

# Test that the extractor rejects an invalid URL format
def test_invalid_url_rejection():
    url = "https://example.com/details/invalid"
    ie = ArchiveOrgIE()
    # The _match_id method should raise a ValueError because the URL does not match the pattern
    with pytest.raises(ValueError):
        ie._match_id(url)
