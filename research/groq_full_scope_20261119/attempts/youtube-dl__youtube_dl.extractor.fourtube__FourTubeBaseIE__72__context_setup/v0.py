import re
import pytest
from youtube_dl.extractor.fourtube import FourTubeBaseIE
from youtube_dl.utils import int_or_none

class DummyFourTubeIE(FourTubeBaseIE):
    """A minimal subclass that overrides network calls for testing."""
    def __init__(self, token_map):
        super().__init__()
        self._token_map = token_map

    def _download_json(self, url, video_id, data=None, headers=None):
        # Return a copy to avoid accidental mutation
        return dict(self._token_map)

    def _sort_formats(self, formats):
        # Use the real sorting logic from InfoExtractor
        super()._sort_formats(formats)

def test_extract_formats_basic(tmp_path):
    # Prepare a dummy token map for three formats
    token_map = {"720": "https://example.com/720p",
                 "480": "https://example.com/480p",
                 "360": "https://example.com/360p"}
    ie = DummyFourTubeIE(token_map)
    url = "https://fourtube.com/watch?v=123"
    video_id = "123"
    media_id = "456"
    sources = ["720", "480", "360"]
    formats = ie._extract_formats(url, video_id, media_id, sources)

    # Verify that each format dict contains expected keys and values
    expected = {
        "720p": {"url": "https://example.com/720p", "format_id": "720p",
                 "resolution": "720p", "quality": 720},
        "480p": {"url": "https://example.com/480p", "format_id": "480p",
                 "resolution": "480p", "quality": 480},
        "360p": {"url": "https://example.com/360p", "format_id": "360p",
                 "resolution": "360p", "quality": 360},
    }
    for fmt in formats:
        assert fmt["format_id"] in expected
        assert fmt == expected[fmt["format_id"]]
    # Formats should be sorted by quality descending
    qualities = [f["quality"] for f in formats]
    assert qualities == sorted(qualities, reverse=True)

def test_extract_formats_missing_token_raises():
    # Token map missing one format
    token_map = {"720": "https://example.com/720p",
                 "480": "https://example.com/480p"}
    ie = DummyFourTubeIE(token_map)
    url = "https://fourtube.com/watch?v=123"
    video_id = "123"
    media_id = "456"
    sources = ["720", "480", "360"]  # 360 missing in token_map

    with pytest.raises(KeyError):
        ie._extract_formats(url, video_id, media_id, sources)

def test_extract_formats_empty_sources_returns_empty_list(tmp_path):
    # Even if token_map is empty, _extract_formats should return an empty list
    token_map = {}
    ie = DummyFourTubeIE(token_map)
    url = "https://fourtube.com/watch?v=123"
    video_id = "123"
    media_id = "456"
    sources = []
    formats = ie._extract_formats(url, video_id, media_id, sources)
    assert formats == []
