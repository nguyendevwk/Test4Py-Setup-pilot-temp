import re
import pytest
from youtube_dl.extractor.nrk import NRKTVEpisodesIE


def test_valid_url_match():
    """The _VALID_URL regex should match a valid NRK TV episodes URL."""
    url = "https://tv.nrk.no/program/episodes/nytt-paa-nytt/69031"
    match = re.match(NRKTVEpisodesIE._VALID_URL, url)
    assert match is not None
    assert match.group("id") == "69031"


def test_extract_title():
    """_extract_title should return the title from a simple HTML snippet."""
    html = "<html><body><h1>Sample Episode Title</h1></body></html>"
    extractor = NRKTVEpisodesIE()
    title = extractor._extract_title(html)
    assert title == "Sample Episode Title"


def test_item_re_match():
    """_ITEM_RE should match an HTML element containing a data-episode attribute."""
    # Construct a minimal string that contains the expected data-episode attribute
    # The attribute value is a numeric ID; we use 12345 for testing.
    html = '<div data-episode="12345"></div>'
    # The pattern should match the entire attribute string
    pattern = re.compile(NRKTVEpisodesIE._ITEM_RE)
    match = pattern.search(html)
    assert match is not None
    # The matched string should include the attribute and its value
    assert 'data-episode="12345"' in match.group(0)
