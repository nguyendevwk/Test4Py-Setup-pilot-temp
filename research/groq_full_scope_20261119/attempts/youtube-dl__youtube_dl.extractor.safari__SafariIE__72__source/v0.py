import re
import pytest
from youtube_dl.extractor.safari import SafariIE

# Test 1: URL with course_id and part – should capture both groups correctly
def test_valid_course_url_groups():
    url = "https://www.safaribooksonline.com/library/view/hadoop-fundamentals-livelessons/9780133392838/part00.html"
    pattern = SafariIE._VALID_URL
    match = re.match(pattern, url)
    assert match is not None, "URL should match the pattern"
    assert match.group('course_id') == "9780133392838", "course_id group mismatch"
    assert match.group('part') == "part00", "part group mismatch"
    assert match.group('reference_id') is None, "reference_id should be None for course URLs"

# Test 2: URL with reference_id – should capture reference_id group correctly
def test_valid_reference_url_groups():
    url = "https://www.safaribooksonline.com/videos/python-programming-language/9780134217314/9780134217314-PYMC_13_00"
    pattern = SafariIE._VALID_URL
    match = re.match(pattern, url)
    assert match is not None, "URL should match the pattern"
    assert match.group('reference_id') == "9780134217314-PYMC_13_00", "reference_id group mismatch"
    assert match.group('course_id') is None, "course_id should be None for reference URLs"
    assert match.group('part') is None, "part should be None for reference URLs"

# Test 3: URL that should not match – ensure no match is returned
def test_invalid_url_no_match():
    url = "https://www.example.com/not-a-valid-url"
    pattern = SafariIE._VALID_URL
    match = re.match(pattern, url)
    assert match is None, "URL should not match the pattern"
