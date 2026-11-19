import pytest
from youtube_dl.extractor.nrk import NRKTVIE
from youtube_dl.utils import ExtractorError

def test_real_extract_returns_expected_result():
    ie = NRKTVIE()
    url = "https://tv.nrk.no/program/MDDP12000117"
    result = ie._real_extract(url)
    assert result.url == "nrk:MDDP12000117"
    assert result.ie == "NRKIE"
    assert result.video_id == "MDDP12000117"

def test_real_extract_with_series_episode_url():
    ie = NRKTVIE()
    url = "https://tv.nrk.no/serie/20-spoersmaal-tv/MUHH48000314/23-05-2014"
    result = ie._real_extract(url)
    assert result.url == "nrk:MUHH48000314"
    assert result.ie == "NRKIE"
    assert result.video_id == "MUHH48000314"

def test_real_extract_invalid_url_raises_error():
    ie = NRKTVIE()
    invalid_url = "https://tv.nrk.no/invalid/12345"
    with pytest.raises(ExtractorError):
        ie._real_extract(invalid_url)
