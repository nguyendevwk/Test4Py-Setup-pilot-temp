import re
import pytest
from youtube_dl.extractor.nrk import NRKPlaylistIE
from youtube_dl.utils import ExtractorError

# Helper subclass that overrides network-dependent methods
class DummyNRKPlaylistIE(NRKPlaylistIE):
    def __init__(self, webpage):
        super().__init__(downloader=None)
        self._webpage = webpage

    def _download_webpage(self, url, playlist_id, note=None, errnote=None, headers=None, data=None, timeout=None, *, fatal=True):
        # Return the pre‑provided webpage regardless of URL
        return self._webpage

    def _match_id(self, url):
        # Use the regex from the real class to extract the id
        m = re.search(self._VALID_URL, url)
        if not m:
            raise ExtractorError('Invalid URL')
        return m.group('id')

# Test 1: Normal extraction with two video items
def test_nrk_playlist_normal(tmp_path):
    # Construct a minimal webpage containing two video IDs and og tags
    webpage = '''
        <html>
        <head>
            <meta property="og:title" content="Test Playlist Title" />
            <meta property="og:description" content="Test description." />
        </head>
        <body>
            <div class="rich" data-video-id="vid1"></div>
            <div class="rich" data-video-id="vid2"></div>
        </body>
        </html>
    '''
    url = 'http://www.nrk.no/test/playlist-1.12345678'
    ie = DummyNRKPlaylistIE(webpage)
    result = ie._real_extract(url)

    # Verify playlist metadata
    assert result['id'] == 'playlist-1.12345678'
    assert result['title'] == 'Test Playlist Title'
    assert result['description'] == 'Test description.'

    # Verify entries
    entries = result['entries']
    assert len(entries) == 2
    assert entries[0]['url'] == 'nrk:vid1'
    assert entries[1]['url'] == 'nrk:vid2'

# Test 2: Boundary case with no video items
def test_nrk_playlist_no_items(tmp_path):
    webpage = '''
        <html>
        <head>
            <meta property="og:title" content="Empty Playlist" />
            <meta property="og:description" content="No videos." />
        </head>
        <body>
            <p>No videos here.</p>
        </body>
        </html>
    '''
    url = 'http://www.nrk.no/test/empty-1.87654321'
    ie = DummyNRKPlaylistIE(webpage)
    result = ie._real_extract(url)

    assert result['id'] == 'empty-1.87654321'
    assert result['title'] == 'Empty Playlist'
    assert result['description'] == 'No videos.'
    assert result['entries'] == []

# Test 3: Error when URL does not match the expected pattern
def test_nrk_playlist_invalid_url(tmp_path):
    webpage = '<html></html>'
    url = 'http://www.example.com/not-nrk'
    ie = DummyNRKPlaylistIE(webpage)
    with pytest.raises(ExtractorError):
        ie._real_extract(url)
