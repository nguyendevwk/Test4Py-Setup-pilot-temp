import re
import pytest
from youtube_dl.extractor.fourtube import FourTubeIE

def test_valid_url_parsing():
    """FourTubeIE should correctly parse a valid URL into its components."""
    url = "http://www.4tube.com/videos/12345/some-title"
    match = re.match(FourTubeIE._VALID_URL, url)
    assert match is not None, "URL should match the regex"
    kind, video_id, display_id = match.group('kind', 'id', 'display_id')
    assert kind == 'www', f"Expected 'www', got {kind}"
    assert video_id == '12345', f"Expected '12345', got {video_id}"
    assert display_id == 'some-title', f"Expected 'some-title', got {display_id}"

def test_invalid_url_raises():
    """FourTubeIE should raise a ValueError when given an invalid URL."""
    invalid_url = "http://example.com/not-a-4tube-url"
    with pytest.raises(ValueError):
        FourTubeIE()._real_extract(invalid_url)

def test_url_template_substitution():
    """The URL template should correctly format a video ID into a full URL."""
    video_id = "98765"
    expected = "https://www.4tube.com/videos/98765/video"
    result = FourTubeIE._URL_TEMPLATE % video_id
    assert result == expected, f"Expected {expected}, got {result}"
