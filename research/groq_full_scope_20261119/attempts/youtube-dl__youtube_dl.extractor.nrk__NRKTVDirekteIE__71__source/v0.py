import re
import pytest
from youtube_dl.extractor.nrk import NRKTVDirekteIE

def test_valid_url_matches_expected_pattern():
    """Ensure the regex matches the expected NRK TV and Radio Direkte URLs."""
    pattern = NRKTVDirekteIE._VALID_URL
    assert isinstance(pattern, str)
    regex = re.compile(pattern)
    # Valid TV URL
    assert regex.match('https://tv.nrk.no/direkte/nrk1')
    # Valid Radio URL
    assert regex.match('https://radio.nrk.no/direkte/p1_oslo_akershus')
    # Invalid URL (different domain)
    assert not regex.match('https://www.nrk.no/direkte/nrk1')
    # Invalid URL (missing path)
    assert not regex.match('https://tv.nrk.no/direkte/')

def test_test_cases_have_only_matching_flag():
    """Verify that all test cases in _TESTS are marked as only_matching."""
    tests = NRKTVDirekteIE._TESTS
    assert isinstance(tests, list)
    for test in tests:
        assert isinstance(test, dict)
        assert test.get('only_matching') is True, f"Test {test} missing only_matching flag"

def test_ie_description_is_correct():
    """Check that the IE_DESC attribute is set to the expected description."""
    assert NRKTVDirekteIE.IE_DESC == 'NRK TV Direkte and NRK Radio Direkte'
