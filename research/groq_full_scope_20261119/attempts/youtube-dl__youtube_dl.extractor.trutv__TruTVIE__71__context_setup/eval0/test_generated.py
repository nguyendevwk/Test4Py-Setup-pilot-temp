import re
import pytest
from youtube_dl.extractor.trutv import TruTVIE

def test_valid_url_parsing():
    """Verify that the regex captures the correct groups for a typical TruTV URL."""
    url = "https://www.trutv.com/shows/the-carbonaro-effect/videos/sunlight-activated-flower.html"
    match = re.match(TruTVIE._VALID_URL, url)
    assert match is not None, "URL should match the _VALID_URL pattern"
    series_slug, clip_slug, video_id = match.groups()
    assert series_slug == "the-carbonaro-effect", f"Unexpected series_slug: {series_slug}"
    assert clip_slug == "sunlight-activated-flower", f"Unexpected clip_slug: {clip_slug}"
    assert video_id is None, f"video_id should be None for a clip URL, got {video_id}"

def test_test_dict_structure():
    """Ensure the _TEST dictionary contains the expected keys and values."""
    test = TruTVIE._TEST
    assert isinstance(test, dict), "_TEST should be a dictionary"
    assert "url" in test, "Missing 'url' key in _TEST"
    assert "info_dict" in test, "Missing 'info_dict' key in _TEST"
    assert "params" in test, "Missing 'params' key in _TEST"
    info = test["info_dict"]
    expected_keys = {"id", "ext", "title", "description"}
    assert expected_keys.issubset(info.keys()), f"_TEST info_dict missing keys: {expected_keys - set(info.keys())}"
    assert test["url"] == "https://www.trutv.com/shows/the-carbonaro-effect/videos/sunlight-activated-flower.html"
    assert test["params"]["skip_download"] is True, "Expected skip_download to be True"

def test_invalid_url_raises():
    """Calling _real_extract with an invalid URL should raise an AttributeError due to no match."""
    ie = TruTVIE()
    invalid_url = "https://www.trutv.com/invalid/path"
    with pytest.raises(AttributeError):
        ie._real_extract(invalid_url)
