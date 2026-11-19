import re
import pytest
from youtube_dl.extractor.nrk import NRKRadioPodkastIE
from youtube_dl.utils import ExtractorError

# Test 1: Validate that the regex matches a correct NRK podcast URL and extracts the ID
def test_valid_url_extraction():
    url = "https://radio.nrk.no/podkast/ulrikkes_univers/l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"
    match = re.match(NRKRadioPodkastIE._VALID_URL, url)
    assert match is not None, "URL should match the _VALID_URL pattern"
    extracted_id = match.group("id")
    assert extracted_id == "l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"

# Test 2: Ensure that _real_extract returns the expected url_result structure
def test_real_extract_returns_expected_result():
    url = "https://radio.nrk.no/podkast/ulrikkes_univers/l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"
    ie = NRKRadioPodkastIE()
    result = ie._real_extract(url)
    # The result should be a dict with keys 'url', 'ie_key', and 'video_id'
    assert isinstance(result, dict), "Result should be a dictionary"
    assert result["url"] == "nrk:l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"
    assert result["ie_key"] == "NRKIE"
    assert result["video_id"] == "l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"

# Test 3: Verify that an invalid URL raises an ExtractorError due to no match
def test_invalid_url_raises_error():
    invalid_url = "https://radio.nrk.no/invalid/endpoint/l_12345678-1234-1234-1234-123456789abc"
    ie = NRKRadioPodkastIE()
    with pytest.raises(ExtractorError):
        ie._real_extract(invalid_url)
