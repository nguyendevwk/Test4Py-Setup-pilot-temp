import re
import pytest
from youtube_dl.extractor.safari import SafariCourseIE


def test_suitable_matches_course_url():
    """SafariCourseIE should recognize a valid course URL."""
    url = "https://www.safaribooksonline.com/library/view/hadoop-fundamentals-livelessons/9780133392838/"
    assert SafariCourseIE.suitable(url) is True
    # The URL should not be considered suitable for SafariIE or SafariApiIE
    from youtube_dl.extractor.safari import SafariIE, SafariApiIE
    assert SafariIE.suitable(url) is False
    assert SafariApiIE.suitable(url) is False


def test_match_id_extraction():
    """The extractor should correctly extract the course id from the URL."""
    url = "https://www.safaribooksonline.com/library/view/hadoop-fundamentals-livelessons/9780133392838/"
    extractor = SafariCourseIE()
    # _match_id is a protected method; we can call it directly for testing
    course_id = extractor._match_id(url)
    assert course_id == "9780133392838"
    # Ensure that the extracted id matches the regex group
    pattern = re.compile(SafariCourseIE._VALID_URL)
    match = pattern.search(url)
    assert match is not None
    assert match.group("id") == course_id


def test_suitable_false_for_non_course_urls():
    """SafariCourseIE should not match URLs that belong to other extractors."""
    # A URL that matches SafariIE but not SafariCourseIE
    url_video = "https://www.safaribooksonline.com/library/view/hadoop-fundamentals-livelessons/9780133392838/part00.html"
    assert SafariCourseIE.suitable(url_video) is False
    # A URL that matches SafariApiIE but not SafariCourseIE
    url_api = "https://www.safaribooksonline.com/api/v1/book/9780133392838/chapter/part00.html"
    assert SafariCourseIE.suitable(url_api) is False
    # A URL that matches the generic pattern but is not a course view
    url_other = "https://techbus.safaribooksonline.com/9780134426365"
    assert SafariCourseIE.suitable(url_other) is False
