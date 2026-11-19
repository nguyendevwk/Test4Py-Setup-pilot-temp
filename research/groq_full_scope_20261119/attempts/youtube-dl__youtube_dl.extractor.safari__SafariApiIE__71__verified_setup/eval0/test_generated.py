import pytest
from youtube_dl.extractor.safari import SafariApiIE
from youtube_dl.utils import ExtractorError

class DummyDownloader:
    """A minimal downloader that records the last URL requested."""
    def __init__(self):
        self.last_url = None
    def url_result(self, url, ie_key):
        return {'url': url, 'ie_key': ie_key}

def test_safari_api_ie_normal(monkeypatch):
    """Test normal extraction of a Safari API part."""
    # Prepare a dummy downloader and monkeypatch the download_json method
    dummy = DummyDownloader()
    def fake_download_json(url, name, note):
        # Record the URL for later inspection
        dummy.last_url = url
        # Return a JSON dict with a web_url field
        return {'web_url': 'https://example.com/content.html'}
    monkeypatch.setattr(SafariApiIE, '_download_json', fake_download_json, raising=False)

    ie = SafariApiIE()
    # Use a valid URL from the tests
    url = 'https://www.safaribooksonline.com/api/v1/book/9780133392838/chapter/part00.html'
    result = ie._real_extract(url)

    # Verify that the downloader was called with the correct URL
    assert dummy.last_url == url
    # Verify that the returned result contains the expected web_url and IE key
    assert result['url'] == 'https://example.com/content.html'
    assert result['ie_key'] == 'safari'

def test_safari_api_ie_download_error(monkeypatch):
    """Test that an error during JSON download propagates as ExtractorError."""
    def fake_download_json(url, name, note):
        raise ExtractorError('download failed')
    monkeypatch.setattr(SafariApiIE, '_download_json', fake_download_json, raising=False)

    ie = SafariApiIE()
    url = 'https://www.safaribooksonline.com/api/v1/book/9780133392838/chapter/part00.html'
    with pytest.raises(ExtractorError, match='download failed'):
        ie._real_extract(url)

def test_safari_api_ie_invalid_url():
    """Test that an invalid URL raises an AttributeError due to regex mismatch."""
    ie = SafariApiIE()
    invalid_url = 'https://invalid.com/api/v1/book/123/chapter/part00.html'
    with pytest.raises(AttributeError):
        ie._real_extract(invalid_url)
