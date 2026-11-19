import re
import pytest
from youtube_dl.extractor.nrk import NRKTVEpisodesIE

def test_valid_url_parsing():
    """Ensure the regex captures the episode id correctly."""
    url = "https://tv.nrk.no/program/episodes/nytt-paa-nytt/69031"
    match = re.match(NRKTVEpisodesIE._VALID_URL, url)
    assert match is not None, "URL should match the VALID_URL pattern"
    assert match.group("id") == "69031", "Captured id should be '69031'"

def test_extract_title_success():
    """_extract_title should return the title when an <h1> tag is present."""
    webpage = """
        <html>
            <head><title>Test</title></head>
            <body>
                <h1>Sample Episode Title</h1>
                <p>Some content</p>
            </body>
        </html>
    """
    ie = NRKTVEpisodesIE()
    title = ie._extract_title(webpage)
    assert title == "Sample Episode Title", "Title should be extracted from the <h1> tag"

def test_extract_title_missing():
    """When no <h1> tag is present, _extract_title should return None (fatal=False)."""
    webpage = """
        <html>
            <head><title>No Title</title></head>
            <body>
                <p>Content without a header</p>
            </body>
        </html>
    """
    ie = NRKTVEpisodesIE()
    title = ie._extract_title(webpage)
    assert title is None, "Missing <h1> should result in None when fatal=False"
