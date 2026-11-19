import importlib
import types
import pytest

# Import the target module and its constants
unix = importlib.import_module("thefuck.system.unix")
const = importlib.import_module("thefuck.system.unix.const")

def test_get_key_mapping(monkeypatch):
    """
    Verify that a key present in KEY_MAPPING is translated correctly.
    """
    # Choose a key that is guaranteed to be in the mapping
    key_in_mapping = next(iter(const.KEY_MAPPING))
    expected = const.KEY_MAPPING[key_in_mapping]

    # Monkeypatch getch to return the chosen key
    monkeypatch.setattr(unix, "getch", lambda: key_in_mapping)

    result = unix.get_key()
    assert result == expected, f"Expected {expected!r} for key {key_in_mapping!r}, got {result!r}"


def test_get_key_escape_sequence(monkeypatch):
    """
    Verify that an escape sequence for the up arrow is interpreted as KEY_UP.
    """
    # Sequence: ESC '[' 'A'
    sequence = iter(["\x1b", "[", "A"])
    monkeypatch.setattr(unix, "getch", lambda: next(sequence))

    result = unix.get_key()
    assert result == const.KEY_UP, f"Expected {const.KEY_UP!r} for up arrow sequence, got {result!r}"


def test_get_key_default(monkeypatch):
    """
    Verify that a key not in KEY_MAPPING and not part of an escape sequence
    is returned unchanged.
    """
    # Return a printable character that is not in the mapping
    non_mapped_char = "z"
    monkeypatch.setattr(unix, "getch", lambda: non_mapped_char)

    result = unix.get_key()
    assert result == non_mapped_char, f"Expected {non_mapped_char!r} unchanged, got {result!r}"
