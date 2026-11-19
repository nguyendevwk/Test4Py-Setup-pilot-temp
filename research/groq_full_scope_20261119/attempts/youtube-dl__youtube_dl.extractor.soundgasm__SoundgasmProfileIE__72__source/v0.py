import re
import pytest
from youtube_dl.extractor.soundgasm import SoundgasmProfileIE

# Helper to create a fake extractor instance with a custom _download_webpage
def make_extractor_with_webpage(webpage_content):
    ie = SoundgasmProfileIE()
    # Override the _download_webpage method to return the provided content
    ie._download_webpage = lambda url, video_id, note=None, errnote=None, *, data=None, headers=None, timeout=None, fatal=True: webpage_content
    return ie

def test_soundgasm_profile_extraction_normal(tmp_path):
    # Create a fake webpage containing two audio links for the profile 'ytdl'
    fake_webpage = '''
        <html>
            <body>
                <a href="https://soundgasm.net/u/ytdl/12345">Audio 1</a>
                <a href="https://soundgasm.net/u/ytdl/67890">Audio 2</a>
            </body>
        </html>
    '''
    ie = make_extractor_with_webpage(fake_webpage)
    result = ie._real_extract('https://soundgasm.net/u/ytdl')
    # The result should be a playlist with two entries
    assert result['entries'] is not None
    assert len(result['entries']) == 2
    # Each entry should be a dict with 'url' and 'ie_key'
    for entry in result['entries']:
        assert isinstance(entry, dict)
        assert 'url' in entry
        assert entry['ie_key'] == 'Soundgasm'
        # The URL should contain the profile id 'ytdl'
        assert re.search(r'/u/ytdl/', entry['url'])
    # The playlist id should match the profile id
    assert result['id'] == 'ytdl'

def test_soundgasm_profile_extraction_no_entries(tmp_path):
    # Fake webpage with no matching audio links
    fake_webpage = '''
        <html><body><p>No audio here</p></body></html>
    '''
    ie = make_extractor_with_webpage(fake_webpage)
    result = ie._real_extract('https://soundgasm.net/u/emptyprofile')
    # Should return an empty playlist
    assert result['entries'] == []
    assert result['id'] == 'emptyprofile'

def test_soundgasm_profile_extraction_invalid_url():
    ie = SoundgasmProfileIE()
    # Provide a URL that does not match the extractor's pattern
    with pytest.raises(Exception) as excinfo:
        ie._real_extract('https://example.com/not-a-profile')
    # The exception should indicate a URL mismatch
    assert 'does not match' in str(excinfo.value)
