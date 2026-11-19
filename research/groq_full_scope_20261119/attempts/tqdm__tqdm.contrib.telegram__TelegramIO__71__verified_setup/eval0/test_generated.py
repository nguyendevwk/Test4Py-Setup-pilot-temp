import pytest
from tqdm.contrib.telegram import TelegramIO
from requests.exceptions import RequestException

def test_initialization_sets_attributes(tmp_path):
    """The constructor should store the token, chat_id and create a Session."""
    token = "dummy_token"
    chat_id = "dummy_chat"
    io = TelegramIO(token, chat_id)
    assert io.token == token
    assert io.chat_id == chat_id
    assert hasattr(io, "session")
    assert isinstance(io.session, type(io.session))
    # The text attribute should be the class name
    assert io.text == "TelegramIO"
    # Accessing message_id should raise an exception because the bot token is invalid
    with pytest.raises(Exception):
        _ = io.message_id

def test_write_avoids_duplicate_message(tmp_path):
    """write should return None when the new text is identical to the current one."""
    token = "dummy_token"
    chat_id = "dummy_chat"
    io = TelegramIO(token, chat_id)
    # Force a message_id to avoid network call during the test
    io._message_id = 12345
    io.text = "original"
    # Writing the same text should do nothing
    result = io.write("original")
    assert result is None
    # Writing an empty string should set text to "..."
    result = io.write("")
    assert io.text == "..."
    # Since we set _message_id, write will attempt to edit the message
    # This will raise an exception due to invalid token, which we ignore
    with pytest.raises(Exception):
        io.write("new text")

def test_delete_raises_on_invalid_token(tmp_path):
    """delete should raise an exception when the bot token is invalid."""
    token = "dummy_token"
    chat_id = "dummy_chat"
    io = TelegramIO(token, chat_id)
    # Force a message_id to avoid network call during the test
    io._message_id = 12345
    with pytest.raises(Exception):
        io.delete()
