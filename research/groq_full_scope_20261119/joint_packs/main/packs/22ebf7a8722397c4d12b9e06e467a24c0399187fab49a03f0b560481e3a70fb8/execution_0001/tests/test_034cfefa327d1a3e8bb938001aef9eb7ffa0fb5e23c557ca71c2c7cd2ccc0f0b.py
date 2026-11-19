import pytest
from youtube_dl.extractor.safari import SafariBaseIE

# Test 1: Verify that the class constants are set correctly
def test_safari_base_ie_constants():
    assert SafariBaseIE._LOGIN_URL == 'https://learning.oreilly.com/accounts/login/'
    assert SafariBaseIE._API_BASE == 'https://learning.oreilly.com/api/v1'
    assert SafariBaseIE._API_FORMAT == 'json'
    assert SafariBaseIE._NETRC_MACHINE == 'safari'
    # LOGGED_IN should start as False
    assert SafariBaseIE.LOGGED_IN is False

# Test 2: Ensure that _real_initialize calls _login
def test_real_initialize_calls_login(monkeypatch):
    called = False

    def fake_login(self):
        nonlocal called
        called = True
        # Simulate successful login by setting LOGGED_IN
        self.LOGGED_IN = True

    monkeypatch.setattr(SafariBaseIE, "_login", fake_login, raising=True)
    ie = SafariBaseIE()
    ie._real_initialize()
    assert called is True
    assert ie.LOGGED_IN is True

# Test 3: Confirm that the instance can be created without errors and
# that its default state is as expected
def test_safari_base_ie_initial_state():
    ie = SafariBaseIE()
    # Instance should not be logged in initially
    assert ie.LOGGED_IN is False
    # The instance should have the expected API base and format
    assert ie._API_BASE == 'https://learning.oreilly.com/api/v1'
    assert ie._API_FORMAT == 'json'
