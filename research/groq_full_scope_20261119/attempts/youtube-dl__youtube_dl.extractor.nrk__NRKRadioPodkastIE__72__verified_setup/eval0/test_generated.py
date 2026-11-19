import pytest
from youtube_dl.extractor.nrk import NRKRadioPodkastIE
from youtube_dl.utils import ExtractorError

# Test 1: Normal extraction of a valid NRK radio podcast URL
def test_nrk_radio_podkast_extraction(tmp_path):
    ie = NRKRadioPodkastIE()
    url = "https://radio.nrk.no/podkast/ulrikkes_univers/l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"
    result = ie._real_extract(url)
    # The result should be a URLResult pointing to the NRKIE extractor
    assert result._url.startswith("nrk:")
    assert result._url.endswith("l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8")
    assert result.ie_key() == "NRKIE"

# Test 2: Extraction should raise ExtractorError for a URL that does not match the pattern
def test_nrk_radio_podkast_invalid_url():
    ie = NRKRadioPodkastIE()
    invalid_url = "https://radio.nrk.no/invalid/endpoint/l_12345678-1234-1234-1234-123456789012"
    with pytest.raises(ExtractorError):
        ie._real_extract(invalid_url)

# Test 3: Ensure that URLs matching only the pattern but not the full path raise no error
def test_nrk_radio_podkast_only_matching_url():
    ie = NRKRadioPodkastIE()
    # This URL matches the regex but is intended for only_matching tests
    url = "https://radio.nrk.no/podcast/ulrikkes_univers/l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"
    # The extractor should still process it because the regex matches
    result = ie._real_extract(url)
    assert result._url.startswith("nrk:")
    assert result.ie_key() == "NRKIE"
