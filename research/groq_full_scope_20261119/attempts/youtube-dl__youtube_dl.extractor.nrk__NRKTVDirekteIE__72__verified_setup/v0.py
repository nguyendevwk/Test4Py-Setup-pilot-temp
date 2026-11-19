import re
import pytest
from youtube_dl.extractor.nrk import NRKTVDirekteIE

def test_valid_url_match():
    """The _VALID_URL regex should match known NRK TV and Radio Direkte URLs."""
    valid_urls = [
        "https://tv.nrk.no/direkte/nrk1",
        "http://tv.nrk.no/direkte/nrk2",
        "https://radio.nrk.no/direkte/p1_oslo_akershus",
        "http://radio.nrk.no/direkte/p2_bergen",
    ]
    pattern = re.compile(NRKTVDirekteIE._VALID_URL)
    for url in valid_urls:
        assert pattern.match(url), f"URL {url!r} did not match the pattern"

def test_invalid_url_no_match():
    """URLs that do not follow the NRK Direkte pattern should not match."""
    invalid_urls = [
        "https://tv.nrk.no/direkte/",          # missing id
        "https://tv.nrk.no/direkte/nrk1/extra", # trailing path
        "https://example.com/direkte/nrk1",
        "https://radio.nrk.no/direkte",        # missing id
        "https://tv.nrk.no/other/nrk1",
    ]
    pattern = re.compile(NRKTVDirekteIE._VALID_URL)
    for url in invalid_urls:
        assert not pattern.match(url), f"URL {url!r} incorrectly matched the pattern"

def test_test_cases_only_matching_flag():
    """Each test case in _TESTS should have the 'only_matching' flag set to True."""
    for test in NRKTVDirekteIE._TESTS:
        assert test.get("only_matching") is True, (
            f"Test case {test.get('url')} does not have 'only_matching' set to True"
        )
