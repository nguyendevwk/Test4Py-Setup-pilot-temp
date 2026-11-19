import importlib
import pytest

# Import the module under test
unix = importlib.import_module("thefuck.system.unix")
const = importlib.import_module("thefuck.const")

# Helper to patch getch in the module
def patch_getch(monkeypatch, values):
    """Return successive values from `values` each time getch() is called."""
    it = iter(values)

    def fake_getch():
        return next(it)

    monkeypatch.setattr(unix, "getch", fake_getch)


def test_get_key_returns_mapped_key(monkeypatch):
    """
    When getch returns a character that is present in const.KEY_MAPPING,
    get_key should return the mapped value.
    """
    # Pick a key that is guaranteed to be in the mapping
    key_char = next(iter(const.KEY_MAPPING))
    expected = const.KEY_MAPPING[key_char]

    patch_getch(monkeypatch, [key_char])

    result = unix.get_key()
    assert result == expected, f"Expected {expected!r} for key {key_char!r}, got {result!r}"


def test_get_key_handles_escape_up(monkeypatch):
    """
    When getch returns the escape sequence for the up arrow,
    get_key should return const.KEY_UP.
    """
    # Escape sequence: '\x1b' '[' 'A'
    patch_getch(monkeypatch, ["\x1b", "[", "A"])

    result = unix.get_key()
    assert result == const.KEY_UP, f"Expected {const.KEY_UP!r} for up arrow, got {result!r}"


def test_get_key_handles_escape_down(monkeypatch):
    """
    When getch returns the escape sequence for the down arrow,
    get_key should return const.KEY_DOWN.
    """
    # Escape sequence: '\x1b' '[' 'B'
    patch_getch(monkeypatch, ["\x1b", "[", "B"])

    result = unix.get_key()
    assert result == const.KEY_DOWN, f"Expected {const.KEY_DOWN!r} for down arrow, got {result!r}"
