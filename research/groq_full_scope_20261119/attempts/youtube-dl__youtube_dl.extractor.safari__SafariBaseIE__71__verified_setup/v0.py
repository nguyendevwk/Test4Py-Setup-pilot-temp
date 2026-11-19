import json
import types
import pytest
from youtube_dl.extractor.safari import SafariBaseIE
from youtube_dl.utils import ExtractorError


class DummyURLH:
    def __init__(self, url):
        self._url = url

    def geturl(self):
        return self._url


def test_login_skipped_when_no_credentials():
    """When no login info is provided, _login should return immediately."""
    ie = SafariBaseIE()
    # Patch _get_login_info to return None
    ie._get_login_info = lambda: (None, None)
    # Patch _download_webpage_handle to raise if called (should not be called)
    ie._download_webpage_handle = lambda *_, **__: (_raise := (_ for _ in ()).throw(RuntimeError("Should not be called")))
    # Ensure LOGGED_IN remains False
    ie._login()
    assert not ie.LOGGED_IN


def test_login_fails_with_missing_credentials():
    """If the login response contains credentials but no logged_in flag, an error is raised."""
    ie = SafariBaseIE()
    ie._get_login_info = lambda: ("user@example.com", "wrongpass")

    # First webpage download: not logged in
    ie._download_webpage_handle = lambda *_, **__: (None, DummyURLH("https://learning.oreilly.com/accounts/login-check/"))

    # JSON download returns auth dict with credentials but not logged in
    ie._download_json_handle = lambda *_, **__: {
        "logged_in": False,
        "redirect_uri": None,
        "credentials": "Invalid credentials",
    }

    with pytest.raises(ExtractorError, match="Unable to login: Invalid credentials"):
        ie._login()


def test_successful_login_sets_flag():
    """A successful login flow sets LOGGED_IN to True."""
    ie = SafariBaseIE()
    ie._get_login_info = lambda: ("user@example.com", "correctpass")

    # First webpage download: not logged in
    ie._download_webpage_handle = lambda *_, **__: (None, DummyURLH("https://learning.oreilly.com/accounts/login-check/"))

    # JSON download returns auth dict indicating logged in
    ie._download_json_handle = lambda *_, **__: {
        "logged_in": True,
        "redirect_uri": None,
        "credentials": None,
    }

    # Completing login webpage download: now logged in
    def completing_download(*_, **__):
        return (None, DummyURLH("https://learning.oreilly.com/home/"))

    ie._download_webpage_handle = completing_download

    ie._login()
    assert ie.LOGGED_IN
