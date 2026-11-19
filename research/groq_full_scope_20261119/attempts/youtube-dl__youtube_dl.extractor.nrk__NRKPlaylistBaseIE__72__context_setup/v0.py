import re
import types
import importlib
import pytest

# Import the target module
module = importlib.import_module('youtube_dl.extractor.nrk')
NRKPlaylistBaseIE = module.NRKPlaylistBaseIE

# Helper dummy NRKIE class
class DummyNRKIE:
    @staticmethod
    def ie_key():
        return 'NRKIE'

# Test that the unimplemented _extract_description returns None
def test_extract_description_returns_none():
    class DummyIE(NRKPlaylistBaseIE):
        def _match_id(self, url):
            return 'dummy_id'
        def _download_webpage(self, url, playlist_id):
            return ''
        def _extract_title(self, webpage):
            return 'dummy title'
        def playlist_result(self, entries, playlist_id, title, description):
            return {
                'entries': entries,
                'id': playlist_id,
                'title': title,
                'description': description,
            }
    ie = DummyIE()
    result = ie._real_extract('http://example.com/dummy')
    assert result['description'] is None
    assert result['title'] == 'dummy title'

# Test that _real_extract correctly builds entries and calls playlist_result
def test_real_extract_builds_entries_and_calls_playlist_result(tmp_path):
    # Prepare a dummy webpage with two video ids
    webpage = '...<div data-video-id="vid1"></div>...<div data-video-id="vid2"></div>...'
    # Patch the module's regex to match the dummy ids
    module._ITEM_RE = r'data-video-id="([^"]+)"'
    # Patch NRKIE in the module
    module.NRKIE = DummyNRKIE
    class DummyIE(NRKPlaylistBaseIE):
        def _match_id(self, url):
            return 'playlist123'
        def _download_webpage(self, url, playlist_id):
            return webpage
        def _extract_title(self, webpage):
            return 'Test Playlist'
        def _extract_description(self, webpage):
            return 'A test playlist description.'
        def playlist_result(self, entries, playlist_id, title, description):
            # Return a dict for easy assertion
            return {
                'entries': entries,
                'id': playlist_id,
                'title': title,
                'description': description,
            }
    ie = DummyIE()
    result = ie._real_extract('http://example.com/playlist123')
    assert result['id'] == 'playlist123'
    assert result['title'] == 'Test Playlist'
    assert result['description'] == 'A test playlist description.'
    # Entries should be url_results with correct keys
    assert len(result['entries']) == 2
    for entry, vid in zip(result['entries'], ['vid1', 'vid2']):
        assert entry['url'] == f'nrk:{vid}'
        assert entry['ie_key'] == 'NRKIE'
