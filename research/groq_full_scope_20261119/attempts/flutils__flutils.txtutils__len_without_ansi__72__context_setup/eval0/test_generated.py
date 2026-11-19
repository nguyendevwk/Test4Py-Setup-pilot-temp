import re
import pytest
from flutils.txtutils import len_without_ansi, _ANSI_RE

def test_len_without_ansi_single_string_with_ansi():
    # ANSI escape sequence for bright magenta foreground
    text = "\x1b[38;5;209mfoobar\x1b[0m"
    # The function should ignore the escape codes and return the length of "foobar"
    assert len_without_ansi(text) == 6
    # Verify that the regex correctly splits the string into parts
    parts = _ANSI_RE.split(text)
    assert parts == ['', '\x1b[38;5;209m', 'foobar', '\x1b[0m', '']
    # The function should not count the escape sequences
    assert all(part not in _ANSI_RE.pattern for part in parts if part)

def test_len_without_ansi_list_of_strings_with_mixed_content():
    # A list containing plain text and ANSI sequences interleaved
    seq = ["Hello ", "\x1b[31m", "world", "\x1b[0m", "!"]
    # The function should count only the visible characters
    assert len_without_ansi(seq) == len("Hello world!")
    # Ensure that the function treats each element correctly
    # The ANSI codes should be ignored, but the exclamation mark counted
    assert len_without_ansi(["\x1b[32m", "green", "\x1b[0m"]) == len("green")

def test_len_without_ansi_empty_and_non_string_input():
    # Empty string should return 0
    assert len_without_ansi("") == 0
    # Passing a list of empty strings should also return 0
    assert len_without_ansi(["", ""]) == 0
    # Passing a non-string sequence that contains no ANSI codes
    assert len_without_ansi([123, 45]) == 2  # each element counted as length 1
    # Passing a sequence with mixed types should raise a TypeError when
    # attempting to call .capitalize on a non-string element
    with pytest.raises(AttributeError):
        len_without_ansi([123, "\x1b[0m"])
