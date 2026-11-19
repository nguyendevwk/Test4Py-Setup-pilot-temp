import pytest
from youtube_dl.extractor.itv import ITVBTCCIE
from youtube_dl.utils import ExtractorError

# Sample HTML containing two video IDs and a title
SAMPLE_HTML = """
<html>
<head><title>Test Page</title></head>
<body>
<div class="video" data-video-id="12345"></div>
<div class="video" data-video-id="67890"></div>
</body>
</html>
"""

def test_itvbtccie_extract_entries(monkeypatch):
    """Verify that the extractor returns the correct number of entries and video IDs."""
    extractor = ITVBTCCIE()
    # Mock _download_webpage to return SAMPLE_HTML
    monkeypatch.setattr(extractor, "_download_webpage", lambda url, video_id: SAMPLE_HTML)
    # Use a URL that matches the pattern
    url = "http://www.itv.com/btcc/races/btcc-2018-all-the-action-from-brands-hatch"
    result = extractor._real_extract(url)
    # The result should be a playlist with two entries
    assert result["entries"] is not None
    entries = list(result["entries"])
    assert len(entries) == 2
    # Each entry should be a dict with the correct video_id
    video_ids = {entry["video_id"] for entry in entries}
    assert video_ids == {"12345", "67890"}

def test_itvbtccie_title_extraction(monkeypatch):
    """Verify that the extractor correctly extracts the title from the og:title meta tag."""
    extractor = ITVBTCCIE()
    # HTML with an og:title meta tag
    html_with_title = """
    <html>
    <head>
        <meta property="og:title" content="BTCC 2018: All the action from Brands Hatch" />
    </head>
    <body>
        <div data-video-id="11111"></div>
    </body>
    </html>
    """
    monkeypatch.setattr(extractor, "_download_webpage", lambda url, video_id: html_with_title)
    url = "http://www.itv.com/btcc/races/btcc-2018-all-the-action-from-brands-hatch"
    result = extractor._real_extract(url)
    # The title should match the og:title content
    assert result["title"] == "BTCC 2018: All the action from Brands Hatch"

def test_itvbtccie_invalid_url_raises(monkeypatch):
    """Verify that an invalid URL raises an ExtractorError."""
    extractor = ITVBTCCIE()
    # No need to mock _download_webpage because the URL won't match
    invalid_url = "http://www.itv.com/invalid/path"
    with pytest.raises(ExtractorError):
        extractor._real_extract(invalid_url)
