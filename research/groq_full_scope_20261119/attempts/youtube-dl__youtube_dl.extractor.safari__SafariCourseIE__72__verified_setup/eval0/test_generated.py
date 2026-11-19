import pytest
from youtube_dl.extractor.safari import SafariCourseIE
from youtube_dl.utils import ExtractorError

# Test that SafariCourseIE correctly identifies URLs that it should handle
def test_safari_course_ie_suitable():
    # URL that matches the pattern but is not handled by SafariIE or SafariApiIE
    url = "https://www.safaribooksonline.com/library/view/hadoop-fundamentals-livelessons/9780133392838/"
    assert SafariCourseIE.suitable(url) is True

    # URL that is handled by SafariIE (e.g., a book page)
    url_book = "https://www.safaribooksonline.com/api/v1/book/9781449396459/?override_format=json"
    assert SafariCourseIE.suitable(url_book) is False

    # URL that is handled by SafariApiIE (e.g., a video page)
    url_video = "https://www.safaribooksonline.com/videos/python-programming-language/9780134217314"
    assert SafariCourseIE.suitable(url_video) is False

# Test that _real_extract returns a playlist with the expected entries
def test_safari_course_ie_extract_success():
    # Create an instance of the extractor
    ie = SafariCourseIE()
    # Monkeypatch the downloader to return a controlled JSON response
    def fake_download_json(url, video_id, note):
        # The URL is not used in this test; we just return a minimal valid structure
        return {
            "title": "Test Course Title",
            "chapters": [
                "https://www.safaribooksonline.com/api/v1/chapter/1",
                "https://www.safaribooksonline.com/api/v1/chapter/2",
            ],
        }
    ie._download_json = fake_download_json

    # Use a URL that matches the extractor's pattern
    url = "https://www.safaribooksonline.com/library/view/test-course/1234567890/"
    result = ie.extract(url)

    # The result should be a playlist with two entries
    assert result['entries'] is not None
    assert len(result['entries']) == 2
    # Each entry should be a URL result pointing to SafariApiIE
    for entry in result['entries']:
        assert entry['ie_key'] == 'safari:api'
        assert entry['url'] in [
            "https://www.safaribooksonline.com/api/v1/chapter/1",
            "https://www.safaribooksonline.com/api/v1/chapter/2",
        ]
    # The playlist title should match the fake JSON title
    assert result['title'] == "Test Course Title"
    # The playlist ID should be extracted from the URL
    assert result['id'] == "1234567890"

# Test that an ExtractorError is raised when the JSON lacks chapters
def test_safari_course_ie_extract_no_chapters():
    ie = SafariCourseIE()
    def fake_download_json(url, video_id, note):
        # Return JSON without 'chapters' key to trigger the error
        return {"title": "Incomplete Course"}
    ie._download_json = fake_download_json

    url = "https://www.safaribooksonline.com/library/view/incomplete-course/9876543210/"
    with pytest.raises(ExtractorError) as excinfo:
        ie.extract(url)
    assert "No chapters found for course 9876543210" in str(excinfo.value)
