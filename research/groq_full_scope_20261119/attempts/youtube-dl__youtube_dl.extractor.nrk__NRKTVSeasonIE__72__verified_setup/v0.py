import re
import pytest
from youtube_dl.extractor.nrk import NRKTVSeasonIE

# Test that the regex correctly captures the components of a valid NRK TV/Radio season URL
def test_valid_url_parsing():
    url = "https://tv.nrk.no/serie/backstage/sesong/1"
    match = re.match(NRKTVSeasonIE._VALID_URL, url)
    assert match is not None, "URL should match the NRKTVSeasonIE pattern"
    assert match.group("domain") == "tv"
    assert match.group("serie_kind") == "serie"
    assert match.group("serie") == "backstage"
    assert match.group("id") == "1"
    assert match.group("id_2") is None

    # Test a URL without the explicit /sesong/ segment
    url2 = "https://tv.nrk.no/serie/lindmo/2016"
    match2 = re.match(NRKTVSeasonIE._VALID_URL, url2)
    assert match2 is not None
    assert match2.group("domain") == "tv"
    assert match2.group("serie_kind") == "serie"
    assert match2.group("serie") == "lindmo"
    assert match2.group("id") is None
    assert match2.group("id_2") == "2016"

# Test that suitable returns False for URLs that do not match the pattern
def test_suitable_false_for_non_matching():
    non_matching_url = "https://example.com/not-nrk/serie/abc"
    assert NRKTVSeasonIE.suitable(non_matching_url) is False

# Test that suitable returns True for a URL that matches the pattern
def test_suitable_true_for_matching():
    matching_url = "https://radio.nrk.no/serie/dickie-dick-dickens/sesong/1"
    assert NRKTVSeasonIE.suitable(matching_url) is True
