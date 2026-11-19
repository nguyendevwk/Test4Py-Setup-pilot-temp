import pytest
from youtube_dl.extractor.nrk import NRKRadioPodkastIE

def test_valid_url_parsing():
    """Test that a valid NRK radio podcast URL is parsed correctly."""
    url = "https://radio.nrk.no/podkast/ulrikkes_univers/l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"
    ie = NRKRadioPodkastIE()
    result = ie._real_extract(url)
    # The result should be a dict with a 'url' key pointing to the NRKIE URL
    assert isinstance(result, dict)
    assert result["url"] == "nrk:l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"
    # The 'ie' key should be the key of the NRKIE extractor
    assert result["ie"] == "NRKIE"
    # The 'video_id' should match the captured ID
    assert result["video_id"] == "l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"

def test_only_matching_urls():
    """Test that URLs matching the pattern but not intended for extraction return only_matching."""
    ie = NRKRadioPodkastIE()
    # These URLs should match the regex but are marked as only_matching in _TESTS
    urls = [
        "https://radio.nrk.no/podcast/ulrikkes_univers/l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8",
        "https://radio.nrk.no/podkast/ulrikkes_univers/sesong/1/l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8",
        "https://radio.nrk.no/podkast/hele_historien/sesong/bortfoert-i-bergen/l_774d1a2c-7aa7-4965-8d1a-2c7aa7d9652c",
    ]
    for url in urls:
        # _match_id should succeed because the regex matches
        video_id = ie._match_id(url)
        assert video_id is not None
        # But _real_extract should still produce the same result structure
        result = ie._real_extract(url)
        assert result["url"] == f"nrk:{video_id}"
        assert result["ie"] == "NRKIE"
        assert result["video_id"] == video_id

def test_invalid_url_raises():
    """Test that an invalid URL raises ExtractorError."""
    ie = NRKRadioPodkastIE()
    invalid_url = "https://radio.nrk.no/invalid/path/l_12345678-1234-1234-1234-123456789abc"
    with pytest.raises(ie.IEError):
        ie._real_extract(invalid_url)
