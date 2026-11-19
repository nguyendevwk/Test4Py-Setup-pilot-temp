import pytest
from youtube_dl.extractor.safari import SafariCourseIE
from youtube_dl.utils import ExtractorError

# Test 1: URL suitability
def test_safari_course_suitable():
    # URL that should match SafariCourseIE but not SafariIE or SafariApiIE
    url = "https://www.safaribooksonline.com/library/view/hadoop-fundamentals-livelessons/9780133392838/"
    assert SafariCourseIE.suitable(url) is True
    # URL that matches SafariIE (e.g., a book view) should not be suitable
    book_url = "https://www.safaribooksonline.com/library/view/learning-python/9780134685991/"
    assert SafariCourseIE.suitable(book_url) is False

# Test 2: Successful extraction returns playlist with correct metadata
def test_safari_course_real_extract_success(monkeypatch):
    # Prepare a fake JSON response with chapters
    fake_json = {
        "title": "Fake Course Title",
        "chapters": ["https://example.com/chapter1", "https://example.com/chapter2"]
    }
    # Monkeypatch the download method to return our fake JSON
    monkeypatch.setattr(
        SafariCourseIE,
        "_download_json",
        lambda self, url, video_id, note=None: fake_json
    )
    extractor = SafariCourseIE()
    result = extractor._real_extract("https://www.safaribooksonline.com/library/view/fake/1234567890/")
    # Verify playlist structure
    assert result['entries'] == [
        extractor.url_result("https://example.com/chapter1", SafariCourseIE.ie_key()),
        extractor.url_result("https://example.com/chapter2", SafariCourseIE.ie_key())
    ]
    assert result['id'] == "1234567890"
    assert result['title'] == "Fake Course Title"

# Test 3: Extraction fails when chapters key is missing
def test_safari_course_real_extract_no_chapters(monkeypatch):
    # Fake JSON without 'chapters'
    fake_json = {"title": "No Chapters Course"}
    monkeypatch.setattr(
        SafariCourseIE,
        "_download_json",
        lambda self, url, video_id, note=None: fake_json
    )
    extractor = SafariCourseIE()
    with pytest.raises(ExtractorError) as excinfo:
        extractor._real_extract("https://www.safaribooksonline.com/library/view/noc/0987654321/")
    assert "No chapters found for course 0987654321" in str(excinfo.value)
