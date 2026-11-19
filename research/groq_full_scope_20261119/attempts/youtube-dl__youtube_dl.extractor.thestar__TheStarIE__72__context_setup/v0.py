import re
import pytest
from youtube_dl.extractor.thestar import TheStarIE, InfoExtractor


def test_valid_url_match():
    """The _VALID_URL regex should correctly capture the id part of a Star URL."""
    url = "http://www.thestar.com/life/2016/02/01/mankind-why-this-woman-started-a-men-s-skincare-line.html"
    match = re.match(TheStarIE._VALID_URL, url)
    assert match is not None, "URL should match the regex"
    assert match.group("id") == "mankind-why-this-woman-started-a-men-s-skincare-line", \
        "Captured id should be the path segment before .html"


def test_real_extract_success():
    """_real_extract should return a Brightcove URL when the brightcove id is present."""
    class DummyTheStarIE(TheStarIE):
        def _download_webpage(self, url, display_id, note=None, errnote=None, timeout=None, *, data=None, headers=None, query=None, ext=None, ie_key=None, **kw):
            # Return a minimal webpage containing the brightcove id
            return '<script>var mainartBrightcoveVideoId="1234567890";</script>'

    dummy = DummyTheStarIE()
    result = dummy._real_extract("http://www.thestar.com/example.html")
    assert result.url == "http://players.brightcove.net/794267642001/default_default/index.html?videoId=1234567890"
    assert result.ie_key == "BrightcoveNew"
    assert result.info_dict["id"] == "1234567890"


def test_real_extract_missing_id():
    """_real_extract should raise ExtractorError when brightcove id is not found."""
    class DummyTheStarIE(TheStarIE):
        def _download_webpage(self, url, display_id, note=None, errnote=None, timeout=None, *, data=None, headers=None, query=None, ext=None, ie_key=None, **kw):
            # Return a webpage without the brightcove id
            return "<html><body>No video here</body></html>"

    dummy = DummyTheStarIE()
    with pytest.raises(Exception) as excinfo:
        dummy._real_extract("http://www.thestar.com/no-video.html")
    assert "brightcove id" in str(excinfo.value)
