import re
import pytest
from youtube_dl.extractor.safari import SafariIE
from youtube_dl.utils import ExtractorError


class DummySafariIE(SafariIE):
    """SafariIE subclass with overridden network methods for deterministic tests."""

    def __init__(self, downloader=None, logged_in=False):
        super().__init__(downloader)
        self.LOGGED_IN = logged_in

    def _download_webpage_handle(self, url, video_id):
        # Return a dummy webpage containing the required data attributes
        webpage = (
            f'<div data-reference-id="ref-{video_id}" '
            f'data-partner-id="partner-{video_id}" '
            f'data-ui-id="ui-{video_id}"></div>'
        )
        class DummyHandle:
            def geturl(self_inner):
                return url
        return webpage, DummyHandle()

    def _search_regex(self, pattern, string, name, group=None, default=None):
        # Simple regex search that returns the first group
        m = re.search(pattern, string)
        if m:
            return m.group(group) if group else m.group(1)
        return default

    def _download_json(self, url, video_id, note, errnote, fatal, headers):
        # Return a dummy session JSON if LOGGED_IN is True
        if self.LOGGED_IN:
            return {"session": "dummy_session"}
        return None


def test_normal_extraction_with_webpage_data(tmp_path):
    """Test extraction when reference_id is not in URL and data is parsed from webpage."""
    url = "https://www.safaribooksonline.com/library/view/hadoop-fundamentals-livelessons/9780133392838/part00.html"
    ie = DummySafariIE()
    result = ie._real_extract(url)

    # The result should be a Kaltura URL with correct query parameters
    assert result._type == "url"
    assert result._url.startswith("https://cdnapisec.kaltura.com/html5/html5lib/v2.37.1/mwEmbedFrame.php")
    parsed = re.search(r"wid=_(?P<wid>[^&]+)&uiconf_id=(?P<uiconf>[^&]+)&flashvars%5BreferenceId%5D=(?P<ref>[^&]+)", result._url)
    assert parsed, "Expected query parameters not found"
    assert parsed.group("wid") == "partner-9780133392838-part00"
    assert parsed.group("uiconf") == "ui-9780133392838-part00"
    assert parsed.group("ref") == "ref-9780133392838-part00"


def test_extraction_with_reference_id_in_url(tmp_path):
    """Test extraction when reference_id is present directly in the URL."""
    url = "https://www.safaribooksonline.com/videos/python-programming-language/9780134217314/9780134217314-PYMC_13_00"
    ie = DummySafariIE()
    result = ie._real_extract(url)

    # The result should contain the reference_id from the URL
    assert result._type == "url"
    assert result._url.startswith("https://cdnapisec.kaltura.com/html5/html5lib/v2.37.1/mwEmbedFrame.php")
    parsed = re.search(r"flashvars%5BreferenceId%5D=(?P<ref>[^&]+)", result._url)
    assert parsed, "Reference ID not found in query"
    assert parsed.group("ref") == "9780134217314-PYMC_13_00"


def test_extraction_without_kaltura_session(tmp_path):
    """Test extraction when LOGGED_IN is True but no session JSON is returned."""
    url = "https://www.safaribooksonline.com/library/view/hadoop-fundamentals-livelessons/9780133392838/part00.html"
    ie = DummySafariIE(logged_in=True)

    # Override _download_json to return None to simulate missing session
    def no_session(url, video_id, note, errnote, fatal, headers):
        return None
    ie._download_json = no_session

    result = ie._real_extract(url)

    # Ensure that the URL does not contain a flashvars[ks] parameter
    assert "flashvars%5Bks%5D=" not in result._url
