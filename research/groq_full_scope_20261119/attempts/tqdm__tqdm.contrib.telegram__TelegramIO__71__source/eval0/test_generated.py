import pytest
from tqdm.contrib.telegram import TelegramIO


class DummyTelegramIO(TelegramIO):
    """Subclass that records the arguments passed to submit instead of executing them."""
    def __init__(self, token, chat_id):
        super().__init__(token, chat_id)
        self.submitted = []

    def submit(self, func, url, data=None):
        # Record the call and return a dummy future-like object
        self.submitted.append((func, url, data))
        class DummyFuture:
            def result(self):
                return "dummy"
        return DummyFuture()


def test_write_same_text_returns_none(tmp_path):
    """write should return None when the new text is identical to the current text."""
    io = DummyTelegramIO("dummy_token", "dummy_chat")
    io.text = "same_text"
    # The write method should detect the duplicate and return immediately
    result = io.write("same_text")
    assert result is None
    # No submit call should have been made
    assert io.submitted == []


def test_write_calls_submit_with_correct_url_and_data(tmp_path):
    """write should submit a POST to the editMessageText endpoint with proper data."""
    io = DummyTelegramIO("dummy_token", "dummy_chat")
    # Force a message_id to avoid network call
    io._message_id = 123
    io.text = "old_text"
    io.write("new_text")
    # One submit call should have been recorded
    assert len(io.submitted) == 1
    func, url, data = io.submitted[0]
    # Verify the URL uses the correct endpoint
    assert url == f"{io.API}{io.token}/editMessageText"
    # Verify the data payload contains the expected fields
    assert data["chat_id"] == io.chat_id
    assert data["message_id"] == 123
    assert data["text"] == "`new_text`"
    assert data["parse_mode"] == "MarkdownV2"


def test_delete_uses_incorrect_url(tmp_path):
    """delete should submit to a malformed URL due to missing f-string formatting."""
    io = DummyTelegramIO("dummy_token", "dummy_chat")
    # Force a message_id to avoid network call
    io._message_id = 456
    io.delete()
    # One submit call should have been recorded
    assert len(io.submitted) == 1
    func, url, data = io.submitted[0]
    # The URL should incorrectly contain the literal '{self.API}' string
    assert url == '{self.API}{self.token}/deleteMessage'
    # The data payload should still contain the correct chat_id and message_id
    assert data["chat_id"] == io.chat_id
    assert data["message_id"] == 456
