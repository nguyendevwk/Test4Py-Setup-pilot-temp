import re
import pytest
from youtube_dl.extractor.soundgasm import SoundgasmIE

# Helper to create a minimal extractor with overridden download method
class DummyExtractor(SoundgasmIE):
    def __init__(self, webpage):
        super().__init__()
        self._webpage = webpage

    def _download_webpage(self, url, display_id, note=None, errnote=None, *, data=None, headers=None, timeout=None, err=None):
        return self._webpage


def test_soundgasm_normal_extraction():
    # Construct a minimal HTML page containing all required elements
    html = """
    <html>
    <head><title>Test</title></head>
    <body>
        <div class="jp-title">Piano sample</div>
        <div class="jp-description">Royalty Free Sample Music</div>
        <script>
            var audio = { m4a: "https://cdn.soundgasm.net/audio/88abd86ea000cafe98f96321b23cc1206cbcbcc9.m4a" };
        </script>
    </body>
    </html>
    """
    url = "http://soundgasm.net/u/ytdl/Piano-sample"
    extractor = DummyExtractor(html)
    result = extractor._real_extract(url)

    assert result["id"] == "88abd86ea000cafe98f96321b23cc1206cbcbcc9"
    assert result["display_id"] == "Piano-sample"
    assert result["url"] == "https://cdn.soundgasm.net/audio/88abd86ea000cafe98f96321b23cc1206cbcbcc9.m4a"
    assert result["title"] == "Piano sample"
    assert result["description"] == "Royalty Free Sample Music"
    assert result["uploader"] == "ytdl"
    assert result["vcodec"] == "none"


def test_soundgasm_missing_description():
    # HTML without a description element
    html = """
    <html>
    <body>
        <div class="jp-title">Piano sample</div>
        <script>
            var audio = { m4a: "https://cdn.soundgasm.net/audio/88abd86ea000cafe98f96321b23cc1206cbcbcc9.m4a" };
        </script>
    </body>
    </html>
    """
    url = "http://soundgasm.net/u/ytdl/Piano-sample"
    extractor = DummyExtractor(html)
    result = extractor._real_extract(url)

    # Description should be None because it is optional
    assert result["description"] is None
    assert result["title"] == "Piano sample"


def test_soundgasm_invalid_url():
    # URL that does not match the extractor's pattern
    url = "http://soundgasm.net/invalid/123"
    extractor = DummyExtractor("<html></html>")
    with pytest.raises(re.error):
        # The extractor will raise a regex error when matching fails
        extractor._real_extract(url)
