import pytest
from youtube_dl.extractor.thestar import TheStarIE

# Sample webpage containing the Brightcove ID
SAMPLE_WEBPAGE = """
<html>
<head><title>Test</title></head>
<body>
<script>
var mainartBrightcoveVideoId = "1234567890";
</script>
</body>
</html>
"""

def test_suitable_url():
    """The extractor should recognize a valid thestar URL."""
    extractor = TheStarIE()
    assert extractor.suitable('http://www.thestar.com/life/2016/02/01/mankind-why-this-woman-started-a-men-s-skincare-line.html')
    assert not extractor.suitable('http://www.example.com/video.html')

def test_extract_returns_brightcove_url():
    """_real_extract should return the Brightcove URL constructed from the ID."""
    extractor = TheStarIE()
    # Patch _download_webpage to return our sample HTML
    extractor._download_webpage = lambda url, display_id: SAMPLE_WEBPAGE
    result = extractor._real_extract('http://www.thestar.com/example.html')
    expected_url = 'http://players.brightcove.net/794267642001/default_default/index.html?videoId=1234567890'
    assert result.url == expected_url
    assert result.info_dict['id'] == '1234567890'
    assert result.info_dict['ie_key'] == 'BrightcoveNew'

def test_extract_raises_on_missing_id():
    """If the Brightcove ID is missing, a regex error should be raised."""
    extractor = TheStarIE()
    # Provide HTML without the Brightcove ID
    extractor._download_webpage = lambda url, display_id: "<html></html>"
    with pytest.raises(Exception) as excinfo:
        extractor._real_extract('http://www.thestar.com/example.html')
    assert 'brightcove id' in str(excinfo.value)
