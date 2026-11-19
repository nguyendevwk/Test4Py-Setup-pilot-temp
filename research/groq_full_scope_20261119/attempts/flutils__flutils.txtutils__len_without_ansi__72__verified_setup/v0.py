import re
import pytest
from flutils.txtutils import len_without_ansi

def test_len_without_ansi_single_string_with_ansi():
    # ANSI escape sequence for color
    text = "\x1b[38;5;209mfoobar\x1b[0m"
    # The visible characters are "foobar" which has length 6
    assert len_without_ansi(text) == 6

def test_len_without_ansi_list_of_strings_with_mixed_ansi():
    # Mixed list: some strings contain ANSI codes, some don't
    seq = [
        "\x1b[31mred\x1b[0m",
        "plain",
        "\x1b[1mbold\x1b[0m",
        "\x1b[32mgreen\x1b[0m"
    ]
    # Visible characters: "redplainboldgreen" -> length 19
    assert len_without_ansi(seq) == 19

def test_len_without_ansi_empty_and_non_ansi():
    # Empty string should return 0
    assert len_without_ansi("") == 0
    # String without ANSI codes should count all characters
    assert len_without_ansi("noansi") == 6
