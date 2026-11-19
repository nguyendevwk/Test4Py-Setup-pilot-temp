import sys
import colorama
import pytest

# Import the function under test
from thefuck.logs import warn

# Ensure colorama is initialized for consistent output
colorama.init()


def test_warn_with_normal_title(capsys):
    """Warn should write a formatted warning with the given title."""
    title = "Disk space low"
    warn(title)
    captured = capsys.readouterr()
    # The output should end with a newline
    assert captured.err.endswith("\n")
    # The output should contain the title
    assert title in captured.err
    # The output should start with the red background and white bright text
    expected_start = (
        colorama.Back.RED + colorama.Fore.WHITE + colorama.Style.BRIGHT
    )
    assert captured.err.startswith(expected_start)
    # The output should end with the reset style
    assert captured.err.strip().endswith(colorama.Style.RESET_ALL)


def test_warn_with_empty_title(capsys):
    """Warn should handle an empty title gracefully."""
    warn("")
    captured = capsys.readouterr()
    # The output should still contain the warning prefix and reset code
    assert captured.err.startswith(
        colorama.Back.RED + colorama.Fore.WHITE + colorama.Style.BRIGHT
    )
    assert captured.err.strip().endswith(colorama.Style.RESET_ALL)
    # There should be no title text between the prefix and reset
    middle = captured.err[len(colorama.Back.RED + colorama.Fore.WHITE + colorama.Style.BRIGHT):-len(colorama.Style.RESET_ALL)]
    assert middle.strip() == ""


def test_warn_with_non_string_title(capsys):
    """Warn should convert non-string titles to their string representation."""
    title_obj = 42
    warn(title_obj)
    captured = capsys.readouterr()
    # The output should contain the string representation of the object
    assert "42" in captured.err
    # Ensure the formatting is still correct
    assert captured.err.startswith(
        colorama.Back.RED + colorama.Fore.WHITE + colorama.Style.BRIGHT
    )
    assert captured.err.strip().endswith(colorama.Style.RESET_ALL)
