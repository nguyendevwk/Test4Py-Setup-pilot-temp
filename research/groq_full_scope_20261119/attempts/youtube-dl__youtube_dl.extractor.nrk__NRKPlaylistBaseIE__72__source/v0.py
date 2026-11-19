import re
import pytest
from youtube_dl.extractor.nrk import NRKPlaylistBaseIE, NRKIE
from youtube_dl.utils import ExtractorError

class DummyNRKIE(NRKIE):
    @staticmethod
    def ie_key():
        return 'DummyNRKIE'

@pytest.fixture
def dummy_ie(monkeypatch):
    # Patch NRKIE.ie_key to avoid dependency on the real NRKIE implementation
    monkeypatch.setattr(NRKIE, 'ie_key', DummyNRKIE.ie_key)
    return DummyNRKIE()

class TestNRKPlaylistBaseIE:
    def test_normal_extraction(self, dummy_ie):
        # Prepare a dummy webpage containing two video IDs
        dummy_webpage = """
            <div class="video" data-id="vid123"></div>
            <div class="video" data-id="vid456"></div>
        """
        # Override methods to provide controlled data
        dummy_ie._match_id = lambda url: 'pl123'
        dummy_ie._download_webpage = lambda url, playlist_id: dummy_webpage
        dummy_ie._ITEM_RE = r'data-id="([^"]+)"'
        dummy_ie._extract_title = lambda webpage: 'Test Playlist'
        dummy_ie._extract_description = lambda webpage: 'A test playlist description.'

        result = dummy_ie._real_extract('http://example.com/playlist/pl123')
        assert result['entries'] == [
            dummy_ie.url_result('nrk:vid123', 'DummyNRKIE'),
            dummy_ie.url_result('nrk:vid456', 'DummyNRKIE')
        ]
        assert result['id'] == 'pl123'
        assert result['title'] == 'Test Playlist'
        assert result['description'] == 'A test playlist description.'

    def test_boundary_no_videos(self, dummy_ie):
        # Webpage with no matching video IDs
        dummy_webpage = '<div>No videos here</div>'
        dummy_ie._match_id = lambda url: 'pl_empty'
        dummy_ie._download_webpage = lambda url, playlist_id: dummy_webpage
        dummy_ie._ITEM_RE = r'data-id="([^"]+)"'
        dummy_ie._extract_title = lambda webpage: 'Empty Playlist'
        dummy_ie._extract_description = lambda webpage: None

        result = dummy_ie._real_extract('http://example.com/playlist/pl_empty')
        assert result['entries'] == []
        assert result['id'] == 'pl_empty'
        assert result['title'] == 'Empty Playlist'
        assert result['description'] is None

    def test_error_invalid_id(self, dummy_ie):
        # Simulate a failure in _match_id
        dummy_ie._match_id = lambda url: (_ for _ in ()).throw(ExtractorError('Invalid ID'))
        dummy_ie._download_webpage = lambda url, playlist_id: ''
        dummy_ie._ITEM_RE = r'data-id="([^"]+)"'

        with pytest.raises(ExtractorError, match='Invalid ID'):
            dummy_ie._real_extract('http://example.com/playlist/invalid')
