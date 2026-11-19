import pytest
from tqdm.contrib.telegram import tqdm_telegram
from tqdm.auto import tqdm

class DummyIO:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.writes = []
    def write(self, msg):
        self.writes.append(msg)
    def delete(self):
        self.writes.append("deleted")

@pytest.fixture
def monkeypatch_tio(monkeypatch):
    monkeypatch.setattr("tqdm.contrib.telegram.TelegramIO", DummyIO)

def test_disable_prevents_tgio_creation(monkeypatch_tio):
    # When disable=True, tgio should not be created
    pbar = tqdm_telegram(range(3), disable=True, token="x", chat_id="y")
    assert not hasattr(pbar, "tgio")
    # Iterating should not raise
    for _ in pbar:
        pass

def test_display_modifies_bar_format_and_writes(monkeypatch_tio):
    # Create a progress bar with a custom bar_format
    pbar = tqdm_telegram(range(2), disable=False, token="x", chat_id="y",
                         bar_format="{l_bar}{bar}|{n_fmt}/{total_fmt}")
    # Force a display call
    pbar.display()
    # The DummyIO should have recorded the formatted message
    assert pbar.tgio.writes, "No write recorded"
    # The bar_format should have been modified to include width specifier
    assert "{bar:10u}" in pbar.tgio.writes[0]

def test_close_deletes_when_not_leaving(monkeypatch_tio):
    # Create a progress bar that does not leave the bar on close
    pbar = tqdm_telegram(range(1), disable=False, token="x", chat_id="y",
                         leave=False)
    # Close the bar
    pbar.close()
    # DummyIO should have recorded a delete call
    assert "deleted" in pbar.tgio.writes
