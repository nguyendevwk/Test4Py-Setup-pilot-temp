import re
import pytest
from youtube_dl.extractor.nrk import NRKTVEpisodesIE, NRKPlaylistBaseIE, NRKIE
from youtube_dl.utils import ExtractorError

class DummyNRKTVEpisodesIE(NRKTVEpisodesIE):
    """A subclass that overrides network access for testing."""
    def __init__(self, webpage):
        super().__init__()
        self._webpage = webpage

    def _download_webpage(self, url, playlist_id, note=None, errnote=None, timeout=10, data=None, headers=None, query=None, disposition=False, raw=False, err=None):
        return self._webpage

    def _extract_description(self, webpage):
        return None

def test_extract_title_success():
    """_extract_title should return the text inside the first <h1> tag."""
    html = "<html><body><h1>Sample Title</h1><p>Other content</p></body></html>"
    ie = DummyNRKTVEpisodesIE(html)
    assert ie._extract_title(html) == "Sample Title"

def test_extract_title_missing():
    """_extract_title should return None when no <h1> tag is present."""
    html = "<html><body><p>No title here</p></body></html>"
    ie = DummyNRKTVEpisodesIE(html)
    assert ie._extract_title(html) is None

def test_real_extract_playlist_entries(tmp_path):
    """_real_extract should return a playlist with the correct number of entries."""
    # Construct a fake webpage with four data-episode attributes
    episode_ids = ["123", "456", "789", "101112"]
    items = "".join(f'<div data-episode="{eid}"></div>' for eid in episode_ids)
    html = f"<html><body>{items}<h1>Test Playlist</h1></body></html>"
    url = "https://tv.nrk.no/program/episodes/test/99999"
    ie = DummyNRKTVEpisodesIE(html)
    result = ie._real_extract(url)

    # Verify the playlist structure
    assert result['entries'] == [ie.url_result(f"nrk:{eid}", NRKIE.ie_key()) for eid in episode_ids]
    assert result['id'] == "99999"
    assert result['title'] == "Test Playlist"
    assert result['description'] is None
    assert len(result['entries']) == 4
