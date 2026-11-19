import pytest
from youtube_dl.extractor.nrk import NRKTVIE

def test_real_extract_valid_url_returns_expected_result():
    ie = NRKTVIE()
    url = "https://tv.nrk.no/program/MDDP12000117"
    result = ie._real_extract(url)
    assert isinstance(result, dict)
    assert result["url"] == "nrk:MDDP12000117"
    assert result["ie_key"] == "NRKIE"
    assert result["video_id"] == "MDDP12000117"

def test_real_extract_invalid_url_raises_error():
    ie = NRKTVIE()
    invalid_url = "https://tv.nrk.no/program/INVALID123"
    with pytest.raises(Exception):
        ie._real_extract(invalid_url)

def test_real_extract_boundary_case_missing_id():
    ie = NRKTVIE()
    boundary_url = "https://tv.nrk.no/program/"
    with pytest.raises(Exception):
        ie._real_extract(boundary_url)
