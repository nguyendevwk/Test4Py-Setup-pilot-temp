import re
import pytest
from youtube_dl.extractor.nrk import NRKTVDirekteIE

def test_valid_url_match():
    """The _VALID_URL regex should match known NRK TV and Radio Direkte URLs."""
    valid_urls = [
        "https://tv.nrk.no/direkte/nrk1",
        "http://tv.nrk.no/direkte/nrk1",
        "https://radio.nrk.no/direkte/p1_oslo_akershus",
        "http://radio.nrk.no/direkte/p1_oslo_akershus",
    ]
    pattern = re.compile(NRKTVDirekteIE._VALID_URL)
    for url in valid_urls:
        match = pattern.match(url)
        assert match is not None, f"URL {url} should match the pattern"
        # The captured group 'id' should be the part after the last slash
        expected_id = url.split('/')[-1]
        assert match.group('id') == expected_id, f"Captured id {match.group('id')} does not match expected {expected_id}"

def test_invalid_url_no_match():
    """URLs that do not follow the NRK Direkte pattern should not match."""
    invalid_urls = [
        "https://tv.nrk.no/direkte/",
        "https://tv.nrk.no/direkte",
        "https://radio.nrk.no/direkte/",
        "https://radio.nrk.no/direkte",
        "https://tv.nrk.no/other/nrk1",
        "https://radio.nrk.no/other/p1_oslo_akershus",
        "https://example.com/direkte/nrk1",
    ]
    pattern = re.compile(NRKTVDirekteIE._VALID_URL)
    for url in invalid_urls:
        assert pattern.match(url) is None, f"URL {url} should not match the pattern"

def test_test_cases_only_matching_flag():
    """Each test case in _TESTS should have the 'only_matching' flag set to True."""
    for test in NRKTVDirekteIE._TESTS:
        assert test.get('only_matching') is True, (
            f"Test case {test} does not have 'only_matching' set to True"
        )
