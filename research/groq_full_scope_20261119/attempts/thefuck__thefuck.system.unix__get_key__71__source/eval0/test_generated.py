import builtins
import importlib
import types

import pytest

# Import the target module
from thefuck.system.unix import get_key, const

# Helper to patch getch in the module
def patch_getch(return_values):
    """
    Return a context manager that patches the module's getch function
    to yield values from `return_values` sequentially.
    """
    def generator():
        for val in return_values:
            yield val
    gen = generator()

    def fake_getch():
        return next(gen)

    return pytest.MonkeyPatch().setattr(get_key.__globals__['getch'], fake_getch)


def test_get_key_normal_mapping(monkeypatch):
    """
    Test that a key present in const.KEY_MAPPING is correctly mapped.
    """
    # Pick a key that is guaranteed to be in the mapping
    key_char = next(iter(const.KEY_MAPPING))
    expected = const.KEY_MAPPING[key_char]

    # Patch getch to return this key
    with patch_getch([key_char]):
        result = get_key()
    assert result == expected, f"Expected {expected!r} for key {key_char!r}, got {result!r}"


def test_get_key_escape_sequence_up(monkeypatch):
    """
    Test that the escape sequence for the up arrow returns const.KEY_UP.
    """
    # Escape sequence: ESC [ A
    with patch_getch(['\x1b', '[', 'A']):
        result = get_key()
    assert result == const.KEY_UP, f"Expected {const.KEY_UP!r} for up arrow, got {result!r}"


def test_get_key_default_return(monkeypatch):
    """
    Test that an unmapped key returns itself.
    """
    # Use a character not in KEY_MAPPING and not part of an escape sequence
    key_char = 'z'
    with patch_getch([key_char]):
        result = get_key()
    assert result == key_char, f"Expected {key_char!r} for unmapped key, got {result!r}"
