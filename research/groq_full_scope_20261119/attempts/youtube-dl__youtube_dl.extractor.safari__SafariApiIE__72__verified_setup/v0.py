import re
import pytest
from youtube_dl.extractor.safari import SafariApiIE

def test_valid_url_matching():
    """SafariApiIE should match known Safari API URLs."""
    valid_urls = [
        'https://www.safaribooksonline.com/api/v1/book/9780133392838/chapter/part00.html',
        'https://www.safaribooksonline.com/api/v1/book/9780134664057/chapter/RHCE_Introduction.html',
        'https://learning.oreilly.com/api/v1/book/1234567890/chapter/part01.html',
    ]
    pattern = re.compile(SafariApiIE._VALID_URL)
    for url in valid_urls:
        assert pattern.match(url), f"URL should match: {url}"

def test_invalid_url_not_matching():
    """SafariApiIE should not match URLs that do not follow the expected pattern."""
    invalid_urls = [
        'https://www.safaribooksonline.com/api/v1/book/9780133392838/chapter/part00.htm',  # wrong extension
        'https://www.safaribooksonline.com/api/v1/book/9780133392838/chapter/',  # missing part
        'https://www.safaribooksonline.com/api/v1/book//chapter/part00.html',  # missing course_id
        'https://www.example.com/api/v1/book/9780133392838/chapter/part00.html',  # wrong domain
    ]
    pattern = re.compile(SafariApiIE._VALID_URL)
    for url in invalid_urls:
        assert not pattern.match(url), f"URL should not match: {url}"

def test_ie_key():
    """The IE key should be correctly defined."""
    assert SafariApiIE.ie_key() == 'safari:api'
