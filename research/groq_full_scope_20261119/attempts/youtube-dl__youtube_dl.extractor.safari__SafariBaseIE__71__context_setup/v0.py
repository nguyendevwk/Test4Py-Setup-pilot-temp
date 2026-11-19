import json
import types
import pytest
from youtube_dl.extractor.safari import SafariBaseIE
from youtube_dl.utils import ExtractorError


class DummyURLH:
    """Simple mock for a URL handle with a geturl method."""
    def __init__(self, url):
        self._url = url

    def geturl(self):
        return self._url


def test_login_skipped_when_no_credentials(tmp_path):
    """When no login info is provided, LOGGED_IN remains False."""
    ie = SafariBaseIE()
    # Patch _get_login_info to return None, simulating no credentials
    ie._get_login_info = lambda: (None, None)

    # Patch _download_webpage_handle to avoid network calls
    ie._download_webpage_handle = lambda url, *_, **__: (None, DummyURLH(url))

    # Call _login and verify no exception and LOGGED_IN stays False
    ie._login()
    assert ie.LOGGED_IN is False


def test_login_successful_sets_logged_in(tmp_path):
    """When login succeeds, LOGGED_IN is set to True."""
    ie = SafariBaseIE()
    ie._get_login_info = lambda: ("user@example.com", "secret")

    # Mock the initial login-check page
    ie._download_webpage_handle = lambda url, *_, **__: (
        None,
        DummyURLH("https://learning.oreilly.com/accounts/login-check/?next=/home/"),
    )

    # Mock the JSON login response indicating success
    def mock_download_json_handle(url, *_, **__):
        auth = {"logged_in": True, "redirect_uri": "https://learning.oreilly.com/home/"}
        return auth, DummyURLH(auth["redirect_uri"])

    ie._download_json_handle = mock_download_json_handle

    # Mock cookie application (no-op)
    ie._apply_first_set_cookie_header = lambda urlh, cookie: None

    # Mock the final redirect page
    ie._download_webpage_handle = lambda url, *_, **__: (
        None,
        DummyURLH("https://learning.oreilly.com/home/"),
    )

    ie._login()
    assert ie.LOGGED_IN is True


def test_login_failure_raises_error(tmp_path):
    """If credentials are returned but login is not successful, an error is raised."""
    ie = SafariBaseIE()
    ie._get_login_info = lambda: ("user@example.com", "wrong")

    # Mock the initial login-check page
    ie._download_webpage_handle = lambda url, *_, **__: (
        None,
        DummyURLH("https://learning.oreilly.com/accounts/login-check/?next=/home/"),
    )

    # Mock the JSON login response with credentials but no logged_in or redirect_uri
    def mock_download_json_handle(url, *_, **__):
        auth = {"credentials": "Invalid credentials"}
        return auth, DummyURLH("https://learning.oreilly.com/home/")

    ie._download_json_handle = mock_download_json_handle

    # Mock cookie application (no-op)
    ie._apply_first_set_cookie_header = lambda urlh, cookie: None

    # Expect ExtractorError due to failed login
    with pytest.raises(ExtractorError) as excinfo:
        ie._login()
    assert "Unable to login" in str(excinfo.value)
