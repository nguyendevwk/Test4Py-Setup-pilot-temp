import re
import pytest
from youtube_dl.extractor.nrk import NRKPlaylistIE

# Helper to create a minimal webpage with og tags
def make_webpage(title, description):
    return f"""<html><head>
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    </head><body></body></html>"""

def test_valid_url_match():
    """NRKPlaylistIE should match valid NRK playlist URLs."""
    ie = NRKPlaylistIE()
    valid_urls = [
        "http://www.nrk.no/troms/gjenopplev-den-historiske-solformorkelsen-1.12270763",
        "https://nrk.no/kultur/bok/rivertonprisen-til-karin-fossum-1.12266449",
        "http://nrk.no/nyheter/eksempel-1.12345678",
    ]
    for url in valid_urls:
        assert re.match(ie._VALID_URL, url), f"URL should match: {url}"
    # URLs that should not match
    invalid_urls = [
        "http://www.nrk.no/video/123456",
        "https://nrk.no/skole/123456",
        "http://example.com/nrk/no/123456",
    ]
    for url in invalid_urls:
        assert not re.match(ie._VALID_URL, url), f"URL should not match: {url}"

def test_extract_title_and_description():
    """_extract_title and _extract_description should return correct values from og tags."""
    ie = NRKPlaylistIE()
    title = "Test Title"
    description = "Test Description"
    webpage = make_webpage(title, description)
    extracted_title = ie._extract_title(webpage)
    extracted_description = ie._extract_description(webpage)
    assert extracted_title == title, "Title extraction failed"
    assert extracted_description == description, "Description extraction failed"

def test_extract_title_fallback_and_missing_description():
    """_extract_title should not raise if og:title is missing; _extract_description should raise."""
    ie = NRKPlaylistIE()
    # Webpage without og:title
    webpage_no_title = "<html><head></head><body></body></html>"
    # Should return None (fatal=False)
    assert ie._extract_title(webpage_no_title) is None
    # Webpage without og:description should raise ExtractorError
    webpage_no_desc = "<html><head><meta property=\"og:title\" content=\"Only Title\"></head><body></body></html>"
    with pytest.raises(Exception):
        ie._extract_description(webpage_no_desc)
