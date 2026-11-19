import re
import pytest
from youtube_dl.extractor.nrk import NRKSkoleIE

def test_valid_url_parsing():
    """The extractor should correctly extract the mediaId from a valid URL."""
    extractor = NRKSkoleIE()
    url = "https://www.nrk.no/skole/?page=search&q=&mediaId=14099"
    match = re.match(extractor._VALID_URL, url)
    assert match is not None, "URL should match the extractor pattern"
    assert match.group("id") == "14099", "Extracted mediaId should be '14099'"

def test_test_cases_structure():
    """Each test case in _TESTS should contain the required keys."""
    for test in NRKSkoleIE._TESTS:
        assert "url" in test, "Test case must have a 'url' key"
        if "only_matching" in test:
            assert isinstance(test["only_matching"], bool), "'only_matching' must be a bool"
        else:
            assert "md5" in test, "Test case must have an 'md5' key"
            assert "info_dict" in test, "Test case must have an 'info_dict' key"
            info = test["info_dict"]
            for key in ("id", "ext", "title", "description", "duration"):
                assert key in info, f"info_dict must contain '{key}'"

def test_invalid_url_raises():
    """Providing an URL that does not match should raise ExtractorError."""
    extractor = NRKSkoleIE()
    invalid_url = "https://www.example.com/not-nrk"
    with pytest.raises(extractor.IEError):
        extractor._match_id(invalid_url)
