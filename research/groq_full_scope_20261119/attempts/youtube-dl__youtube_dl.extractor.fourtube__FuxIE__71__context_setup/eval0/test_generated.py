import re
import pytest
from youtube_dl.extractor.fourtube import FuxIE


def test_valid_url_groups():
    """Test that the regular expression captures the expected groups."""
    url = "https://www.fux.com/video/195359/awesome-fucking-kitchen-ends-cum-swallow"
    match = re.match(FuxIE._VALID_URL, url)
    assert match is not None, "URL should match the pattern"
    kind, video_id, display_id = match.group('kind', 'id', 'display_id')
    assert kind == 'www', f"Expected kind 'www', got {kind}"
    assert video_id == '195359', f"Expected id '195359', got {video_id}"
    assert display_id == 'awesome-fucking-kitchen-ends-cum-swallow', (
        f"Expected display_id 'awesome-fucking-kitchen-ends-cum-swallow', got {display_id}"
    )


def test_url_template_substitution():
    """Test that the URL template is correctly formed from a video id."""
    video_id = "123456"
    expected = "https://www.fux.com/video/123456/video"
    actual = FuxIE._URL_TEMPLATE % video_id
    assert actual == expected, f"URL template substitution failed: {actual}"


def test_invalid_url_raises():
    """Test that providing an invalid URL raises a ValueError during extraction."""
    fux_ie = FuxIE()
    invalid_url = "https://www.example.com/not-a-fux-url"
    with pytest.raises(ValueError):
        fux_ie._real_extract(invalid_url)
