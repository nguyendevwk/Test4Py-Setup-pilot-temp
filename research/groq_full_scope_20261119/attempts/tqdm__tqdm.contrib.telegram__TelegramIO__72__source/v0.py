import pytest
from tqdm.contrib.telegram import TelegramIO
from tqdm.auto import tqdm as tqdm_auto
from tqdm.std import TqdmWarning
from warnings import catch_warnings, simplefilter

# Use a dummy token and chat_id that will not succeed in contacting Telegram
DUMMY_TOKEN = "000000:dummy"
DUMMY_CHAT_ID = "123456"

def test_message_id_none_on_connection_error():
    """message_id should be None when the Telegram API is unreachable."""
    io = TelegramIO(DUMMY_TOKEN, DUMMY_CHAT_ID)
    # The first access to message_id triggers a POST request that will fail.
    # It should return None and not raise.
    assert io.message_id is None

def test_write_no_change_does_not_submit():
    """write should return None when the new text is identical to the current."""
    io = TelegramIO(DUMMY_TOKEN, DUMMY_CHAT_ID)
    # Force message_id to None to avoid network calls
    io._message_id = None
    # Set current text
    io.text = "original"
    # Attempt to write the same text
    result = io.write("original")
    # No future should be submitted
    assert result is None

def test_delete_handles_exception_and_returns_none():
    """delete should handle exceptions gracefully and return None."""
    io = TelegramIO(DUMMY_TOKEN, DUMMY_CHAT_ID)
    # Force message_id to None to avoid network calls
    io._message_id = None
    # Capture any warnings or output
    with catch_warnings(record=True) as w:
        simplefilter("always")
        result = io.delete()
        # No future should be submitted
        assert result is None
        # No warnings should be emitted for this scenario
        assert all(warning.category is not TqdmWarning for warning in w)
