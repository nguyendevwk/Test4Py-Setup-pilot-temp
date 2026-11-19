import pytest
from tqdm.contrib.telegram import TelegramIO

@pytest.fixture
def telegram_io():
    """Create a TelegramIO instance with dummy credentials."""
    return TelegramIO(token="invalid_token", chat_id="123456")

def test_message_id_none(telegram_io):
    """The message_id property should return None when the API call fails."""
    # The first access triggers an HTTP request that will fail.
    assert telegram_io.message_id is None

def test_write_empty_returns_none(telegram_io):
    """Writing an empty string should return None and not raise."""
    # The message_id is already None from the previous test.
    result = telegram_io.write("")
    assert result is None

def test_delete_returns_none(telegram_io):
    """Deleting a non-existent message should return None and not raise."""
    result = telegram_io.delete()
    assert result is None
