import re
import pytest
from youtube_dl.extractor.nrk import NRKPlaylistIE

# Helper to create a fake extractor instance with overridden download method
def make_extractor(webpage_content):
    class DummyExtractor(NRKPlaylistIE):
        def _download_webpage(self, url, playlist_id, *args, **kwargs):
            return webpage_content
    return DummyExtractor()

def test_normal_extraction(tmp_path):
    # A minimal fake webpage containing two video items and metadata
    webpage = '''
        <html>
        <head>
            <meta property="og:title" content="Sample Playlist" />
            <meta property="og:description" content="A test playlist." />
        </head>
        <body>
            <div class="rich" data-video-id="vid123"></div>
            <div class="rich" data-video-id="vid456"></div>
        </body>
        </html>
    '''
    extractor = make_extractor(webpage)
    result = extractor._real_extract('http://www.nrk.no/test/playlist-1')
    assert result['entries'] == [
        extractor.url_result('nrk:vid123', 'NRKIE'),
        extractor.url_result('nrk:vid456', 'NRKIE')
    ]
    assert result['id'] == 'playlist-1'
    assert result['title'] == 'Sample Playlist'
    assert result['description'] == 'A test playlist.'

def test_no_items(tmp_path):
    # Webpage with no matching items should yield empty playlist
    webpage = '''
        <html><head><meta property="og:title" content="Empty" /></head>
        <body><p>No videos here.</p></body></html>
    '''
    extractor = make_extractor(webpage)
    result = extractor._real_extract('http://www.nrk.no/test/empty-1')
    assert result['entries'] == []
    assert result['id'] == 'empty-1'
    assert result['title'] == 'Empty'
    assert result['description'] is None

def test_missing_title_raises_error(tmp_path):
    # Webpage missing og:title should trigger fatal error in _extract_title
    webpage = '''
        <html><head><meta property="og:description" content="Desc" /></head>
        <body><div class="rich" data-video-id="vid789"></div></body></html>
    '''
    extractor = make_extractor(webpage)
    with pytest.raises(Exception) as excinfo:
        extractor._real_extract('http://www.nrk.no/test/no-title-1')
    assert 'Unable to find title' in str(excinfo.value)
