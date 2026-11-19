import re
import pytest
from youtube_dl.extractor.itv import ITVBTCCIE
from youtube_dl.extractor.brightcove import BrightcoveNewIE
from youtube_dl.utils import ExtractorError

# Helper to create an ITVBTCCIE instance with a custom _download_webpage
def make_ie(webpage_content):
    ie = ITVBTCCIE()
    ie._download_webpage = lambda url, video_id: webpage_content
    return ie

def test_itvbtccie_extracts_entries_and_title(tmp_path):
    # Sample webpage containing two video ids and a title
    webpage = """
    <html><head><title>Test Page</title></head>
    <body>
    <meta property="og:title" content="BTCC 2018: All the action from Brands Hatch"/>
    <div data-video-id="12345"></div>
    <div data-video-id="67890"></div>
    </body></html>
    """
    ie = make_ie(webpage)
    result = ie.extract('http://www.itv.com/btcc/test/playlist')
    # The result should be a playlist with two entries
    assert result['entries'] is not None
    entries = list(result['entries'])
    assert len(entries) == 2
    # Each entry should be a dict with 'url' smuggled and 'ie' pointing to BrightcoveNewIE
    for entry, vid in zip(entries, ['12345', '67890']):
        assert entry['ie'] == BrightcoveNewIE.ie_key()
        assert entry['video_id'] == vid
        # The smuggled URL should contain the video id
        assert f"videoId={vid}" in entry['url']
    # Title should be extracted from og:title
    assert result['title'] == "BTCC 2018: All the action from Brands Hatch"

def test_itvbtccie_no_video_ids_returns_empty_playlist(tmp_path):
    # Webpage with no data-video-id attributes
    webpage = """
    <html><head><title>No Videos</title></head>
    <body><p>No video here</p></body></html>
    """
    ie = make_ie(webpage)
    result = ie.extract('http://www.itv.com/btcc/test/empty')
    # entries should be an empty list
    entries = list(result['entries'])
    assert entries == []
    # Title should be None because og:title not found
    assert result['title'] is None

def test_itvbtccie_invalid_url_raises_error():
    ie = ITVBTCCIE()
    # URL that does not match the _VALID_URL pattern should raise ExtractorError
    with pytest.raises(ExtractorError):
        ie.extract('http://www.example.com/not-itv-url')
