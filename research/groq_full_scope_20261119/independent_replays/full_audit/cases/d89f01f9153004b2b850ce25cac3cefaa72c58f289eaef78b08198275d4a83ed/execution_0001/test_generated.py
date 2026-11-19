import sys
import io
import colorama
import pytest
from thefuck.logs import failed

# Ensure colorama is initialized for tests
colorama.init(autoreset=True)

def test_failed_writes_colored_message(capsys):
    """The failed function should write the message to stderr with red color."""
    test_msg = "Error occurred"
    failed(test_msg)
    captured = capsys.readouterr()
    # The output should end with a newline
    assert captured.err.endswith("\n")
    # Strip the newline for easier comparison
    output = captured.err.rstrip("\n")
    # The output should contain the red color code and the reset code
    assert colorama.Fore.RED in output
    assert colorama.Style.RESET_ALL in output
    # The message should be present between the color codes
    assert test_msg in output

def test_failed_with_empty_string(capsys):
    """Passing an empty string should still produce a colored newline."""
    failed("")
    captured = capsys.readouterr()
    # The output should be just the color codes and a newline
    output = captured.err.rstrip("\n")
    assert output == f"{colorama.Fore.RED}{colorama.Style.RESET_ALL}"
    assert captured.err.endswith("\n")

def test_failed_with_non_string_input(capsys):
    """The function should convert non-string inputs to string."""
    number = 42
    failed(number)
    captured = capsys.readouterr()
    output = captured.err.rstrip("\n")
    # The numeric value should appear in the output
    assert "42" in output
    # Color codes should still be present
    assert colorama.Fore.RED in output
    assert colorama.Style.RESET_ALL in output
