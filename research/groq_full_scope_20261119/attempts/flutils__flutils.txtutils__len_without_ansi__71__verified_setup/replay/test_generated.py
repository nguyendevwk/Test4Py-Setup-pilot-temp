import re
import pytest
from flutils.txtutils import len_without_ansi

# Regular expression used inside the function (re-exported for clarity)
_ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def test_len_without_ansi_single_string_with_ansi():
    """A single string containing ANSI escape codes should return the
    length of the visible characters only."""
    text = "\x1b[38;5;209mfoobar\x1b[0m"
    # The visible text is "foobar" which has 6 characters
    assert len_without_ansi(text) == 6

def test_len_without_ansi_list_of_strings_with_mixed_content():
    """A list of strings, some with ANSI codes and some plain, should
    correctly sum the lengths of the visible parts."""
    parts = [
        "\x1b[31mred\x1b[0m",
        "text",
        "\x1b[1mbold\x1b[0m",
        "\x1b[0m",  # only ANSI, no visible chars
    ]
    # Visible parts: "red" (3), "text" (4), "bold" (4) => total 11
    assert len_without_ansi(parts) == 11

def test_len_without_ansi_invalid_sequence_raises_type_error():
    """Passing a non-sequence (e.g., an integer) should raise a TypeError
    because the function expects a sequence of strings."""
    with pytest.raises(TypeError):
        len_without_ansi(123)
