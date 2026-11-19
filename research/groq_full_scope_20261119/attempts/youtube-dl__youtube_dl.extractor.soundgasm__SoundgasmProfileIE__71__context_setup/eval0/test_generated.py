import re
import pytest
from youtube_dl.extractor.soundgasm import SoundgasmProfileIE

# Helper to create an instance with overridden methods
def make_ie_with_overrides(overrides):
    ie = SoundgasmProfileIE()
    for name, func in overrides.items():
        setattr(ie, name, func)
    return ie

def test_real_extract_parses_multiple_entries():
    # Fake webpage containing two audio URLs for profile 'ytdl'
    fake_webpage = '''
        <html>
            <a href="https://soundgasm.net/u/ytdl/12345">Audio 1</a>
            <a href="https://soundgasm.net/u/ytdl/67890">Audio 2</a>
        </html>
    '''
    captured_entries = []

    def fake_download_webpage(url, video_id):
        assert url == 'http://soundgasm.net/u/ytdl'
        assert video_id == 'ytdl'
        return fake_webpage

    def fake_url_result(url, ie_name):
        captured_entries.append((url, ie_name))
        return {'url': url, 'ie': ie_name}

    def fake_playlist_result(entries, playlist_id):
        # Return a dict that contains the entries list and id
        return {'entries': entries, 'playlist_id': playlist_id}

    ie = make_ie_with_overrides({
        '_download_webpage': fake_download_webpage,
        'url_result': fake_url_result,
        'playlist_result': fake_playlist_result,
    })

    result = ie._real_extract('http://soundgasm.net/u/ytdl')
    assert result['playlist_id'] == 'ytdl'
    assert len(result['entries']) == 2
    assert captured_entries[0][0] == 'https://soundgasm.net/u/ytdl/12345'
    assert captured_entries[1][0] == 'https://soundgasm.net/u/ytdl/67890'
    assert all(entry['ie'] == 'Soundgasm' for entry in result['entries'])

def test_real_extract_no_entries_returns_empty_playlist():
    # Fake webpage with no matching hrefs
    fake_webpage = '<html><p>No audio here</p></html>'

    def fake_download_webpage(url, video_id):
        return fake_webpage

    def fake_playlist_result(entries, playlist_id):
        return {'entries': entries, 'playlist_id': playlist_id}

    ie = make_ie_with_overrides({
        '_download_webpage': fake_download_webpage,
        'playlist_result': fake_playlist_result,
    })

    result = ie._real_extract('http://soundgasm.net/u/emptyprofile')
    assert result['playlist_id'] == 'emptyprofile'
    assert result['entries'] == []

def test_real_extract_invalid_url_raises():
    ie = SoundgasmProfileIE()
    # URL that does not match the pattern should raise ExtractorError
    with pytest.raises(Exception) as excinfo:
        ie._real_extract('http://invalid.com/u/abc')
    # The exception should be due to _match_id failing
    assert 'Invalid URL' in str(excinfo.value) or 'does not match' in str(excinfo.value)
