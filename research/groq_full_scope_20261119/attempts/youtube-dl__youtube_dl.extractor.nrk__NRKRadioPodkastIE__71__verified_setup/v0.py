import pytest
from youtube_dl.extractor.nrk import NRKRadioPodkastIE, NRKIE
from youtube_dl.utils import ExtractorError

# Test 1: Normal extraction of a valid NRK radio podcast URL
def test_nrk_radio_podkast_extraction(tmp_path):
    url = "https://radio.nrk.no/podkast/ulrikkes_univers/l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"
    ie = NRKRadioPodkastIE()
    result = ie._real_extract(url)
    # The result should be a URLResult with the expected format
    assert result.url == "nrk:l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"
    assert result.ie_key() == NRKIE.ie_key()
    # The video_id passed to the result should match the captured group
    assert result.video_id == "l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"

# Test 2: Extraction should raise an error for a URL that does not match the pattern
def test_nrk_radio_podkast_invalid_url():
    ie = NRKRadioPodkastIE()
    invalid_url = "https://radio.nrk.no/invalid/path/l_12345678-1234-1234-1234-123456789abc"
    with pytest.raises(ExtractorError):
        ie._real_extract(invalid_url)

# Test 3: Boundary case – URL with the shortest valid path
def test_nrk_radio_podkast_boundary_url():
    # Minimal path that still satisfies the regex: /podkast/<id>
    url = "https://radio.nrk.no/podkast/l_00000000-0000-0000-0000-000000000000"
    ie = NRKRadioPodkastIE()
    result = ie._real_extract(url)
    assert result.url == "nrk:l_00000000-0000-0000-0000-000000000000"
    assert result.video_id == "l_00000000-0000-0000-0000-000000000000"
