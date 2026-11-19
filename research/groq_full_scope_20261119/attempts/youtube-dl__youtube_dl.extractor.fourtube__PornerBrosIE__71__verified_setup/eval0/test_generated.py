import re
import pytest
from youtube_dl.extractor.fourtube import PornerBrosIE

# Test 1: Verify that the _VALID_URL regex correctly extracts the id and kind
def test_valid_url_parsing():
    url = "https://www.pornerbros.com/videos/skinny-brunette-takes-big-cock-down-her-anal-hole_181369"
    match = re.match(PornerBrosIE._VALID_URL, url)
    assert match is not None, "URL should match the regex"
    assert match.group("id") == "181369", "Extracted id should be '181369'"
    assert match.group("kind") == "www", "Extracted kind should be 'www'"

# Test 2: Verify that the URL template is correctly formatted with the extracted id
def test_url_template():
    video_id = "181369"
    expected = "https://www.pornerbros.com/videos/video_181369"
    assert PornerBrosIE._URL_TEMPLATE % video_id == expected, "URL template formatting failed"

# Test 3: Verify that an invalid URL does not match the regex
def test_invalid_url():
    url = "https://www.pornerbros.com/invalid/12345"
    assert re.match(PornerBrosIE._VALID_URL, url) is None, "Invalid URL should not match the regex"
