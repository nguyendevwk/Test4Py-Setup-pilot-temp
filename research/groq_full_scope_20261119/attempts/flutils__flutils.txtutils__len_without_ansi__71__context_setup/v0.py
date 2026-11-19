import re
import pytest
from flutils.txtutils import len_without_ansi

# Helper ANSI escape sequence used in the implementation
_ANSI_RE = re.compile(r'(\x1b\[[0-9;:]+[ABCDEFGHJKSTfhilmns])')

def test_len_without_ansi_single_string_with_ansi():
    # ANSI escape codes should not be counted in the length
    text = "\x1b[38;5;209mfoobar\x1b[0m"
    assert len_without_ansi(text) == 6
    # Verify that the function correctly strips the ANSI codes
    stripped = _ANSI_RE.split(text)
    assert stripped == ['', 'foobar', '']
    # The function should ignore the empty strings produced by the split
    assert all(part == '' or part.isprintable() for part in stripped)

def test_len_without_ansi_sequence_of_strings():
    # A list of strings containing ANSI codes and plain text
    seq = ["\x1b[31mred\x1b[0m", "green", "\x1b[32m", "blue\x1b[0m"]
    # Expected length: "red" (3) + "green" (5) + "blue" (4) = 12
    assert len_without_ansi(seq) == 12
    # Ensure that the function does not modify the original sequence
    assert seq == ["\x1b[31mred\x1b[0m", "green", "\x1b[32m", "blue\x1b[0m"]

def test_len_without_ansi_edge_cases_and_errors():
    # Empty string should return 0
    assert len_without_ansi("") == 0
    # String with only ANSI codes should return 0
    assert len_without_ansi("\x1b[0m\x1b[31m") == 0
    # Non-string elements in the sequence should be ignored
    seq = ["text", 123, None, "\x1b[32mgreen\x1b[0m"]
    # Only "text" (4) and "green" (5) contribute to the length
    assert len_without_ansi(seq) == 9
    # Passing an object without a 'capitalize' attribute should raise AttributeError
    class Dummy:
        pass
    dummy = Dummy()
    with pytest.raises(AttributeError):
        len_without_ansi(dummy)
