import pytest
from youtube_dl.extractor.nrk import NRKPlaylistIE

# Test 1: Verify that the extractor recognises a valid NRK playlist URL
def test_nrk_playlist_suitable():
    extractor = NRKPlaylistIE()
    valid_url = "http://www.nrk.no/troms/gjenopplev-den-historiske-solformorkelsen-1.12270763"
    assert extractor.suitable(valid_url) is True

# Test 2: Verify that the title extraction works with a minimal HTML containing an og:title tag
def test_nrk_extract_title():
    extractor = NRKPlaylistIE()
    html = """
        <html>
            <head>
                <meta property="og:title" content="Sample NRK Title" />
            </head>
            <body></body>
        </html>
    """
    title = extractor._extract_title(html)
    assert title == "Sample NRK Title"

# Test 3: Verify that the extractor does not consider an unrelated URL as suitable
def test_nrk_playlist_not_suitable():
    extractor = NRKPlaylistIE()
    invalid_url = "https://www.example.com/some/other/page"
    assert extractor.suitable(invalid_url) is False
