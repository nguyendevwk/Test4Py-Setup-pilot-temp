import re
import pytest
from youtube_dl.extractor.itv import ITVBTCCIE
from youtube_dl.utils import smuggle_url

def test_valid_url_matches_expected_pattern():
    """The _VALID_URL regex should match a typical ITV BTCC URL and capture the ID."""
    url = "https://www.itv.com/btcc/races/btcc-2018-all-the-action-from-brands-hatch"
    match = re.match(ITVBTCCIE._VALID_URL, url)
    assert match is not None, "URL should match the regex"
    assert match.group("id") == "btcc-2018-all-the-action-from-brands-hatch"

def test_brightcove_url_template_formatting():
    """The BRIGHTCOVE_URL_TEMPLATE should correctly format a video ID into a URL."""
    video_id = "123456789"
    expected = "http://players.brightcove.net/1582188683001/HkiHLnNRx_default/index.html?videoId=123456789"
    assert ITVBTCCIE.BRIGHTCOVE_URL_TEMPLATE % video_id == expected

def test_smuggle_url_includes_expected_metadata(tmp_path):
    """smuggle_url should embed the provided metadata into the URL query string."""
    base_url = "http://example.com/video"
    metadata = {"geo_ip_blocks": ["1.2.3.0/24"], "referrer": "http://referrer.com"}
    smuggled = smuggle_url(base_url, metadata)
    # The smuggled URL should contain the original base URL and the metadata as a query string
    assert smuggled.startswith(base_url)
    # Extract the query part after the first '?' and parse it
    query = smuggled.split("?", 1)[1]
    # The query should contain the metadata keys
    assert "geo_ip_blocks" in query
    assert "referrer" in query
    # The metadata values should be URL-encoded
    assert "1.2.3.0%2F24" in query
    assert "http%3A%2F%2Freferrer.com" in query
