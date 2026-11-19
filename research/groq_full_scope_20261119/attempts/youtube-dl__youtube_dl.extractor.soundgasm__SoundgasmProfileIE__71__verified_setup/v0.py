import re
import pytest
from youtube_dl.extractor.soundgasm import SoundgasmProfileIE
from youtube_dl.utils import RegexMatchError


class FakeSoundgasmIE(SoundgasmProfileIE):
    """Subclass that overrides webpage download for testing."""

    def __init__(self, webpage: str):
        super().__init__(downloader=None)
        self._webpage = webpage

    def _download_webpage(self, url, video_id, note=None, errnote=None, *, data=None, headers=None, timeout=None, fatal=True):
        # Return the pre‑defined webpage regardless of URL
        return self._webpage


def test_valid_extract():
    """Test that a valid profile URL returns the expected playlist."""
    # Construct a fake webpage containing two audio links for profile 'ytdl'
    fake_webpage = '''
        <html>
            <a href="https://soundgasm.net/u/ytdl/12345.mp3">Audio 1</a>
            <a href="https://soundgasm.net/u/ytdl/67890.mp3">Audio 2</a>
        </html>
    '''
    ie = FakeSoundgasmIE(fake_webpage)
    result = ie.extract('http://soundgasm.net/u/ytdl')
    # The result should be a playlist with two entries
    assert result['entries'] is not None
    assert len(result['entries']) == 2
    # Each entry should be a dict with 'url' and 'ie_key'
    for entry in result['entries']:
        assert entry['url'].startswith('https://soundgasm.net/u/ytdl/')
        assert entry['ie_key'] == 'Soundgasm'


def test_no_audio_links():
    """Test that a profile with no audio links yields an empty playlist."""
    fake_webpage = '''
        <html>
            <p>No audio here.</p>
        </html>
    '''
    ie = FakeSoundgasmIE(fake_webpage)
    result = ie.extract('http://soundgasm.net/u/emptyprofile')
    # The playlist should contain zero entries
    assert result['entries'] == []
    # The playlist id should match the profile id
    assert result['id'] == 'emptyprofile'


def test_invalid_url():
    """Test that an invalid URL raises a RegexMatchError."""
    ie = FakeSoundgasmIE('')
    with pytest.raises(RegexMatchError):
        ie.extract('https://example.com/not-a-soundgasm-profile')
