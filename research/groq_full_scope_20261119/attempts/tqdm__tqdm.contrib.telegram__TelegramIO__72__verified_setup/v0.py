import pytest
from tqdm.contrib.telegram import TelegramIO

def test_init_sets_attributes():
    """Verify that the constructor stores token, chat_id and creates a Session."""
    token = "dummy_token"
    chat_id = "dummy_chat"
    io = TelegramIO(token, chat_id)
    assert io.token == token
    assert io.chat_id == chat_id
    # Session should be an instance of requests.Session
    from requests import Session
    assert isinstance(io.session, Session)
    # text should be the class name
    assert io.text == "TelegramIO"
    # message_id property should be accessible (will raise on network)
    with pytest.raises(Exception):
        _ = io.message_id

def test_message_id_property_raises_on_network_error():
    """Accessing message_id should raise an exception when network is unreachable."""
    io = TelegramIO("invalid_token", "invalid_chat")
    with pytest.raises(Exception):
        _ = io.message_id

def test_write_returns_none_when_message_id_unavailable():
    """write should return None if message_id cannot be obtained."""
    io = TelegramIO("invalid_token", "invalid_chat")
    # Force message_id to raise by accessing it
    with pytest.raises(Exception):
        _ = io.message_id
    # Now call write; it will attempt to get message_id again and fail
    result = io.write("test")
    assert result is None
