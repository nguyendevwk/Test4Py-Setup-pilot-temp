import re
import pytest
from youtube_dl.extractor.tvplay import ViafreeIE

# Test 1: Validate that the extractor reports itself as suitable for a valid viafree URL
def test_viafree_suitable_valid_url():
    url = "https://www.viafree.no/programmer/underholdning/det-beste-vorspielet/sesong-2/episode-1"
    assert ViafreeIE.suitable(url) is True

# Test 2: Validate that the extractor reports itself as not suitable for a non‑viafree URL
def test_viafree_suitable_invalid_url():
    url = "https://www.example.com/some/path"
    assert ViafreeIE.suitable(url) is False

# Test 3: Validate that the regular expression correctly captures the country and path components
def test_viafree_valid_url_regex_groups():
    url = "http://www.viafree.se/program/reality/sommaren-med-youtube-stjarnorna/sasong-1/avsnitt-1"
    match = re.match(ViafreeIE._VALID_URL, url)
    assert match is not None
    country, path = match.groups()
    assert country in {"dk", "no", "se"}
    # The path should start with 'program' or 'programmer' and contain at least one slash
    assert path.startswith(("program", "programmer"))
    assert "/" in path
