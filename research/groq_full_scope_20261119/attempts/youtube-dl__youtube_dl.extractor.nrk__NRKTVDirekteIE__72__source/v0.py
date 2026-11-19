import re
import pytest
from youtube_dl.extractor.nrk import NRKTVDirekteIE

# Test 1: Verify that the regex matches valid NRK TV and Radio Direkte URLs
def test_valid_url_matching():
    valid_urls = [
        'https://tv.nrk.no/direkte/nrk1',
        'http://tv.nrk.no/direkte/nrk1',
        'https://radio.nrk.no/direkte/p1_oslo_akershus',
        'http://radio.nrk.no/direkte/p1_oslo_akershus',
    ]
    pattern = re.compile(NRKTVDirekteIE._VALID_URL)
    for url in valid_urls:
        match = pattern.match(url)
        assert match is not None, f"URL {url} should match the pattern"
        assert 'id' in match.groupdict(), f"URL {url} should capture an 'id' group"
        assert match.group('id'), f"URL {url} should have a non-empty id"

# Test 2: Verify that the regex does not match invalid URLs
def test_invalid_url_matching():
    invalid_urls = [
        'https://tv.nrk.no/direkte/',          # missing id
        'https://tv.nrk.no/direkte',           # missing trailing slash
        'https://tv.nrk.no/direkte/nrk1/extra',# extra path segment
        'https://radio.nrk.no/direkte/',       # missing id
        'https://radio.nrk.no/direkte',        # missing trailing slash
        'https://radio.nrk.no/direkte/p1_oslo_akershus/extra',
        'https://example.com/direkte/nrk1',
        'ftp://tv.nrk.no/direkte/nrk1',
    ]
    pattern = re.compile(NRKTVDirekteIE._VALID_URL)
    for url in invalid_urls:
        assert pattern.match(url) is None, f"URL {url} should NOT match the pattern"

# Test 3: Verify that the _TESTS list contains only matching tests
def test_tests_only_matching():
    for test in NRKTVDirekteIE._TESTS:
        assert test.get('only_matching') is True, (
            f"Test entry {test} should have 'only_matching' set to True"
        )
        assert 'url' in test, f"Test entry {test} must contain a 'url' key"
        # Ensure the URL matches the regex
        assert re.match(NRKTVDirekteIE._VALID_URL, test['url']), (
            f"Test URL {test['url']} does not match the regex"
        )
