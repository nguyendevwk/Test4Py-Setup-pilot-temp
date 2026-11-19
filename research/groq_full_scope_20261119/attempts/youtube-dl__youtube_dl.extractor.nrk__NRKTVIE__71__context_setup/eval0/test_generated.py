import pytest
from youtube_dl.extractor.nrk import NRKTVIE
from youtube_dl.utils import ExtractorError


def test_real_extract_returns_expected_url_result():
    """Verify that _real_extract returns a url_result with the correct format."""
    extractor = NRKTVIE()
    url = "https://tv.nrk.no/program/MDDP12000117"
    result = extractor._real_extract(url)
    # The result should be a URLResult instance pointing to the NRKIE extractor
    assert result.url == "nrk:MDDP12000117"
    assert result.ie == "NRKIE"
    assert result.video_id == "MDDP12000117"


def test_real_extract_with_series_and_episode_url():
    """Test extraction for a URL containing series and episode information."""
    extractor = NRKTVIE()
    url = "https://tv.nrk.no/serie/20-spoersmaal-tv/MUHH48000314/23-05-2014"
    result = extractor._real_extract(url)
    assert result.url == "nrk:MUHH48000314"
    assert result.ie == "NRKIE"
    assert result.video_id == "MUHH48000314"


def test_real_extract_invalid_url_raises_error():
    """Ensure that an invalid URL raises ExtractorError."""
    extractor = NRKTVIE()
    invalid_url = "https://tv.nrk.no/invalid/1234"
    with pytest.raises(ExtractorError):
        extractor._real_extract(invalid_url)
