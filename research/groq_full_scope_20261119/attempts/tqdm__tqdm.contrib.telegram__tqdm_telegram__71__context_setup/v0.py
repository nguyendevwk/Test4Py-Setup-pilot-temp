import pytest
from tqdm.contrib.telegram import tqdm_telegram

class DummyIO:
    def __init__(self):
        self.written = []
        self.deleted = False

    def write(self, s):
        self.written.append(s)

    def delete(self):
        self.deleted = True

def test_disable_no_tgio(tmp_path):
    """When disable=True, tqdm_telegram should not create a TelegramIO instance."""
    t = tqdm_telegram(disable=True)
    assert not hasattr(t, "tgio"), "tgio should not be created when disabled"

def test_display_replaces_bar_format(tmp_path):
    """display should replace <bar/> with a formatted bar and call tgio.write."""
    t = tqdm_telegram(disable=True)
    dummy = DummyIO()
    t.tgio = dummy
    # Prepare a format_dict that would normally contain a bar placeholder
    t.format_dict = {
        "bar_format": "Progress: <bar/>",
        "n": 5,
        "total": 10,
        "elapsed": 1,
        "rate": 5,
        "remaining": 5,
        "desc": "test",
    }
    # Call display; it should call dummy.write with the formatted string
    t.display()
    assert dummy.written, "tgio.write should have been called"
    written = dummy.written[-1]
    # The bar placeholder should be replaced with a formatted bar
    assert "{bar:10u}" in written, "bar placeholder not replaced correctly"

def test_clear_writes_empty_when_not_disabled(tmp_path):
    """clear should call tgio.write('') when not disabled."""
    t = tqdm_telegram(disable=False)
    dummy = DummyIO()
    t.tgio = dummy
    t.clear()
    assert dummy.written, "tgio.write should have been called during clear"
    assert dummy.written[-1] == "", "clear should write an empty string"
