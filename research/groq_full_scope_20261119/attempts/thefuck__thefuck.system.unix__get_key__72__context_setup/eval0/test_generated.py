import builtins
import io
import types
import pytest

# Import the target module
from thefuck.system.unix import get_key, getch, const

# Helper to monkeypatch getch in the module
def patch_getch(return_values):
    """Return a function that yields values from return_values sequentially."""
    values = iter(return_values)

    def fake_getch():
        return next(values)
    return fake_getch

def test_get_key_normal_char(monkeypatch):
    """When a normal character is pressed, it should be returned unchanged."""
    # Patch getch to return 'a'
    monkeypatch.setattr(get_key.__globals__, 'getch', patch_getch(['a']))
    result = get_key()
    assert result == 'a', "Normal character should be returned as is"

def test_get_key_arrow_up(monkeypatch):
    """When the up arrow key sequence is pressed, it should return KEY_UP."""
    # Escape sequence for up arrow: ESC [ A
    monkeypatch.setattr(get_key.__globals__, 'getch', patch_getch(['\x1b', '[', 'A']))
    result = get_key()
    assert result == const.KEY_UP, "Up arrow should map to KEY_UP"

def test_get_key_unknown_escape(monkeypatch):
    """When an unknown escape sequence is pressed, it should return the first escape char."""
    # Escape sequence: ESC [ Z (unknown)
    monkeypatch.setattr(get_key.__globals__, 'getch', patch_getch(['\x1b', '[', 'Z']))
    result = get_key()
    assert result == '\x1b', "Unknown escape should return the ESC character"
