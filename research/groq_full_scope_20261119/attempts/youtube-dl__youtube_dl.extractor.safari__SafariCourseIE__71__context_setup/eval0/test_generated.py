import re
import pytest
from youtube_dl.extractor.safari import SafariCourseIE, SafariIE, SafariApiIE
from youtube_dl.utils import ExtractorError


def test_safari_course_suitable_excludes_other_ie():
    """SafariCourseIE.suitable should return False for URLs that match SafariIE or SafariApiIE."""
    url = "https://www.safaribooksonline.com/library/view/hadoop-fundamentals-livelessons/9780133392838/part00.html"
    assert SafariIE.suitable(url) is True
    assert SafariApiIE.suitable(url) is False
    assert SafariCourseIE.suitable(url) is False


def test_safari_course_suitable_matches_course_url():
    """SafariCourseIE.suitable should return True for a course URL that does not match other IEs."""
    url = "https://www.safaribooksonline.com/library/view/hadoop-fundamentals-livelessons/9780133392838/"
    assert SafariCourseIE.suitable(url) is True
    assert SafariIE.suitable(url) is False
    assert SafariApiIE.suitable(url) is False


def test_safari_course_extract_raises_on_missing_chapters(monkeypatch):
    """_real_extract should raise ExtractorError when the JSON lacks 'chapters'."""
    ie = SafariCourseIE()
    # monkeypatch the download_json method to return a dict without 'chapters'
    def fake_download_json(url, video_id, note=None, errnote=None, headers=None, data=None, timeout=None, fatal=True):
        return {"title": "Fake Course"}  # no 'chapters' key
    monkeypatch.setattr(ie, "_download_json", fake_download_json)

    url = "https://www.safaribooksonline.com/library/view/fake-course/1234567890/"
    with pytest.raises(ExtractorError) as excinfo:
        ie._real_extract(url)
    assert "No chapters found for course 1234567890" in str(excinfo.value)
