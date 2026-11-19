import pytest
from youtube_dl.extractor.safari import SafariCourseIE
from youtube_dl.utils import ExtractorError

# Test 1: Verify that SafariCourseIE.suitable correctly identifies a valid course URL
def test_safari_course_ie_suitable_valid_url():
    url = "https://www.safaribooksonline.com/library/view/hadoop-fundamentals-livelessons/9780133392838/"
    assert SafariCourseIE.suitable(url) is True

# Test 2: Verify that SafariCourseIE.suitable returns False for a URL that matches SafariIE or SafariApiIE patterns
def test_safari_course_ie_suitable_conflict_url():
    # This URL matches the SafariApiIE pattern (api/v1/book)
    url = "https://www.safaribooksonline.com/api/v1/book/9781449396459/?override_format=json"
    # SafariCourseIE should not consider this suitable because SafariApiIE is suitable
    assert SafariCourseIE.suitable(url) is False

# Test 3: Verify that _real_extract raises ExtractorError when the JSON lacks 'chapters'
def test_safari_course_ie_real_extract_missing_chapters(tmp_path):
    # Create a dummy course URL that matches the regex
    url = "https://www.safaribooksonline.com/library/view/dummy-course/1234567890123/"
    # Instantiate the extractor
    ie = SafariCourseIE()
    # Monkeypatch _download_json to return a dict without 'chapters'
    def fake_download_json(url, video_id, note):
        return {"title": "Dummy Course"}  # No 'chapters' key
    ie._download_json = fake_download_json
    # Expect ExtractorError when calling _real_extract
    with pytest.raises(ExtractorError) as excinfo:
        ie._real_extract(url)
    assert "No chapters found for course 1234567890123" in str(excinfo.value)
