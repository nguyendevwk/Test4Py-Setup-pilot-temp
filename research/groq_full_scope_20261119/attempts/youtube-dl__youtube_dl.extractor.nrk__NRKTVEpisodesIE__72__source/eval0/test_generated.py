import re
import pytest
from youtube_dl.extractor.nrk import NRKTVEpisodesIE

# Test 1: Validate the URL matching regex
def test_valid_url_regex():
    url = "https://tv.nrk.no/program/episodes/nytt-paa-nytt/69031"
    pattern = NRKTVEpisodesIE._VALID_URL
    match = re.match(pattern, url)
    assert match is not None, "URL should match the _VALID_URL pattern"
    assert match.group('id') == "69031", "Captured group 'id' should be '69031'"

# Test 2: Extract title from a sample HTML snippet
def test_extract_title_from_html():
    sample_html = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Sample Episode Title</h1>
                <p>Some content here.</p>
            </body>
        </html>
    """
    ie = NRKTVEpisodesIE()
    title = ie._extract_title(sample_html)
    assert title == "Sample Episode Title", "Title extraction should return the correct text"

# Test 3: Check that the extractor reports suitability for a known URL
def test_suitable_for_known_url():
    url = "https://tv.nrk.no/program/episodes/nytt-paa-nytt/69031"
    ie = NRKTVEpisodesIE()
    assert ie.suitable(url) is True, "Extractor should be suitable for the given NRK TV episodes URL"
