import re
import pytest
from youtube_dl.extractor.soundgasm import SoundgasmProfileIE

# Helper to create a fake webpage containing two audio links for a given profile id
def fake_webpage(profile_id: str) -> str:
    return f'''
    <html>
        <body>
            <a href="https://soundgasm.net/u/{profile_id}/audio1.mp3">Audio 1</a>
            <a href="https://soundgasm.net/u/{profile_id}/audio2.mp3">Audio 2</a>
        </body>
    </html>
    '''

def test_profile_extractor_parses_multiple_entries(tmp_path):
    """Verify that the extractor returns a playlist with all matching audio URLs."""
    ie = SoundgasmProfileIE()
    profile_id = "testuser"

    # Patch the downloader to return our fake webpage
    def fake_download(url, video_id):
        assert url == f"https://soundgasm.net/u/{profile_id}"
        assert video_id == profile_id
        return fake_webpage(profile_id)

    ie._download_webpage = fake_download

    result = ie._real_extract(f"https://soundgasm.net/u/{profile_id}")

    # The result should be a playlist with two entries
    assert result['entries'] is not None
    assert len(result['entries']) == 2
    # Each entry should be a dict with the correct URL and IE name
    for entry, suffix in zip(result['entries'], ("audio1.mp3", "audio2.mp3")):
        assert entry['url'] == f"https://soundgasm.net/u/{profile_id}/{suffix}"
        assert entry['ie_key'] == 'Soundgasm'

def test_profile_extractor_no_entries(tmp_path):
    """Verify that the extractor returns an empty playlist when no audio links are found."""
    ie = SoundgasmProfileIE()
    profile_id = "emptyprofile"

    def fake_download(url, video_id):
        assert url == f"https://soundgasm.net/u/{profile_id}"
        assert video_id == profile_id
        # Return a page with no matching links
        return '<html><body>No audio here</body></html>'

    ie._download_webpage = fake_download

    result = ie._real_extract(f"https://soundgasm.net/u/{profile_id}")

    # The playlist should contain zero entries
    assert result['entries'] is not None
    assert len(result['entries']) == 0

def test_profile_extractor_invalid_url_raises():
    """Verify that an invalid URL raises a ValueError due to regex mismatch."""
    ie = SoundgasmProfileIE()
    invalid_url = "https://soundgasm.net/invalid/path"

    with pytest.raises(ValueError):
        ie._real_extract(invalid_url)
