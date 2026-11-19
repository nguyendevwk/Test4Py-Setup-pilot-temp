import pytest
from tqdm.contrib.telegram import tqdm_telegram

def test_init_disable_true(tmp_path):
    """When disable=True, tqdm_telegram should not create a TelegramIO instance."""
    # Instantiate with disable=True to avoid network calls
    t = tqdm_telegram(iterable=[1, 2, 3], disable=True)
    # The instance should not have a tgio attribute
    assert not hasattr(t, "tgio")
    # The progress bar should still iterate correctly
    result = list(t)
    assert result == [1, 2, 3]

def test_display_no_tgio(tmp_path):
    """Calling display with disable=True should not raise an exception."""
    t = tqdm_telegram(iterable=[1, 2], disable=True)
    # Manually trigger display; it should handle missing tgio gracefully
    try:
        t.display()
    except Exception as e:
        pytest.fail(f"display raised an exception: {e}")

def test_clear_no_tgio(tmp_path):
    """Calling clear with disable=True should not raise an exception."""
    t = tqdm_telegram(iterable=[1, 2], disable=True)
    # Manually trigger clear; it should handle missing tgio gracefully
    try:
        t.clear()
    except Exception as e:
        pytest.fail(f"clear raised an exception: {e}")
