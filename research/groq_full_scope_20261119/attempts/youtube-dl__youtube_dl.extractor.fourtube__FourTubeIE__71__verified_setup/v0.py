import re
import pytest
from youtube_dl.extractor.fourtube import FourTubeIE

# Test 1: Verify that the extractor recognises a valid 4tube URL
def test_fourtube_suitable_valid_url():
    extractor = FourTubeIE()
    url = "http://www.4tube.com/videos/209733/hot-babe-holly-michaels-gets-her-ass-stuffed-by-black"
    assert extractor.suitable(url) is True

# Test 2: Verify that the extractor rejects an unrelated URL
def test_fourtube_suitable_invalid_url():
    extractor = FourTubeIE()
    url = "https://example.com/videos/12345"
    assert extractor.suitable(url) is False

# Test 3: Verify that the URL template is correctly formatted with a video ID
def test_fourtube_url_template_format():
    video_id = "209733"
    expected_url = f"https://www.4tube.com/videos/{video_id}/video"
    assert FourTubeIE._URL_TEMPLATE % video_id == expected_url
