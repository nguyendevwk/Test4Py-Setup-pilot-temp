import re
import pytest
from youtube_dl.extractor.soundgasm import SoundgasmIE

class DummySoundgasmIE(SoundgasmIE):
    """Subclass that overrides _download_webpage to return a custom HTML string."""
    def __init__(self, webpage: str):
        super().__init__(downloader=None)
        self._webpage = webpage

    def _download_webpage(self, url, display_id, note=None, errnote=None, *, data=None, headers=None, timeout=None, err=None):
        return self._webpage


def test_soundgasm_normal_extraction():
    # Construct a minimal HTML that satisfies all regexes
    html = """
    <html>
      <div class="jp-title">Piano sample</div>
      <div class="jp-description">Royalty Free Sample Music</div>
      <script>
        var audio = { m4a: 'https://example.com/audio/88abd86ea000cafe98f96321b23cc1206cbcbcc9.m4a' };
      </script>
    </html>
    """
    extractor = DummySoundgasmIE(html)
    result = extractor._real_extract('http://soundgasm.net/u/ytdl/Piano-sample')
    assert result['id'] == '88abd86ea000cafe98f96321b23cc1206cbcbcc9'
    assert result['display_id'] == 'Piano-sample'
    assert result['url'] == 'https://example.com/audio/88abd86ea000cafe98f96321b23cc1206cbcbcc9.m4a'
    assert result['title'] == 'Piano sample'
    assert result['description'] == 'Royalty Free Sample Music'
    assert result['uploader'] == 'ytdl'
    assert result['vcodec'] == 'none'


def test_soundgasm_missing_description():
    # HTML without description; description should be None
    html = """
    <html>
      <div class="jp-title">Piano sample</div>
      <script>
        var audio = { m4a: 'https://example.com/audio/88abd86ea000cafe98f96321b23cc1206cbcbcc9.m4a' };
      </script>
    </html>
    """
    extractor = DummySoundgasmIE(html)
    result = extractor._real_extract('http://soundgasm.net/u/ytdl/Piano-sample')
    assert result['description'] is None


def test_soundgasm_missing_audio_url_raises():
    # HTML missing the m4a URL; should raise a RegexNotFoundError
    html = """
    <html>
      <div class="jp-title">Piano sample</div>
      <div class="jp-description">Royalty Free Sample Music</div>
    </html>
    """
    extractor = DummySoundgasmIE(html)
    with pytest.raises(extractor.RegexNotFoundError):
        extractor._real_extract('http://soundgasm.net/u/ytdl/Piano-sample')
