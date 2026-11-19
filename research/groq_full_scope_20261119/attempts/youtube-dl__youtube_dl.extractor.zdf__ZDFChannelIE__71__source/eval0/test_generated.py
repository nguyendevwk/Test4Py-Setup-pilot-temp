import re
import pytest
from youtube_dl.extractor.zdf import ZDFChannelIE

# Test 1: Verify that the _VALID_URL regex correctly extracts the channel id
def test_valid_url_extraction():
    url = "https://www.zdf.de/sport/das-aktuelle-sportstudio"
    match = re.match(ZDFChannelIE._VALID_URL, url)
    assert match is not None, "URL should match the _VALID_URL pattern"
    assert match.group("id") == "das-aktuelle-sportstudio", "Extracted id should match expected value"

# Test 2: Verify that the _match_id method returns the same id as extracted by the regex
def test_match_id_method():
    url = "https://www.zdf.de/dokumentation/planet-e"
    extractor = ZDFChannelIE()
    extracted_id = extractor._match_id(url)
    assert extracted_id == "planet-e", "The _match_id method should return the correct channel id"

# Test 3: Verify that URLs not matching the pattern are rejected by the regex
def test_invalid_url_rejection():
    url = "https://www.zdf.de/filme/taunuskrimi/"
    match = re.match(ZDFChannelIE._VALID_URL, url)
    assert match is None, "URL should not match the _VALID_URL pattern for this case"
