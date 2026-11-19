import re
import pytest
from youtube_dl.extractor.nrk import NRKPlaylistIE

# Test 1: Validate that the _VALID_URL regex correctly captures the ID part of a URL.
def test_valid_url_capture():
    url = "https://www.nrk.no/troms/gjenopplev-den-historiske-solformorkelsen-1.12270763"
    match = re.match(NRKPlaylistIE._VALID_URL, url)
    assert match is not None, "URL should match the _VALID_URL pattern"
    assert match.group("id") == "gjenopplev-den-historiske-solformorkelsen-1.12270763"

# Test 2: Verify that the _ITEM_RE regex extracts all video IDs from a sample HTML snippet.
def test_item_re_extraction():
    html = '''
    <div class="rich" data-video-id="12345"></div>
    <span class="rich" data-video-id="67890"></span>
    <div class="rich" data-video-id="abcde"></div>
    '''
    ids = re.findall(NRKPlaylistIE._ITEM_RE, html)
    assert ids == ["12345", "67890", "abcde"], "All data-video-id values should be extracted"

# Test 3: Ensure that _extract_title returns None when no OpenGraph title is present.
def test_extract_title_missing():
    ie = NRKPlaylistIE()
    # A minimal HTML without an og:title meta tag
    webpage = "<html><head></head><body>No title here</body></html>"
    title = ie._extract_title(webpage)
    assert title is None, "Title should be None when og:title is absent"
