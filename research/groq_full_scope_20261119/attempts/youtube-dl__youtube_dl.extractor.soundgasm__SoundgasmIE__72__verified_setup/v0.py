import re
import pytest
from youtube_dl.extractor.soundgasm import SoundgasmIE


class DummySoundgasmIE(SoundgasmIE):
    """Subclass that overrides network calls to return a controlled HTML page."""

    def __init__(self, html):
        super().__init__()
        self._html = html

    def _download_webpage(self, url, display_id, note=None, errnote=None, *, fatal=True):
        # Return the predefined HTML regardless of the URL
        return self._html


def test_soundgasm_extraction_success():
    # Construct a minimal HTML page that satisfies all regexes
    html = """
    <html>
      <head><title>Test</title></head>
      <body>
        <div class="jp-title">Piano sample</div>
        <div class="jp-description">Royalty Free Sample Music</div>
        <script>
          var audio = { m4a: 'https://cdn.soundgasm.net/audio/88abd86ea000cafe98f96321b23cc1206cbcbcc9.m4a' };
        </script>
      </body>
    </html>
    """
    extractor = DummySoundgasmIE(html)
    url = "http://soundgasm.net/u/ytdl/Piano-sample"
    result = extractor.extract(url)

    assert result["id"] == "88abd86ea000cafe98f96321b23cc1206cbcbcc9"
    assert result["display_id"] == "Piano-sample"
    assert result["url"] == "https://cdn.soundgasm.net/audio/88abd86ea000cafe98f96321b23cc1206cbcbcc9.m4a"
    assert result["vcodec"] == "none"
    assert result["title"] == "Piano sample"
    assert result["description"] == "Royalty Free Sample Music"
    assert result["uploader"] == "ytdl"


def test_soundgasm_missing_description():
    # HTML without a description element
    html = """
    <html>
      <body>
        <div class="jp-title">Piano sample</div>
        <script>
          var audio = { m4a: 'https://cdn.soundgasm.net/audio/88abd86ea000cafe98f96321b23cc1206cbcbcc9.m4a' };
        </script>
      </body>
    </html>
    """
    extractor = DummySoundgasmIE(html)
    url = "http://soundgasm.net/u/ytdl/Piano-sample"
    result = extractor.extract(url)

    assert result["description"] is None  # description is optional


def test_soundgasm_invalid_url_raises():
    extractor = DummySoundgasmIE("<html></html>")
    # URL that does not match the VALID_URL pattern should raise a ValueError
    with pytest.raises(ValueError):
        extractor.extract("http://invalidsite.com/u/ytdl/Piano-sample")
