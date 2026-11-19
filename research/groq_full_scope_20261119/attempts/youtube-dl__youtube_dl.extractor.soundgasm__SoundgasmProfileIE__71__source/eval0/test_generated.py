import re
import pytest
from youtube_dl.extractor.soundgasm import SoundgasmProfileIE

# Helper to create a fake extractor instance with overridden download method
class DummyExtractor(SoundgasmProfileIE):
    def __init__(self, webpage):
        super().__init__()
        self._webpage = webpage

    def _download_webpage(self, url, video_id, note=None, errnote=None, *, data=None, headers=None, timeout=None, add_ie=None):
        # ignore all parameters and return the preset webpage
        return self._webpage

def test_extract_single_entry(tmp_path):
    # Prepare a fake webpage containing one matching audio link
    profile_id = "ytdl"
    audio_url = f"https://soundgasm.net/u/{profile_id}/audio1.mp3"
    webpage = f'<html><body><a href="{audio_url}">Download</a></body></html>'
    extractor = DummyExtractor(webpage)

    result = extractor.sanitize_info(extractor._real_extract(f"http://soundgasm.net/u/{profile_id}"))
    # The result should be a playlist with one entry
    assert result['entries'] is not None
    assert len(result['entries']) == 1
    entry = result['entries'][0]
    assert entry['url'] == audio_url
    assert entry['ie_key'] == 'Soundgasm'

def test_extract_no_entries(tmp_path):
    # Prepare a fake webpage with no matching audio links
    profile_id = "emptyprofile"
    webpage = '<html><body>No audio here</body></html>'
    extractor = DummyExtractor(webpage)

    result = extractor.sanitize_info(extractor._real_extract(f"http://soundgasm.net/u/{profile_id}"))
    # The playlist should be empty
    assert result['entries'] == []
    assert result['id'] == profile_id

def test_invalid_url_raises(monkeypatch):
    # Use the real extractor but monkeypatch _download_webpage to raise an error
    extractor = SoundgasmProfileIE()
    def fake_download(url, video_id, **kwargs):
        raise Exception("Network error")
    monkeypatch.setattr(extractor, "_download_webpage", fake_download)

    with pytest.raises(Exception) as excinfo:
        extractor._real_extract("http://soundgasm.net/u/invalid")
    assert "Network error" in str(excinfo.value)
