import re
import pytest
from youtube_dl.extractor.safari import SafariCourseIE, SafariIE, SafariApiIE


def test_valid_url_matching():
    """Ensure _VALID_URL matches known Safari course URLs."""
    valid_urls = [
        'https://www.safaribooksonline.com/library/view/hadoop-fundamentals-livelessons/9780133392838/',
        'https://www.safaribooksonline.com/api/v1/book/9781449396459/?override_format=json',
        'http://techbus.safaribooksonline.com/9780134426365',
        'https://www.safaribooksonline.com/videos/python-programming-language/9780134217314',
        'https://learning.oreilly.com/videos/hadoop-fundamentals-livelessons/9780133392838',
        'https://www.oreilly.com/library/view/hadoop-fundamentals-livelessons/9780133392838/',
    ]
    pattern = re.compile(SafariCourseIE._VALID_URL, re.VERBOSE)
    for url in valid_urls:
        assert pattern.search(url), f"URL should match pattern: {url}"


def test_invalid_url_rejection():
    """Ensure _VALID_URL rejects URLs that are not Safari course URLs."""
    invalid_urls = [
        'https://www.example.com/library/view/1234567890',
        'https://www.safaribooksonline.com/library/view/invalid/1234567890',
        'https://www.safaribooksonline.com/other/1234567890',
        'https://www.safaribooksonline.com/library/view/1234567890',
        'https://www.safaribooksonline.com/api/v1/book/1234567890',
        'https://www.safaribooksonline.com/api/v1/book/1234567890?foo=bar',
    ]
    pattern = re.compile(SafariCourseIE._VALID_URL, re.VERBOSE)
    for url in invalid_urls:
        assert not pattern.search(url), f"URL should not match pattern: {url}"


def test_suitable_logic_excludes_other_ie():
    """SafariCourseIE.suitable should return False when SafariIE or SafariApiIE are suitable."""
    # URLs that match SafariIE or SafariApiIE patterns
    safari_ie_url = 'https://www.safaribooksonline.com/library/view/1234567890'
    safari_api_ie_url = 'https://www.safaribooksonline.com/api/v1/book/1234567890'
    # URLs that match SafariCourseIE but not the other IEs
    course_url = 'https://www.safaribooksonline.com/library/view/1234567890/1234567890/'

    # SafariIE and SafariApiIE should report suitable for their URLs
    assert SafariIE.suitable(safari_ie_url), "SafariIE should be suitable for its URL"
    assert SafariApiIE.suitable(safari_api_ie_url), "SafariApiIE should be suitable for its URL"

    # SafariCourseIE should not be suitable for URLs that match the other IEs
    assert not SafariCourseIE.suitable(safari_ie_url), "SafariCourseIE should not be suitable for SafariIE URL"
    assert not SafariCourseIE.suitable(safari_api_ie_url), "SafariCourseIE should not be suitable for SafariApiIE URL"

    # SafariCourseIE should be suitable for its own URL
    assert SafariCourseIE.suitable(course_url), "SafariCourseIE should be suitable for its URL"
