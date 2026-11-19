import re
import pytest
from youtube_dl.extractor.nrk import NRKTVDirekteIE
from youtube_dl.utils import urljoin

def test_valid_url_matches_expected_patterns():
    """NRKTVDirekteIE should match both TV and radio direct URLs."""
    pattern = NRKTVDirekteIE._VALID_URL
    assert re.match(pattern, 'https://tv.nrk.no/direkte/nrk1')
    assert re.match(pattern, 'https://radio.nrk.no/direkte/p1_oslo_akershus')
    # URLs that do not follow the pattern should not match
    assert not re.match(pattern, 'https://tv.nrk.no/direkte/')
    assert not re.match(pattern, 'https://tv.nrk.no/direkte/nrk1/extra')
    assert not re.match(pattern, 'http://tv.nrk.no/direkte/nrk1')  # http not allowed

def test_test_cases_have_only_matching_flag():
    """Each test case in NRKTVDirekteIE._TESTS must have only_matching=True."""
    for test in NRKTVDirekteIE._TESTS:
        assert test.get('only_matching') is True, (
            f"Test case {test} does not have only_matching=True"
        )

def test_urljoin_works_with_base_and_path():
    """urljoin should correctly combine base URL and relative path."""
    base = 'https://tv.nrk.no/direkte/'
    path = 'nrk1'
    expected = 'https://tv.nrk.no/direkte/nrk1'
    assert urljoin(base, path) == expected
    # When path is absolute, it should override base
    absolute = 'https://radio.nrk.no/direkte/p1_oslo_akershus'
    assert urljoin(base, absolute) == absolute
