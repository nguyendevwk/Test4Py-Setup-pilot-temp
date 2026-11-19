import re
import pytest
from youtube_dl.extractor.nrk import NRKTVEpisodesIE

def test_extract_title():
    """Test that _extract_title correctly extracts the title from a simple HTML snippet."""
    extractor = NRKTVEpisodesIE()
    html = "<html><body><h1>Sample Episode Title</h1></body></html>"
    title = extractor._extract_title(html)
    assert title == "Sample Episode Title"

def test_valid_url_match():
    """Test that _VALID_URL matches the expected NRK TV episodes URL pattern."""
    valid_url = "https://tv.nrk.no/program/episodes/nytt-paa-nytt/69031"
    invalid_url = "https://tv.nrk.no/program/episodes/nytt-paa-nytt/notanumber"
    pattern = re.compile(NRKTVEpisodesIE._VALID_URL)
    assert pattern.match(valid_url) is not None
    assert pattern.match(invalid_url) is None

def test_item_re_matches_episode_id():
    """Test that _ITEM_RE contains the episode ID pattern and matches a sample data-episode attribute."""
    # Construct a sample string that would appear in the page
    sample = '<div data-episode="12345"></div>'
    # The _ITEM_RE should match the data-episode attribute with the episode ID
    pattern = re.compile(NRKTVEpisodesIE._ITEM_RE)
    match = pattern.search(sample)
    assert match is not None
    # The captured group should be the episode ID
    assert match.group(1) == "12345"
