import re
import pytest
from flutils.txtutils import len_without_ansi

# Regular expression used inside the module (re‑exported for testing)
_ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def test_len_without_ansi_single_string_with_ansi():
    """Length of a single string containing ANSI escape codes."""
    text = "\x1b[38;5;209mfoobar\x1b[0m"
    # The ANSI codes should not be counted
    assert len_without_ansi(text) == 6
    # Verify that the function also works when the string is wrapped in a list
    assert len_without_ansi([text]) == 6

def test_len_without_ansi_list_of_strings():
    """Length of a list of strings, some containing ANSI codes."""
    parts = [
        "Hello ",
        "\x1b[31mworld\x1b[0m",
        "!",
        "\x1b[1mBold\x1b[0m"
    ]
    # Expected length: len("Hello ") + len("world") + len("!") + len("Bold") = 6 + 5 + 1 + 4 = 16
    assert len_without_ansi(parts) == 16

def test_len_without_ansi_empty_and_non_string_elements():
    """Edge cases: empty string and non‑string elements."""
    # Empty string should return 0
    assert len_without_ansi("") == 0
    # Passing a list with a non‑string element should raise a TypeError
    with pytest.raises(TypeError):
        len_without_ansi([123, "\x1b[0m"])
