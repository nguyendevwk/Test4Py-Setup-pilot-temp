import re
import pytest
from youtube_dl.extractor.soundgasm import SoundgasmProfileIE
from youtube_dl.utils import ExtractorError

class DummyDownloader:
    """A minimal downloader that reads a webpage from a file."""
    def __init__(self, webpage_path):
        self.webpage_path = webpage_path

    def _download_webpage(self, url, video_id, note=None, errnote=None, timeout=None, data=None, headers=None, query=None, fatal=True):
        with open(self.webpage_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _download_webpage(self, url, video_id, note=None, errnote=None, timeout=None, data=None, headers=None, query=None, fatal=True):
        with open(self.webpage_path, 'r', encoding='utf-8') as f:
            return f.read()

    # The InfoExtractor expects a method named _download_webpage
    def _download_webpage(self, url, video_id, note=None, errnote=None, timeout=None, data=None, headers=None, query=None, fatal=True):
        with open(self.webpage_path, 'r', encoding='utf-8') as f:
            return f.read()

    # Provide the method name used by InfoExtractor
    download_webpage = _download_webpage

def test_soundgasm_profile_extraction(tmp_path):
    """Normal extraction: one audio link is found."""
    # Prepare a fake webpage containing a single audio link
    profile_id = 'ytdl'
    audio_url = f'https://soundgasm.net/u/{profile_id}/audio1'
    webpage = f'''
        <html>
            <body>
                <a href="{audio_url}">Audio 1</a>
            </body>
        </html>
    '''
    file_path = tmp_path / 'page.html'
    file_path.write_text(webpage, encoding='utf-8')

    downloader = DummyDownloader(file_path)
    ie = SoundgasmProfileIE(downloader=downloader)
    result = ie.extract(f'http://soundgasm.net/u/{profile_id}')

    assert result['id'] == profile_id
    assert result['entries'] == [audio_url]
    assert result['playlist_count'] == 1

def test_soundgasm_profile_no_entries(tmp_path):
    """Boundary case: no audio links are present."""
    profile_id = 'empty'
    webpage = '''
        <html><body>No audio here.</body></html>
    '''
    file_path = tmp_path / 'empty.html'
    file_path.write_text(webpage, encoding='utf-8')

    downloader = DummyDownloader(file_path)
    ie = SoundgasmProfileIE(downloader=downloader)
    result = ie.extract(f'http://soundgasm.net/u/{profile_id}')

    assert result['id'] == profile_id
    assert result['entries'] == []
    assert result['playlist_count'] == 0

def test_soundgasm_profile_invalid_url():
    """Error case: URL does not match the expected pattern."""
    ie = SoundgasmProfileIE()
    with pytest.raises(ExtractorError):
        ie.extract('https://soundgasm.net/invalid/url')
