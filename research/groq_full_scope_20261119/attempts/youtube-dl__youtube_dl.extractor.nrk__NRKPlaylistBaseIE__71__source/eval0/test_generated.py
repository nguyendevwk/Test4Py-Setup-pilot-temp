import pytest
from youtube_dl.extractor.nrk import NRKPlaylistBaseIE
from youtube_dl.utils import ExtractorError

class DummyNRKIE(NRKPlaylistBaseIE):
    # Provide minimal implementation for abstract methods
    _ITEM_RE = r'\d+'
    def _extract_title(self, webpage):
        return "dummy title"
    def _download_webpage(self, url, playlist_id):
        # Return a simple webpage containing two video ids
        return "video ids: 123 456"
    def _real_extract(self, url):
        # Use the base implementation
        return super()._real_extract(url)

def test_extract_description_returns_none():
    """_extract_description should return None for any input."""
    ie = DummyNRKIE()
    assert ie._extract_description("") is None
    assert ie._extract_description("some text") is None

def test_real_extract_raises_on_invalid_url():
    """_real_extract should raise ExtractorError when URL does not match pattern."""
    ie = DummyNRKIE()
    with pytest.raises(ExtractorError):
        ie._real_extract("https://example.com/invalid")

def test_real_extract_returns_playlist_result():
    """_real_extract should return a playlist result with correct entries."""
    ie = DummyNRKIE()
    result = ie._real_extract("https://nrk.no/playlist/123")
    assert result["entries"] == [
        ie.url_result("nrk:123", ie.ie_key()),
        ie.url_result("nrk:456", ie.ie_key())
    ]
    assert result["id"] == "123"
    assert result["title"] == "dummy title"
    assert result["description"] is None
