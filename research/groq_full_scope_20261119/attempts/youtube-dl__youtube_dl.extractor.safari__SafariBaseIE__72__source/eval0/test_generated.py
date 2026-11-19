import json
import pytest
from youtube_dl.extractor.safari import SafariBaseIE
from youtube_dl.utils import ExtractorError

class DummySafariIE(SafariBaseIE):
    """A minimal implementation of SafariBaseIE for testing purposes."""

    def __init__(self, login_info=None, login_page_redirect=None,
                 auth_response=None, final_redirect=None):
        self._login_info = login_info
        self._login_page_redirect = login_page_redirect
        self._auth_response = auth_response
        self._final_redirect = final_redirect
        self._cookies = {}
        super().__init__()

    # Override required methods
    def _get_login_info(self):
        return self._login_info

    def _download_webpage_handle(self, url, video_id, note):
        # Simulate a response object with geturl method
        class DummyResponse:
            def __init__(self, url):
                self._url = url
            def geturl(self):
                return self._url
        if url == 'https://learning.oreilly.com/accounts/login-check/':
            return None, DummyResponse(self._login_page_redirect or url)
        if url == self._final_redirect or url == self._auth_response.get('redirect_uri'):
            return None, DummyResponse(self._final_redirect or url)
        raise ValueError(f"Unexpected URL: {url}")

    def _download_json_handle(self, url, video_id, note, data=None, headers=None,
                              expected_status=None):
        return self._auth_response

    def _apply_first_set_cookie_header(self, urlh, cookie_name):
        # Simulate setting a cookie
        self._cookies[cookie_name] = 'dummy_value'

def test_no_login_info_does_not_set_logged_in():
    """When no login info is provided, LOGGED_IN should remain False."""
    ie = DummySafariIE(login_info=None)
    ie._real_initialize()
    assert not ie.LOGGED_IN

def test_successful_login_sets_logged_in():
    """A successful login flow should set LOGGED_IN to True."""
    # Simulate login page redirecting to a URL containing '/home/'
    login_page_redirect = 'https://learning.oreilly.com/home/'
    # Simulate auth response with redirect_uri
    auth_response = {
        'logged_in': True,
        'redirect_uri': 'https://learning.oreilly.com/home/',
        'credentials': None
    }
    ie = DummySafariIE(
        login_info=('user@example.com', 'password'),
        login_page_redirect=login_page_redirect,
        auth_response=auth_response,
        final_redirect=auth_response['redirect_uri']
    )
    ie._real_initialize()
    assert ie.LOGGED_IN

def test_login_failure_raises_extractor_error():
    """If the auth response indicates failure, an ExtractorError should be raised."""
    # Simulate login page redirecting to a URL not containing '/home/'
    login_page_redirect = 'https://learning.oreilly.com/login/'
    # Simulate auth response with missing logged_in and redirect_uri but credentials present
    auth_response = {
        'logged_in': False,
        'redirect_uri': None,
        'credentials': 'Invalid credentials'
    }
    ie = DummySafariIE(
        login_info=('user@example.com', 'wrongpass'),
        login_page_redirect=login_page_redirect,
        auth_response=auth_response
    )
    with pytest.raises(ExtractorError) as excinfo:
        ie._real_initialize()
    assert 'Unable to login' in str(excinfo.value)
