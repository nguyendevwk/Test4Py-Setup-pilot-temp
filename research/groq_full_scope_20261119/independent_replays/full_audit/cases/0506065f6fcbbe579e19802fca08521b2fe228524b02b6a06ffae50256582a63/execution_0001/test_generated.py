import pytest
from youtube_dl.extractor.safari import SafariBaseIE


def test_default_constants():
    """Verify that the class constants are set to the expected values."""
    assert SafariBaseIE._LOGIN_URL == 'https://learning.oreilly.com/accounts/login/'
    assert SafariBaseIE._NETRC_MACHINE == 'safari'
    assert SafariBaseIE._API_BASE == 'https://learning.oreilly.com/api/v1'
    assert SafariBaseIE._API_FORMAT == 'json'
    # LOGGED_IN should start as False
    assert SafariBaseIE.LOGGED_IN is False


def test_real_initialize_calls_login(monkeypatch):
    """Ensure that _real_initialize triggers the _login method."""
    called = False

    def fake_login(self):
        nonlocal called
        called = True

    monkeypatch.setattr(SafariBaseIE, "_login", fake_login, raising=True)
    ie = SafariBaseIE()
    ie._real_initialize()
    assert called is True, "Expected _login to be called during _real_initialize"


def test_login_flag_set_after_successful_login(monkeypatch):
    """Simulate a successful login by overriding _login to set LOGGED_IN."""
    def fake_login(self):
        self.LOGGED_IN = True

    monkeypatch.setattr(SafariBaseIE, "_login", fake_login, raising=True)
    ie = SafariBaseIE()
    ie._real_initialize()
    assert ie.LOGGED_IN is True, "LOGGED_IN should be True after successful login"
