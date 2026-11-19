import os
import pytest
from tqdm.contrib.telegram import tqdm_telegram

def test_init_with_disable_true(tmp_path):
    """When disable=True, no TelegramIO is created and no tgio attribute exists."""
    # Ensure environment variables are not set to avoid accidental TelegramIO creation
    os.environ.pop("TQDM_TELEGRAM_TOKEN", None)
    os.environ.pop("TQDM_TELEGRAM_CHAT_ID", None)

    # Instantiate with disable=True
    t = tqdm_telegram(range(3), disable=True)
    # The instance should not have a tgio attribute
    assert not hasattr(t, "tgio")
    # The progress bar should still iterate correctly
    assert list(t) == [0, 1, 2]
    t.close()

def test_display_bar_format_modification(tmp_path):
    """The display method should replace '<bar/>' and '{bar}' in bar_format."""
    # Instantiate with disable=True to avoid TelegramIO
    t = tqdm_telegram(range(5), disable=True)
    # Set a custom bar_format containing placeholders
    t.format_dict["bar_format"] = "<bar/> {percentage}%"
    # Call display
    t.display()
    # The bar_format should now have the placeholders replaced
    assert "{bar:10u}" in t.format_dict["bar_format"]
    assert "<bar/>" not in t.format_dict["bar_format"]
    t.close()

def test_close_with_disable_true(tmp_path):
    """close() should return immediately when disable=True."""
    t = tqdm_telegram(range(2), disable=True)
    # close should not raise and should return None
    assert t.close() is None
