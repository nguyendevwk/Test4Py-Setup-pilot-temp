import re
import pytest

# Import the target class from the production source
from youtube_dl.extractor.fourtube import PornTubeIE

# Test 1: Verify that a typical PornTube URL matches the regex and captures the correct groups.
def test_valid_url_parsing():
    url = "https://www.porntube.com/videos/teen-couple-doing-anal_7089759"
    match = re.match(PornTubeIE._VALID_URL, url)
    assert match is not None, "URL should match the _VALID_URL pattern"
    assert match.group('id') == "7089759", "Video ID should be captured correctly"
    assert match.group('display_id') == "teen-couple-doing-anal", "Display ID should be captured correctly"
    assert match.group('kind') == "www", "Kind should be captured correctly"

# Test 2: Verify that a mobile variant URL also matches and captures the correct kind.
def test_mobile_url_parsing():
    url = "https://m.porntube.com/videos/teen-couple-doing-anal_7089759"
    match = re.match(PornTubeIE._VALID_URL, url)
    assert match is not None, "Mobile URL should match the _VALID_URL pattern"
    assert match.group('kind') == "m", "Kind should be 'm' for mobile URLs"

# Test 3: Verify that URLs not conforming to the pattern do not match.
def test_invalid_url_rejection():
    url = "https://www.porntube.com/invalid/path/12345"
    match = re.match(PornTubeIE._VALID_URL, url)
    assert match is None, "Non-matching URL should return None from re.match"
