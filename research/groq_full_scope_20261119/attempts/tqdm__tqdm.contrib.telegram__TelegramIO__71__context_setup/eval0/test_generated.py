import pytest
from tqdm.contrib.telegram import TelegramIO
from requests import Session

def test_write_empty_and_duplicate(tmp_path):
    """Test that write handles empty string and duplicate text correctly."""
    # Create a TelegramIO instance with dummy credentials
    io = TelegramIO(token="dummy", chat_id="dummy")
    # Patch the session.post to raise an exception so that message_id stays None
    def fake_post(*args, **kwargs):
        raise Exception("network error")
    io.session.post = fake_post

    # Initially, message_id should be None due to the fake post
    assert io.message_id is None

    # Writing an empty string should set text to "..."
    io.write("")
    assert io.text == "..."

    # Writing the same text again should not trigger a new post
    # Since message_id is still None, write will return None
    result = io.write("...")
    assert result is None

def test_message_id_creation_and_error_handling(tmp_path):
    """Test that message_id property handles HTTP errors and rate limits."""
    io = TelegramIO(token="dummy", chat_id="dummy")

    # Patch session.post to simulate a 429 rate limit response
    class FakeResponse:
        status_code = 429
        def json(self):
            return {}
        def raise_for_status(self):
            raise Exception("429 Too Many Requests")
    def fake_post(*args, **kwargs):
        return FakeResponse()
    io.session.post = fake_post

    # Accessing message_id should trigger the warning and return None
    assert io.message_id is None

def test_delete_handles_exception(tmp_path):
    """Test that delete handles exceptions gracefully."""
    io = TelegramIO(token="dummy", chat_id="dummy")

    # Patch session.post to raise an exception when delete is called
    def fake_post(*args, **kwargs):
        raise Exception("delete error")
    io.session.post = fake_post

    # delete should return None and not raise
    assert io.delete() is None
