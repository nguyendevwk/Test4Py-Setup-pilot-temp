import re
import pytest
from youtube_dl.extractor.tvplay import ViafreeIE

# Test 1: Verify that the regular expression correctly extracts country and path
def test_valid_url_parsing():
    url = "http://www.viafree.no/programmer/underholdning/det-beste-vorspielet/sesong-2/episode-1"
    match = re.match(ViafreeIE._VALID_URL, url)
    assert match is not None, "URL should match the _VALID_URL pattern"
    country, path = match.groups()
    assert country == "no", f"Expected country 'no', got {country}"
    assert path == "programmer/underholdning/det-beste-vorspielet/sesong-2/episode-1", \
        f"Unexpected path extraction: {path}"

# Test 2: Ensure that the extractor reports itself as suitable for a matching URL
def test_suitable_for_matching_url():
    url = "http://www.viafree.dk/programmer/reality/paradise-hotel/saeson-7/episode-5"
    # The TVPlayIE.suitable check is not available in this context, but ViafreeIE.suitable should
    # return True for a URL that matches its own pattern.
    assert ViafreeIE.suitable(url) is True, "ViafreeIE should be suitable for its own URLs"

# Test 3: Ensure that the extractor reports itself as not suitable for a non-matching URL
def test_not_suitable_for_non_matching_url():
    url = "https://example.com/not-a-viafree-url"
    assert ViafreeIE.suitable(url) is False, "ViafreeIE should not be suitable for unrelated URLs"
