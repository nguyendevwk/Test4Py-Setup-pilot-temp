import re
import pytest
from youtube_dl.extractor.safari import SafariApiIE

def test_valid_url_pattern_matches_expected_groups():
    """Ensure the regex captures course_id and part correctly."""
    url = "https://www.safaribooksonline.com/api/v1/book/9780133392838/chapter/part00.html"
    match = re.match(SafariApiIE._VALID_URL, url)
    assert match is not None, "URL should match the pattern"
    assert match.group('course_id') == "9780133392838"
    assert match.group('part') == "part00"

def test_test_cases_are_only_matching():
    """Verify that all test cases are marked as only_matching."""
    for test in SafariApiIE._TESTS:
        assert test.get('only_matching', False), (
            f"Test case {test.get('url')} should be only_matching"
        )

def test_ie_name_and_key():
    """Check that the IE name and key are as expected."""
    assert SafariApiIE.IE_NAME == "safari:api"
    assert SafariApiIE.ie_key() == "safari:api"
