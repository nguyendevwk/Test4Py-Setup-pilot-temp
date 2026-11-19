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

    return pytest.MonkeyPatch().setattr('thefuck.system.unix.getch', fake_getch)


def test_get_key_mapped_character():
    """
    When getch returns a character that is present in const.KEY_MAPPING,
    get_key should return the mapped value.
    """
    # Pick a key that is mapped, e.g., 'a' -> const.KEY_A
    key = 'a'
    expected = const.KEY_MAPPING[key]
    with patch_getch([key]):
        result = get_key()
    assert result == expected, f"Expected mapping for '{key}' to be {expected!r}, got {result!r}"


def test_get_key_escape_sequence_up_down():
    """
    When getch returns an escape sequence for arrow keys,
    get_key should return the corresponding constants.
    """
    # Test Arrow Up
    with patch_getch(['\x1b', '[', 'A']):
        result_up = get_key()
    assert result_up == const.KEY_UP, f"Expected {const.KEY_UP!r} for Arrow Up, got {result_up!r}"

    # Test Arrow Down
    with patch_getch(['\x1b', '[', 'B']):
        result_down = get_key()
    assert result_down == const.KEY_DOWN, f"Expected {const.KEY_DOWN!r} for Arrow Down, got {result_down!r}"


def test_get_key_default_return():
    """
    When getch returns a character that is not mapped and not part of an escape sequence,
    get_key should return the character itself.
    """
    # Use a character not in KEY_MAPPING and not an escape sequence
    key = 'z'
    with patch_getch([key]):
        result = get_key()
    assert result == key, f"Expected default return of '{key}', got {result!r}"
