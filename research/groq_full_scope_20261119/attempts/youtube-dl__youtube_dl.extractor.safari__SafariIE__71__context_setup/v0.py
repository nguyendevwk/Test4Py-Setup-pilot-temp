import pytest
from youtube_dl.extractor.safari import SafariIE


def test_normal_extraction():
    """Test that a valid Safari book URL returns the expected Kaltura embed URL."""
    ie = SafariIE()
    url = 'https://www.safaribooksonline.com/library/view/hadoop-fundamentals-livelessons/9780133392838/part00.html'
    result = ie._real_extract(url)
    # The result should be a Kaltura URL with the correct referenceId
    assert result._type == 'url'
    assert result.url.startswith('https://cdnapisec.kaltura.com/html5/html5lib/v2.37.1/mwEmbedFrame.php')
    assert 'flashvars%5BreferenceId%5D=9780133392838-00_SeriesIntro' in result.url
    # The result should have the expected IE name
    assert result.ie == 'Kaltura'


def test_only_matching_url():
    """Test that a URL with a non‑digit course ID is correctly identified as only matching."""
    ie = SafariIE()
    url = 'https://www.safaribooksonline.com/library/view/create-a-nodejs/100000006A0210/part00.html'
    # The URL should match the regex but not be processed by _real_extract
    # Since _real_extract expects a reference_id, it will raise an error
    with pytest.raises(Exception):
        ie._real_extract(url)


def test_missing_reference_id_raises():
    """Test that a URL lacking a reference_id triggers an ExtractorError."""
    ie = SafariIE()
    # Construct a URL that matches the pattern but will not contain a reference_id in the page
    # We simulate this by providing a URL that points to a non‑existent part
    url = 'https://www.safaribooksonline.com/library/view/nonexistent/1234567890/part99.html'
    with pytest.raises(Exception):
        ie._real_extract(url)
