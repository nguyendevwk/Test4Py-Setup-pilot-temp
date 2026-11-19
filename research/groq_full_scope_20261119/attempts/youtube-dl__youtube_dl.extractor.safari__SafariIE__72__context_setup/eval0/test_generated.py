import re
import pytest
from youtube_dl.extractor.safari import SafariIE

# Test 1: Validate that the regular expression correctly captures the
# course_id and part components for a typical Safari book URL.
def test_valid_url_course_and_part_extraction():
    url = (
        "https://www.safaribooksonline.com/library/view/"
        "hadoop-fundamentals-livelessons/9780133392838/part00.html"
    )
    match = re.match(SafariIE._VALID_URL, url)
    assert match is not None, "URL should match the pattern"
    assert match.group("course_id") == "9780133392838"
    assert match.group("part") == "part00"

# Test 2: Validate that the regular expression correctly captures the
# reference_id component for a Safari video URL.
def test_valid_url_reference_id_extraction():
    url = (
        "https://www.safaribooksonline.com/videos/python-programming-language/"
        "9780134217314/9780134217314-PYMC_13_00"
    )
    match = re.match(SafariIE._VALID_URL, url)
    assert match is not None, "URL should match the pattern"
    assert match.group("reference_id") == "9780134217314-PYMC_13_00"

# Test 3: Ensure that the default partner and uiconf IDs are set correctly
# and that they are used when constructing the query dictionary.
def test_default_partner_and_uiconf_ids():
    ie = SafariIE()
    # The _real_extract method requires a network call; instead we test
    # the constants directly.
    assert ie._PARTNER_ID == "1926081", "Default partner ID should match expected value"
    assert ie._UICONF_ID == "29375172", "Default uiconf ID should match expected value"
