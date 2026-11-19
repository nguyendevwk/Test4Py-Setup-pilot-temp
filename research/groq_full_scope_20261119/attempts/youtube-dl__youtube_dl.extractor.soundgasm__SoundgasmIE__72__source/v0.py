import re
import pytest
from youtube_dl.extractor.soundgasm import SoundgasmIE

# Helper to create a minimal extractor that overrides _download_webpage
class DummyExtractor(SoundgasmIE):
    def __init__(self, webpage):
        super().__init__()
        self._webpage = webpage

    def _download_webpage(self, url, display_id):
        return self._webpage

def test_normal_extraction():
    # Construct a webpage with all expected elements
    webpage = '''
        <html>
        <div class="jp-title">Piano sample</div>
        <div class="jp-description">Royalty Free Sample Music</div>
        <script>
            var audio = {"m4a":"https://cdn.soundgasm.net/audio/88abd86ea000cafe98f96321b23cc1206cbcbcc9.m4a"};
        </script>
        </html>
    '''
    extractor = DummyExtractor(webpage)
    url = 'http://soundgasm.net/u/ytdl/Piano-sample'
    result = extractor._real_extract(url)

    assert result['id'] == '88abd86ea000cafe98f96321b23cc1206cbcbcc9'
    assert result['display_id'] == 'Piano-sample'
    assert result['url'] == 'https://cdn.soundgasm.net/audio/88abd86ea000cafe98f96321b23cc1206cbcbcc9.m4a'
    assert result['vcodec'] == 'none'
    assert result['title'] == 'Piano sample'
    assert result['description'] == 'Royalty Free Sample Music'
    assert result['uploader'] == 'ytdl'

def test_missing_description():
    # Webpage without description; description should be None
    webpage = '''
        <html>
        <div class="jp-title">Piano sample</div>
        <script>
            var audio = {"m4a":"https://cdn.soundgasm.net/audio/88abd86ea000cafe98f96321b23cc1206cbcbcc9.m4a"};
        </script>
        </html>
    '''
    extractor = DummyExtractor(webpage)
    url = 'http://soundgasm.net/u/ytdl/Piano-sample'
    result = extractor._real_extract(url)

    assert result['description'] is None

def test_title_fallback_to_display_id():
    # Webpage without title; title should fallback to display_id
    webpage = '''
        <html>
        <div class="jp-description">Royalty Free Sample Music</div>
        <script>
            var audio = {"m4a":"https://cdn.soundgasm.net/audio/88abd86ea000cafe98f96321b23cc1206cbcbcc9.m4a"};
        </script>
        </html>
    '''
    extractor = DummyExtractor(webpage)
    url = 'http://soundgasm.net/u/ytdl/Piano-sample'
    result = extractor._real_extract(url)

    assert result['title'] == 'Piano-sample'
