import pytest
from youtube_dl.extractor.nrk import NRKPlaylistBaseIE

class DummyIE(NRKPlaylistBaseIE):
    """A minimal stub that satisfies the abstract methods of NRKPlaylistBaseIE."""
    def _match_id(self, url):
        return "dummy_id"

    def _download_webpage(self, url, video_id):
        return "<html></html>"

    _ITEM_RE = r"video_id=(\w+)"
    def _extract_title(self, webpage):
        return "Dummy Title"

    def _extract_description(self, webpage):
        return "Dummy Description"

def test_extract_description_returns_none_for_base_class():
    """The base class implementation of _extract_description should return None."""
    base_ie = NRKPlaylistBaseIE()
    assert base_ie._extract_description("<html>content</html>") is None
    assert base_ie._extract_description("") is None
    assert base_ie._extract_description(None) is None

def test_extract_description_can_be_overridden_in_subclass():
    """A subclass can override _extract_description to provide custom logic."""
    dummy_ie = DummyIE()
    assert dummy_ie._extract_description("<html>content</html>") == "Dummy Description"

def test_real_extract_uses_overridden_methods_and_returns_playlist_dict(tmp_path):
    """_real_extract should assemble a playlist dict using overridden methods."""
    dummy_ie = DummyIE()
    # Create a temporary file to act as a dummy playlist URL
    playlist_file = tmp_path / "playlist.html"
    playlist_file.write_text('<html><body>video_id=abc123</body></html>')
    # Use the file URL as the input
    url = f"file://{playlist_file}"
    result = dummy_ie._real_extract(url)
    # Verify the structure of the returned playlist
    assert isinstance(result, dict)
    assert result["entries"] == ["nrk:abc123"]
    assert result["id"] == "dummy_id"
    assert result["title"] == "Dummy Title"
    assert result["description"] == "Dummy Description"
