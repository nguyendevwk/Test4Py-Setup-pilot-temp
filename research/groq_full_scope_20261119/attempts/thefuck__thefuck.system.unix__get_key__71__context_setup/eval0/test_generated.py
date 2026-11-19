import builtins
import io
import types
import pytest

# Import the target module
from thefuck.system.unix import get_key, getch
from thefuck import const

# Helper to monkeypatch getch in the module
def _patch_getch(return_values):
    """Return a function that yields values from return_values sequentially."""
    it = iter(return_values)

    def fake_getch():
        try:
            return next(it)
        except StopIteration:
            return ''

    return fake_getch

def test_get_key_returns_regular_character(monkeypatch):
    """get_key should return the character itself when not a special key."""
    # Simulate pressing 'a'
    monkeypatch.setattr('thefuck.system.unix.getch', _patch_getch(['a']))
    assert get_key() == 'a'

def test_get_key_arrow_up_and_down(monkeypatch):
    """get_key should map escape sequences for arrow up/down to constants."""
    # Simulate pressing escape + '[' + 'A' (arrow up)
    monkeypatch.setattr('thefuck.system.unix.getch', _patch_getch(['\x1b', '[', 'A']))
    assert get_key() == const.KEY_UP

    # Simulate pressing escape + '[' + 'B' (arrow down)
    monkeypatch.setattr('thefuck.system.unix.getch', _patch_getch(['\x1b', '[', 'B']))
    assert get_key() == const.KEY_DOWN

def test_get_key_unknown_escape_sequence(monkeypatch):
    """get_key should return the first character of an unknown escape sequence."""
    # Simulate pressing escape + '[' + 'C' (unknown arrow)
    monkeypatch.setattr('thefuck.system.unix.getch', _patch_getch(['\x1b', '[', 'C']))
    # The function will return the first character of the sequence, i.e., '\x1b'
    assert get_key() == '\x1b'
