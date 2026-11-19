import sys
import pytest
from thefuck.logs import warn
from colorama import Back, Fore, Style

def test_warn_outputs_to_stderr_and_contains_title(capsys):
    """Warn should write the formatted warning to stderr."""
    test_title = "Test warning message"
    warn(test_title)
    out, err = capsys.readouterr()
    assert out == ""  # nothing should be printed to stdout
    # Build expected string
    expected = (
        f"{Back.RED}{Fore.WHITE}{Style.BRIGHT}[WARN] {test_title}{Style.RESET_ALL}\n"
    )
    assert err == expected

def test_warn_with_empty_title(capsys):
    """Warn should handle an empty title gracefully."""
    warn("")
    out, err = capsys.readouterr()
    expected = f"{Back.RED}{Fore.WHITE}{Style.BRIGHT}[WARN] {Style.RESET_ALL}\n"
    assert err == expected
    assert out == ""

def test_warn_with_special_characters(capsys):
    """Warn should correctly escape and display special characters."""
    special_title = "Line1\nLine2\tUnicode: \u2603"
    warn(special_title)
    out, err = capsys.readouterr()
    expected = (
        f"{Back.RED}{Fore.WHITE}{Style.BRIGHT}[WARN] {special_title}{Style.RESET_ALL}\n"
    )
    assert err == expected
    assert out == ""
