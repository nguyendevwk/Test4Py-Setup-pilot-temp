import re
import pytest
from youtube_dl.extractor.safari import SafariIE

# Test that the regular expression matches expected URLs and captures groups correctly
def test_valid_url_match_and_groups():
    url = "https://www.safaribooksonline.com/library/view/hadoop-fundamentals-livelessons/9780133392838/part00.html"
    m = re.match(SafariIE._VALID_URL, url)
    assert m is not None, "URL should match the pattern"
    assert m.group('course_id') == '9780133392838'
    assert m.group('part') == 'part00'
    assert m.group('reference_id') is None

# Test that URLs marked as only_matching in _TESTS indeed match the pattern but are not expected to be fully processed
def test_only_matching_urls():
    for test in SafariIE._TESTS:
        if test.get('only_matching'):
            url = test['url']
            m = re.match(SafariIE._VALID_URL, url)
            assert m is not None, f"URL {url} should match the pattern"
            # Ensure that the URL does not contain a reference_id group
            assert m.group('reference_id') is None, f"URL {url} should not have a reference_id group"

# Test that a URL containing a reference_id is parsed correctly
def test_reference_id_extraction():
    url = "https://www.safaribooksonline.com/videos/python-programming-language/9780134217314/9780134217314-PYMC_13_00"
    m = re.match(SafariIE._VALID_URL, url)
    assert m is not None, "URL should match the pattern"
    reference_id = m.group('reference_id')
    assert reference_id == "9780134217314-PYMC_13_00", "Reference ID should be extracted correctly"
    # Ensure that course_id and part groups are None for this URL
    assert m.group('course_id') is None
    assert m.group('part') is None
