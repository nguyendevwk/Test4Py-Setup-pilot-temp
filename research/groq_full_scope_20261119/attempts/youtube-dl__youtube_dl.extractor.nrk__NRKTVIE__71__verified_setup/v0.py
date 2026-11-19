import pytest
from youtube_dl.extractor.nrk import NRKTVIE
from youtube_dl.utils import ExtractorError

def test_real_extract_returns_expected_url_result(tmp_path):
    """Test that _real_extract returns a url_result with correct format."""
    ie = NRKTVIE()
    url = "https://tv.nrk.no/program/MDDP12000117"
    result = ie._real_extract(url)
    # The result should be a UrlResult instance
    assert hasattr(result, "url") and hasattr(result, "ie_key")
    # The URL should be prefixed with 'nrk:' and contain the video id
    assert result.url == "nrk:MDDP12000117"
    # The extractor key should be NRKIE
    assert result.ie_key() == "NRKIE"

def test_real_extract_invalid_url_raises_error(tmp_path):
    """Test that an invalid URL raises ExtractorError."""
    ie = NRKTVIE()
    # URL does not match the _VALID_URL pattern
    invalid_url = "https://example.com/not-a-valid-url"
    with pytest.raises(ExtractorError):
        ie._real_extract(invalid_url)

def test_real_extract_video_id_extraction(tmp_path):
    """Test that the video id is correctly extracted from various URL forms."""
    ie = NRKTVIE()
    # Test with a URL containing a path segment before the id
    url1 = "https://tv.nrk.no/serie/20-spoersmaal-tv/MUHH48000314/23-05-2014"
    result1 = ie._real_extract(url1)
    assert result1.url == "nrk:MUHH48000314"

    # Test with a URL that has a trailing slash
    url2 = "https://tv.nrk.no/program/mdfp15000514/"
    result2 = ie._real_extract(url2)
    assert result2.url == "nrk:MDFP15000514"

    # Test with a URL that includes a fragment
    url3 = "https://tv.nrk.no/serie/tour-de-ski/MSPO40010515/06-01-2015#del=2"
    result3 = ie._real_extract(url3)
    assert result3.url == "nrk:MSPO40010515"
