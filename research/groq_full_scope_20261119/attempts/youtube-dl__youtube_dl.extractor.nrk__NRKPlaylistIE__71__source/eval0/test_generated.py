import re
import pytest
from youtube_dl.extractor.nrk import NRKPlaylistIE

# Sample HTML snippets for title and description extraction
SAMPLE_HTML_TITLE = '''
<html><head><meta property="og:title" content="Sample Title"></head></html>
'''
SAMPLE_HTML_DESC = '''
<html><head><meta property="og:description" content="Sample Description"></head></html>
'''

def test_valid_url_pattern_matches_expected_and_not_invalid():
    """Ensure the NRKPlaylistIE _VALID_URL regex matches valid NRK playlist URLs
    and does not match URLs that should be excluded (e.g., video or skole paths)."""
    valid_urls = [
        'http://www.nrk.no/troms/gjenopplev-den-historiske-solformorkelsen-1.12270763',
        'https://nrk.no/kultur/bok/rivertonprisen-til-karin-fossum-1.12266449',
        'http://nrk.no/region/abc/def/ghi-12345678',
    ]
    invalid_urls = [
        'http://www.nrk.no/video/abc-12345678',
        'https://nrk.no/skole/abc-12345678',
        'http://nrk.no/abc/video/12345678',
    ]
    pattern = re.compile(NRKPlaylistIE._VALID_URL)
    for url in valid_urls:
        assert pattern.match(url), f"URL should match: {url}"
    for url in invalid_urls:
        assert not pattern.match(url), f"URL should not match: {url}"

def test_extract_title_returns_og_title():
    """Test that _extract_title correctly retrieves the og:title meta property."""
    ie = NRKPlaylistIE()
    title = ie._extract_title(SAMPLE_HTML_TITLE)
    assert title == "Sample Title", f"Expected 'Sample Title', got {title}"

def test_extract_description_returns_og_description():
    """Test that _extract_description correctly retrieves the og:description meta property."""
    ie = NRKPlaylistIE()
    description = ie._extract_description(SAMPLE_HTML_DESC)
    assert description == "Sample Description", f"Expected 'Sample Description', got {description}"
