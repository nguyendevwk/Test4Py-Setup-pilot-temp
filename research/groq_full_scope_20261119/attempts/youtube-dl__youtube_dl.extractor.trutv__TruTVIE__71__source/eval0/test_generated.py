import re
import pytest
from youtube_dl.extractor.trutv import TruTVIE

# Test that the regex correctly extracts groups for a clip URL
def test_trutv_clip_url_parsing():
    url = "https://www.trutv.com/shows/the-carbonaro-effect/videos/sunlight-activated-flower.html"
    match = re.match(TruTVIE._VALID_URL, url)
    assert match is not None, "URL should match the regex"
    series_slug, clip_slug, video_id = match.groups()
    assert series_slug == "the-carbonaro-effect"
    assert clip_slug == "sunlight-activated-flower"
    assert video_id is None, "Clip URL should not contain a numeric id"

# Test that the regex correctly extracts groups for an episode URL
def test_trutv_episode_url_parsing():
    url = "https://www.trutv.com/shows/the-carbonaro-effect/12345"
    match = re.match(TruTVIE._VALID_URL, url)
    assert match is not None, "URL should match the regex"
    series_slug, clip_slug, video_id = match.groups()
    assert series_slug == "the-carbonaro-effect"
    assert clip_slug is None, "Episode URL should not contain a clip slug"
    assert video_id == "12345", "Episode URL should contain the numeric id"

# Test that an invalid URL raises a ValueError when attempting to match
def test_trutv_invalid_url_raises():
    url = "https://www.trutv.com/invalid/path"
    match = re.match(TruTVIE._VALID_URL, url)
    assert match is None, "Invalid URL should not match the regex"
    with pytest.raises(AttributeError):
        # Attempting to access groups on a None match should raise AttributeError
        match.groups()
