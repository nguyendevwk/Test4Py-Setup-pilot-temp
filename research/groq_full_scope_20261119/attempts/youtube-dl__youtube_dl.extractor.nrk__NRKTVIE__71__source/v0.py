import pytest
from youtube_dl.extractor.nrk import NRKTVIE
from youtube_dl.utils import ExtractorError

def test_real_extract_returns_expected_url_result():
    ie = NRKTVIE()
    url = "https://tv.nrk.no/program/MDDP12000117"
    result = ie._real_extract(url)
    # The result should be a URLResult pointing to the NRKIE extractor
    assert result._url == "nrk:MDDP12000117"
    assert result.ie_key() == "NRKIE"
    assert result.video_id == "MDDP12000117"

def test_real_extract_with_invalid_url_raises():
    ie = NRKTVIE()
    invalid_url = "https://tv.nrk.no/invalid/XYZ"
    with pytest.raises(ExtractorError):
        ie._real_extract(invalid_url)

def test_real_extract_handles_different_valid_patterns():
    ie = NRKTVIE()
    # Pattern with series and episode
    url = "https://tv.nrk.no/serie/20-spoersmaal-tv/MUHH48000314/23-05-2014"
    result = ie._real_extract(url)
    assert result._url == "nrk:MUHH48000314"
    assert result.video_id == "MUHH48000314"
