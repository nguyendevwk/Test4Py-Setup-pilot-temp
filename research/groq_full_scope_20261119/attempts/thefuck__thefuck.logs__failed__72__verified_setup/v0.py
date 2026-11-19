import sys
import io
import pytest
from thefuck.logs import failed
from colorama import Fore, Style

def test_failed_writes_colored_message(capsys):
    """The function should write the message to stderr wrapped in red color codes."""
    test_msg = "Error occurred"
    failed(test_msg)
    captured = capsys.readouterr()
    # The output should contain the message and the color codes
    assert test_msg in captured.err
    assert Fore.RED in captured.err
    assert Style.RESET_ALL in captured.err
    # Ensure nothing was printed to stdout
    assert captured.out == ""

def test_failed_with_empty_string(capsys):
    """An empty string should still produce a line with only color codes."""
    failed("")
    captured = capsys.readouterr()
    # The output should still contain the color codes and a newline
    assert captured.err.strip() == ""
    assert Fore.RED in captured.err
    assert Style.RESET_ALL in captured.err
    assert captured.out == ""

def test_failed_with_none_value(capsys):
    """Passing None should convert it to the string 'None' and write it."""
    failed(None)
    captured = capsys.readouterr()
    assert "None" in captured.err
    assert Fore.RED in captured.err
    assert Style.RESET_ALL in captured.err
    assert captured.out == ""
