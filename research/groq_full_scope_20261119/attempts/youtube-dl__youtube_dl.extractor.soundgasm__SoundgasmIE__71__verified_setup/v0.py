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
    """Test normal extraction with all fields present."""
    html = """
    <html>
      <div class="jp-title">Piano sample</div>
      <div class="jp-description">Royalty Free Sample Music</div>
      <script>
        var audio = {"m4a":"https://cdn.soundgasm.net/audio/88abd86ea000cafe98f96321b23cc1206cbcbcc9.m4a"};
      </script>
    </html>
    """
    extractor = DummySoundgasmIE(html)
    result = extractor._real_extract("http://soundgasm.net/u/ytdl/Piano-sample")
    assert result["id"] == "88abd86ea000cafe98f96321b23cc1206cbcbcc9"
    assert result["display_id"] == "Piano-sample"
    assert result["url"] == "https://cdn.soundgasm.net/audio/88abd86ea000cafe98f96321b23cc1206cbcbcc9.m4a"
    assert result["title"] == "Piano sample"
    assert result["description"] == "Royalty Free Sample Music"
    assert result["uploader"] == "ytdl"
    assert result["vcodec"] == "none"


def test_soundgasm_missing_description():
    """Test extraction when description is missing; description should be None."""
    html = """
    <html>
      <div class="jp-title">Piano sample</div>
      <script>
        var audio = {"m4a":"https://cdn.soundgasm.net/audio/88abd86ea000cafe98f96321b23cc1206cbcbcc9.m4a"};
      </script>
    </html>
    """
    extractor = DummySoundgasmIE(html)
    result = extractor._real_extract("http://soundgasm.net/u/ytdl/Piano-sample")
    assert result["description"] is None


def test_soundgasm_missing_audio_url():
    """Test extraction when audio URL pattern is not found; should raise ExtractorError."""
    html = """
    <html>
      <div class="jp-title">Piano sample</div>
      <div class="jp-description">Royalty Free Sample Music</div>
    </html>
    """
    extractor = DummySoundgasmIE(html)
    with pytest.raises(Exception) as excinfo:
        extractor._real_extract("http://soundgasm.net/u/ytdl/Piano-sample")
    assert "audio URL" in str(excinfo.value)
