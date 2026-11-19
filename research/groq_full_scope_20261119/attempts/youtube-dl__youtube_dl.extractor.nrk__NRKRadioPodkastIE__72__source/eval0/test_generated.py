import pytest
from youtube_dl.extractor.nrk import NRKRadioPodkastIE
from youtube_dl.utils import ExtractorError

# Test 1: Normal extraction of a known NRK radio podcast URL
def test_nrk_radio_podkast_extraction(tmp_path):
    ie = NRKRadioPodkastIE()
    url = "https://radio.nrk.no/podkast/ulrikkes_univers/l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"
    assert ie.suitable(url) is True
    result = ie.extract_info(url, download=False)
    # The extractor should return a dict with the expected keys
    assert isinstance(result, dict)
    assert result["id"] == "l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"
    assert result["ie_key"] == "NRKIE"
    assert result["url"] == "nrk:l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"
    # The result should be a URL result pointing to the NRKIE extractor
    assert result["ie_key"] == "NRKIE"
    assert result["url"].startswith("nrk:")

# Test 2: URL that matches the pattern but is not suitable for extraction
def test_nrk_radio_podkast_unsuitable_url():
    ie = NRKRadioPodkastIE()
    # This URL matches the regex but the id part is not a valid UUID-like string
    url = "https://radio.nrk.no/podkast/invalid/l_1234"
    assert ie.suitable(url) is False

# Test 3: Extraction of an unsuitable URL should raise ExtractorError
def test_nrk_radio_podkast_extraction_error():
    ie = NRKRadioPodkastIE()
    # URL that does not match the extractor's pattern
    url = "https://radio.nrk.no/other/invalid/url"
    with pytest.raises(ExtractorError):
        ie.extract_info(url, download=False)
