import re
import pytest
from youtube_dl.extractor.fourtube import FuxIE

def test_valid_url_matches_expected_groups():
    """The _VALID_URL regex should correctly capture kind, id, and display_id."""
    url = "https://www.fux.com/video/195359/awesome-fucking-kitchen-ends-cum-swallow"
    match = re.match(FuxIE._VALID_URL, url)
    assert match is not None, "URL should match the regex"
    assert match.group("kind") == "www", "The kind group should capture 'www'"
    assert match.group("id") == "195359", "The id group should capture the numeric ID"
    assert match.group("display_id") == "awesome-fucking-kitchen-ends-cum-swallow", \
        "The display_id group should capture the slug"

def test_url_template_uses_id_and_returns_expected_url():
    """The _URL_TEMPLATE should format the ID into the correct URL."""
    video_id = "123456"
    expected = "https://www.fux.com/video/123456/video"
    formatted = FuxIE._URL_TEMPLATE % video_id
    assert formatted == expected, "URL template formatting failed"

def test_tkn_host_is_correct_and_consistent():
    """The _TKN_HOST constant should be a valid hostname string."""
    assert isinstance(FuxIE._TKN_HOST, str), "_TKN_HOST should be a string"
    assert FuxIE._TKN_HOST == "token.fux.com", "_TKN_HOST should match the expected hostname"
