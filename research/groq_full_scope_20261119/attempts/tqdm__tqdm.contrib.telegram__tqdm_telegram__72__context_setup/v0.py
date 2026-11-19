import builtins
import types
import pytest
from tqdm.contrib.telegram import tqdm_telegram, TelegramIO
from tqdm.auto import tqdm as tqdm_auto
from tqdm import TqdmWarning
from warnings import warn

# Helper to replace requests.Session.post
class DummyResponse:
    def __init__(self, status=200, json_data=None):
        self.status_code = status
        self._json = json_data or {}
    def json(self):
        return self._json
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")

def dummy_post(url, data=None):
    # Simulate a 429 rate limit error
    if "sendMessage" in url:
        return DummyResponse(status=429, json_data={"result": {"message_id": 123}})
    return DummyResponse()

@pytest.fixture(autouse=True)
def patch_session(monkeypatch):
    # Patch Session.post to avoid real network calls
    monkeypatch.setattr("requests.Session.post", dummy_post)

def test_tqdm_telegram_normal_iteration(tmp_path):
    """Verify that tqdm_telegram iterates correctly and writes updates."""
    # Capture write calls
    writes = []

    original_write = TelegramIO.write
    def fake_write(self, s):
        writes.append(s)
        return original_write(self, s)
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(TelegramIO, "write", fake_write)

    # Use a short iterable
    data = list(range(3))
    with tqdm_telegram(data, token="dummy", chat_id="dummy", disable=False) as bar:
        for _ in bar:
            pass

    # Ensure at least one write call was made
    assert writes, "No write calls were made"
    # The last write should contain the final progress string
    assert "100%" in writes[-1]

def test_tqdm_telegram_disable_flag(tmp_path):
    """When disable=True, no TelegramIO should be created or used."""
    # Ensure TelegramIO is not instantiated
    with pytest.raises(AttributeError):
        _ = tqdm_telegram([], token="dummy", chat_id="dummy", disable=True).tgio

def test_tqdm_telegram_rate_limit_warning(caplog):
    """A 429 response should trigger a warning via TqdmWarning."""
    with caplog.at_level(TqdmWarning):
        bar = tqdm_telegram([], token="dummy", chat_id="dummy", disable=False)
        # Trigger message_id property
        _ = bar.tgio.message_id
    # Check that a warning was logged
    assert any(
        record.levelname == "WARNING" and isinstance(record.message, str)
        for record in caplog.records
    )
