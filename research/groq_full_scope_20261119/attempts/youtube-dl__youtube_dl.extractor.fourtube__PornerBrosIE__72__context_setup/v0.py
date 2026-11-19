import re
import pytest
from youtube_dl.extractor.fourtube import PornerBrosIE

# Test 1: Validate the URL regex and group extraction
def test_valid_url_parsing():
    url = "https://www.pornerbros.com/videos/skinny-brunette-takes-big-cock-down-her-anal-hole_181369"
    match = re.match(PornerBrosIE._VALID_URL, url)
    assert match is not None, "URL should match the regex"
    kind, video_id, display_id = match.group('kind', 'id', 'display_id')
    assert kind == 'www', "Kind should be 'www' for this URL"
    assert video_id == '181369', "Video ID should be extracted correctly"
    assert display_id == 'skinny-brunette-takes-big-cock-down-her-anal-hole', "Display ID should be extracted correctly"

# Test 2: Test _extract_formats with mocked _download_json
def test_extract_formats(monkeypatch):
    # Prepare a dummy instance with minimal required attributes
    ie = PornerBrosIE()
    # Mock _download_json to return a predictable token mapping
    def fake_download_json(url, video_id, data=None, headers=None):
        # The URL contains the media_id and sources joined by '+'
        # We ignore it and return a mapping for each source
        return {
            '720': 'https://example.com/720p.mp4',
            '480': 'https://example.com/480p.mp4',
            '360': 'https://example.com/360p.mp4',
        }
    monkeypatch.setattr(ie, "_download_json", fake_download_json)

    # Call _extract_formats with known parameters
    formats = ie._extract_formats(
        url="https://www.pornerbros.com/videos/video_181369",
        video_id="181369",
        media_id="12345",
        sources=['720', '480', '360']
    )

    # Verify that formats are sorted by quality descending
    qualities = [f["quality"] for f in formats]
    assert qualities == [720, 480, 360], "Formats should be sorted by quality descending"

    # Verify that each format dict contains expected keys and values
    for fmt in formats:
        assert fmt["url"].startswith("https://example.com/"), "URL should come from the mocked token"
        assert fmt["format_id"].endswith("p"), "Format ID should end with 'p'"
        assert fmt["resolution"].endswith("p"), "Resolution should end with 'p'"

# Test 3: Test URL template substitution for mobile URLs
def test_url_template_substitution():
    mobile_url = "https://m.pornerbros.com/videos/skinny-brunette-takes-big-cock-down-her-anal-hole_181369"
    match = re.match(PornerBrosIE._VALID_URL, mobile_url)
    assert match is not None, "Mobile URL should match the regex"
    kind, video_id, display_id = match.group('kind', 'id', 'display_id')
    # For mobile kind, the URL should be rewritten using the template
    if kind == 'm' or not display_id:
        rewritten_url = PornerBrosIE._URL_TEMPLATE % video_id
    else:
        rewritten_url = mobile_url
    assert rewritten_url == "https://www.pornerbros.com/videos/video_181369", "URL should be rewritten correctly for mobile"
