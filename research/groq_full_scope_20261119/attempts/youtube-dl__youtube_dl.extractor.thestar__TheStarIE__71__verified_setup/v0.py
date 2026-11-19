import pytest
from youtube_dl.extractor.thestar import TheStarIE
from youtube_dl.utils import ExtractorError

# Helper to create an instance of the extractor with a dummy downloader
@pytest.fixture
def extractor():
    return TheStarIE()

def test_normal_extraction(monkeypatch, extractor):
    # Simulate a webpage containing a brightcove id
    fake_webpage = '''
        <script>
            var mainartBrightcoveVideoId = "1234567890";
        </script>
    '''
    # Patch the download method to return our fake webpage
    monkeypatch.setattr(extractor, "_download_webpage", lambda url, display_id: fake_webpage)
    # Call the extractor on a valid URL
    result = extractor._real_extract("http://www.thestar.com/some/path/1234567890.html")
    # Verify that the result is a Brightcove URL with the correct id
    expected_url = extractor.BRIGHTCOVE_URL_TEMPLATE % "1234567890"
    assert result.url == expected_url
    assert result.info_dict['id'] == "1234567890"
    assert result.info_dict['ie_key'] == "BrightcoveNew"

def test_missing_brightcove_id(monkeypatch, extractor):
    # Simulate a webpage that does not contain the brightcove id
    fake_webpage = "<html><body>No video id here</body></html>"
    monkeypatch.setattr(extractor, "_download_webpage", lambda url, display_id: fake_webpage)
    # Expect an ExtractorError when the regex fails to find an id
    with pytest.raises(ExtractorError) as excinfo:
        extractor._real_extract("http://www.thestar.com/some/path/1234567890.html")
    assert "brightcove id" in str(excinfo.value)

def test_invalid_url_pattern(extractor):
    # URL that does not match the extractor's VALID_URL pattern
    invalid_url = "http://www.example.com/not-a-thestar-url.html"
    # The extractor should raise ExtractorError when attempting to match the id
    with pytest.raises(ExtractorError) as excinfo:
        extractor._real_extract(invalid_url)
    assert "match" in str(excinfo.value)
