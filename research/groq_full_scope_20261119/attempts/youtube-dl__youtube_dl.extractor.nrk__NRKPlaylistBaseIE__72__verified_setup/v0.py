import re
import types
import pytest
from youtube_dl.extractor.nrk import NRKPlaylistBaseIE

# Helper dummy class to replace NRKIE in the module
class DummyNRKIE:
    @staticmethod
    def ie_key():
        return "DummyNRKIE"

# Test that the unimplemented _extract_description returns None
def test_extract_description_returns_none():
    class DummyIE(NRKPlaylistBaseIE):
        def _match_id(self, url):
            return "dummy_id"
        def _download_webpage(self, url, playlist_id):
            return ""
        def _extract_title(self, webpage):
            return "Dummy Title"
        def playlist_result(self, entries, playlist_id, title, description):
            return {
                "entries": entries,
                "id": playlist_id,
                "title": title,
                "description": description,
            }
    dummy = DummyIE()
    assert dummy._extract_description("") is None

# Test that _real_extract correctly builds the playlist result
def test_real_extract_builds_playlist(tmp_path):
    # Prepare a fake webpage containing two video IDs
    fake_webpage = """
        <div class="video" data-id="vid1"></div>
        <div class="video" data-id="vid2"></div>
    """
    # Patch the module's NRKIE reference
    original_nrkie = getattr(NRKPlaylistBaseIE, "__module__").__dict__.get("NRKIE", None)
    NRKPlaylistBaseIE.__module__ = types.SimpleNamespace(NRKIE=DummyNRKIE)

    class DummyIE(NRKPlaylistBaseIE):
        _ITEM_RE = r'data-id="([^"]+)"'
        def _match_id(self, url):
            return "playlist123"
        def _download_webpage(self, url, playlist_id):
            return fake_webpage
        def _extract_title(self, webpage):
            return "Test Playlist"
        def _extract_description(self, webpage):
            return "A test description."
        def playlist_result(self, entries, playlist_id, title, description):
            return {
                "entries": entries,
                "id": playlist_id,
                "title": title,
                "description": description,
            }

    dummy = DummyIE()
    result = dummy._real_extract("http://example.com/playlist/playlist123")

    # Verify playlist metadata
    assert result["id"] == "playlist123"
    assert result["title"] == "Test Playlist"
    assert result["description"] == "A test description."

    # Verify entries list
    assert isinstance(result["entries"], list)
    assert len(result["entries"]) == 2
    expected_urls = [
        "nrk:vid1",
        "nrk:vid2",
    ]
    for entry, expected_url in zip(result["entries"], expected_urls):
        assert entry["url"] == expected_url
        assert entry["ie_key"] == DummyNRKIE.ie_key()

    # Restore original NRKIE if it existed
    if original_nrkie is not None:
        NRKPlaylistBaseIE.__module__.NRKIE = original_nrkie
