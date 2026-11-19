import re
import pytest
from youtube_dl.extractor.fourtube import PornTubeIE

# Test that the regular expression correctly captures the groups for a standard URL
def test_valid_url_parsing():
    url = "https://www.porntube.com/videos/teen-couple-doing-anal_7089759"
    match = re.match(PornTubeIE._VALID_URL, url)
    assert match is not None, "URL should match the pattern"
    video_id, display_id = match.group('id', 'display_id')
    assert video_id == "7089759", f"Expected video_id '7089759', got {video_id}"
    assert display_id == "teen-couple-doing-anal", f"Expected display_id 'teen-couple-doing-anal', got {display_id}"

# Test that the regular expression also matches the embed form
def test_embed_url_parsing():
    url = "https://www.porntube.com/embed/7089759"
    match = re.match(PornTubeIE._VALID_URL, url)
    assert match is not None, "Embed URL should match the pattern"
    video_id, display_id = match.group('id', 'display_id')
    assert video_id == "7089759", f"Expected video_id '7089759', got {video_id}"
    assert display_id is None, f"Expected display_id None, got {display_id}"

# Test that an invalid URL raises an AttributeError due to missing match groups
def test_invalid_url_raises():
    url = "https://example.com/not-a-porn-tube-url"
    with pytest.raises(AttributeError):
        PornTubeIE()._real_extract(url)
