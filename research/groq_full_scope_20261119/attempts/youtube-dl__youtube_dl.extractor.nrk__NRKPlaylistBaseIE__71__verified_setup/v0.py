import re
import pytest
from youtube_dl.extractor.nrk import NRKPlaylistBaseIE

# Test that the default implementation of _extract_description returns None
def test_extract_description_default():
    ie = NRKPlaylistBaseIE()
    assert ie._extract_description("<html></html>") is None

# Test that _real_extract can be executed when all required helpers are stubbed
def test_real_extract_with_stubs(tmp_path):
    ie = NRKPlaylistBaseIE()

    # Stub the helper methods and attributes
    ie._match_id = lambda url: "12345"
    ie._download_webpage = lambda url, playlist_id: (
        f'<div class="video" data-id="vid1"></div>'
        f'<div class="video" data-id="vid2"></div>'
    )
    ie._ITEM_RE = r'data-id="([^"]+)"'
    ie._extract_title = lambda webpage: "Test Playlist"
    ie._extract_description = lambda webpage: "A description"

    # The IE key for NRKIE is not needed for the test; we just check the structure
    result = ie._real_extract("https://example.com/playlist/12345")

    # Verify that the result is a playlist dict with expected fields
    assert result["entries"] == [
        {"url": "nrk:vid1", "ie_key": "NRKIE"},
        {"url": "nrk:vid2", "ie_key": "NRKIE"},
    ]
    assert result["id"] == "12345"
    assert result["title"] == "Test Playlist"
    assert result["description"] == "A description"

# Test that _real_extract raises an error when the URL does not match the expected pattern
def test_real_extract_invalid_url():
    ie = NRKPlaylistBaseIE()
    # Provide a URL that does not match the expected pattern; _match_id will raise
    with pytest.raises(Exception):
        ie._real_extract("https://invalid-url.com/not-a-playlist")
