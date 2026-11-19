import pytest
from youtube_dl.extractor.nrk import NRKTVIE
from youtube_dl.utils import ExtractorError

def test_real_extract_returns_expected_url_result():
    """Test that _real_extract returns a url_result with correct video_id."""
    ie = NRKTVIE()
    url = "https://tv.nrk.no/program/MDDP12000117"
    result = ie._real_extract(url)
    # The result should be a URLResult pointing to the NRKIE extractor
    assert result._ie_key == "NRKIE"
    assert result._url == "nrk:MDDP12000117"
    assert result._video_id == "MDDP12000117"

def test_real_extract_with_series_episode_url():
    """Test that _real_extract handles series episode URLs correctly."""
    ie = NRKTVIE()
    url = "https://tv.nrk.no/serie/20-spoersmaal-tv/MUHH48000314/23-05-2014"
    result = ie._real_extract(url)
    assert result._video_id == "MUHH48000314"
    assert result._url == "nrk:MUHH48000314"

def test_real_extract_invalid_url_raises_error():
    """Test that an invalid URL raises ExtractorError."""
    ie = NRKTVIE()
    invalid_url = "https://tv.nrk.no/invalid/12345"
    with pytest.raises(ExtractorError):
        ie._real_extract(invalid_url)
