import json
import types
import pytest
from youtube_dl.extractor.safari import SafariBaseIE


class DummyHandle:
    """Simple object mimicking a urllib response with geturl."""
    def __init__(self, url):
        self._url = url

    def geturl(self):
        return self._url


class TestSafariBaseIE:
    def test_login_skipped_when_no_credentials(self):
        """When no login info is provided, LOGGED_IN stays False."""
        class TestIE(SafariBaseIE):
            def _get_login_info(self):
                return None

            # Override network methods to avoid actual HTTP calls
            def _download_webpage_handle(self, *args, **kwargs):
                raise AssertionError("Network call should not happen")

            def _download_json_handle(self, *args, **kwargs):
                raise AssertionError("Network call should not happen")

        ie = TestIE()
        ie._real_initialize()
        assert ie.LOGGED_IN is False

    def test_login_successful_with_mocked_handle(self):
        """Simulate a successful login by providing a handle that reports a logged‑in URL."""
        class TestIE(SafariBaseIE):
            def _get_login_info(self):
                return ("user@example.com", "secret")

            def _download_webpage_handle(self, url, *args, **kwargs):
                # First call returns a redirect URL containing 'login-check'
                if "login-check" in url:
                    return DummyHandle("https://learning.oreilly.com/accounts/login-check/?next=/home/")
                # Second call after auth redirects to home
                return DummyHandle("https://learning.oreilly.com/home/")

            def _download_json_handle(self, url, *args, **kwargs):
                # Return a JSON dict that mimics a successful auth response
                return {
                    "logged_in": True,
                    "redirect_uri": "https://learning.oreilly.com/home/",
                    "credentials": None,
                }

            def _apply_first_set_cookie_header(self, urlh, cookie):
                # No-op for test
                pass

        ie = TestIE()
        ie._real_initialize()
        assert ie.LOGGED_IN is True

    def test_login_failure_raises_error(self):
        """If the auth response indicates failure, an ExtractorError is raised."""
        class TestIE(SafariBaseIE):
            def _get_login_info(self):
                return ("user@example.com", "wrong")

            def _download_webpage_handle(self, url, *args, **kwargs):
                return DummyHandle("https://learning.oreilly.com/accounts/login-check/?next=/home/")

            def _download_json_handle(self, url, *args, **kwargs):
                # Simulate failure: logged_in False, no redirect_uri, but credentials present
                return {
                    "logged_in": False,
                    "redirect_uri": None,
                    "credentials": "Invalid credentials",
                }

            def _apply_first_set_cookie_header(self, urlh, cookie):
                pass

        ie = TestIE()
        with pytest.raises(Exception) as excinfo:
            ie._real_initialize()
        assert "Unable to login" in str(excinfo.value)
